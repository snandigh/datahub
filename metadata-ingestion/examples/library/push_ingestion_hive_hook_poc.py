from confluent_kafka import Consumer
import json, logging

group_id = "hive-hook"
env = 'PROD' ## this had to be in uppercase
platform = 'hive'
logger = logging.getLogger(__name__)


from datahub.emitter.kafka_emitter import DatahubKafkaEmitter, KafkaEmitterConfig
from datahub.metadata.com.linkedin.pegasus2avro.common import Status
from datahub.metadata.schema_classes import BrowsePathsClass

from datahub.ingestion.extractor.schema_util import *

from datahub.metadata.com.linkedin.pegasus2avro.schema import SchemaField, SchemaFieldDataType,SchemaMetadata, MySqlDDL

from datahub.metadata.schema_classes import (
    DatasetSnapshotClass,
    MetadataChangeEventClass
)


SchemaConverter = AvroToMceSchemaConverter(is_key_schema=False)

# consumer from ATLAS_HOOK kafka topic
consumer_conf = {'bootstrap.servers': "xxx",
                 'group.id': group_id,
                 'auto.offset.reset': 'earliest',
                 'security.protocol': 'SASL_SSL',
                 'sasl.mechanisms': 'PLAIN',
                 'sasl.username': 'xxx',
                 'sasl.password': 'xxx'
                 }

topic = 'ATLAS_HOOK'
consumer = Consumer(consumer_conf)
# Subscribe to topic
consumer.subscribe([topic])

# created an emitter where  the mce will be emitted, it will be DataHub's Kafka broker in docker (for PoC)
emitter = DatahubKafkaEmitter(
    KafkaEmitterConfig.parse_obj(
        # This is the same config format as the standard Kafka sink's YAML.
        {
            "connection": {
                "bootstrap": "localhost:9092",
                "producer_config": {},
                "schema_registry_url": "http://localhost:8081",
            }
        }
    )
)


def process_json(msg):
    result_dict = {'msgCreatedBy': msg['msgCreatedBy'], 'msgCreationTime': msg['msgCreationTime']}
    message = msg['message']
    result_dict['ddl_type'] = message['type']

    # table attributes
    table_attributes = message['entities']['entities'][0]['attributes']
    result_dict['table_name'] = table_attributes['name']
    result_dict['db_name'] = table_attributes['qualifiedName'].split(".")[0]
    result_dict['table_comment'] = table_attributes['comment']

    # other attributes
    ref_entities = message['entities']['referredEntities']
    ref_keys = list(ref_entities.keys())
    col = []
    for _i in ref_keys:
        type_name = ref_entities[_i]['typeName']
        attributes = ref_entities[_i]['attributes']
        if type_name == 'hive_storagedesc':
            result_dict['location'] = attributes['location']
        elif type_name == 'hive_column':
            col.append(
                {'name': attributes['name'], 'comment': attributes['comment'], 'position': attributes['position'],
                 'type': attributes['type']})

    result_dict['cols'] = col
    return result_dict


# Process messages
def make_mce(m) -> MetadataChangeEventClass:
    entity = m['table_name']
    schema = m['db_name']
    dataset_name = f"{schema}.{entity}"

    dataset_snapshot = DatasetSnapshotClass(
        urn=f"urn:li:dataset:(urn:li:dataPlatform:{platform},{dataset_name},{env})",
        aspects=[],  # we append to this list later on
    )
    dataset_snapshot.aspects.append(Status(removed=False))
    canonical_schema: List[SchemaField] = []

    for column in m['cols']:
        field = SchemaField(
            fieldPath=column.get("name"),
            type= SchemaConverter._get_column_type(column.get('type')),
            nativeDataType=column.get('type'),
            description=column.get('comment'),
            nullable=True,
            recursive=False,
        )
        canonical_schema.append(field)

    schema_metadata = SchemaMetadata(
        schemaName=dataset_name,
        platform=f"urn:li:dataPlatform:{platform}",
        version=0,
        hash="",
        platformSchema=MySqlDDL(tableSchema=""),  # Looks like it needs some platform schema, else gives error !
        fields=canonical_schema,
    )
    dataset_snapshot.aspects.append(schema_metadata)

    # browse_path = BrowsePathsClass(
    #     [f"/prod/{platform}/{schema}"]
    # )
    # dataset_snapshot.aspects.append(browse_path)

    mce = MetadataChangeEventClass(proposedSnapshot=dataset_snapshot)
    return mce


def callback(err, msg):
    print('ingested row')
    if err:
        # Handle the metadata emission error.
        print("error:", err)


try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            print("Waiting for message or event/error in poll()")
            continue
        elif msg.error():
            print('error: {}'.format(msg.error()))
        else:
            # Check for Kafka message
            record_value = msg.value()
            data = json.loads(record_value)
            m = process_json(data)
            print(m)
            print('sending data to datahub')
            mce = make_mce(m)
            # emit the mce to kafka
            emitter.emit_mce_async(mce, callback)
            emitter.flush()


except KeyboardInterrupt:
    pass
finally:
    # Leave group and commit final offsets
    consumer.close()
