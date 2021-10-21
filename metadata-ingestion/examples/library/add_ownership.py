
env = 'DEV' ## this had to be in uppercase
platform = 'hive'

from datahub.emitter.kafka_emitter import DatahubKafkaEmitter, KafkaEmitterConfig
from datahub.emitter.rest_emitter import DatahubRestEmitter

from datahub.ingestion.extractor.schema_util import *

from datahub.metadata.schema_classes import (
    DatasetSnapshotClass,
    MetadataChangeEventClass,
    OwnerClass,
    OwnershipClass,
    OwnershipTypeClass,
)

source_file_path = '/Users/snandi/Downloads/data/owner_data.json'

# created an emitter where  the mce will be emitted, it will be DataHub's Kafka broker in docker (for PoC)
# emitter = DatahubKafkaEmitter(
#     KafkaEmitterConfig.parse_obj(
#         # This is the same config format as the standard Kafka sink's YAML.
#         {
#             "connection": {
#                 "bootstrap": "localhost:9002",
#                 "producer_config": {},
#                 "schema_registry_url": "localhost:8081",
#             }
#         }
#     )
# )


# todo: 1. We have to make a living doc of table ownership 2. If we decide that to be  google doc,
# then create an Oauth or service account to access the  sheet programatically

import json
recs = []
with open(source_file_path, 'r') as f:
    for _i in f:
        row = json.loads(_i.rstrip('\n'))
        Email= row['Email']
        row['Owner'] = [f"urn:li:corpuser:{Email}"]
        recs.append(row)

# recs = [{'schema_name': 'integrated_core', 'table_name': 'order_fact', 'owner': ["urn:li:corpuser:hsk@grubhub.com"]}]


# Process messages
def add_owner_mce(m) -> MetadataChangeEventClass:
    entity = m['Table']
    schema = m['Schema']
    dataset_name = f"{schema}.{entity}"

    owners = [
        OwnerClass(owner=owner, type=OwnershipTypeClass.DATAOWNER)
        for owner in m['Owner']
    ]

    changed_snapshot = DatasetSnapshotClass(
        urn=f"urn:li:dataset:(urn:li:dataPlatform:{platform},{dataset_name},{env})",
        aspects=[],  # we append to this list later on
    )
    changed_snapshot.aspects.append(OwnershipClass(owners))
    mce = MetadataChangeEventClass(proposedSnapshot=changed_snapshot)
    return mce


def callback(err, msg):
    print('ingested row')
    if err:
        # Handle the metadata emission error.
        print("error:", err)


num_recs = len(recs)

# try REST emitter
Restemitter = DatahubRestEmitter("http://10.174.24.179:8080")


for _i in range(num_recs):
    print('sending data to datahub')
    mce = add_owner_mce(recs[_i])
    print(mce)
    # emit the mce to kafka
    # emitter.emit_mce_async(mce, callback)
    # emitter.flush()
    # emit mce to REST
    Restemitter.emit_mce(mce)
    num_recs -= 1
