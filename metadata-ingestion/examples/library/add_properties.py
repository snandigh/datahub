# refer: https://github.com/linkedin/datahub/blob/9dff1b7a1ce43e56a251f2240883a935f458f764/metadata-ingestion/src/datahub/ingestion/source/sql/sql_common.py

from datahub.metadata.com.linkedin.pegasus2avro.metadata.snapshot import DatasetSnapshot
from datahub.metadata.com.linkedin.pegasus2avro.mxe import MetadataChangeEvent

from datahub.metadata.schema_classes import ChangeTypeClass, DatasetPropertiesClass
from datahub.emitter.rest_emitter import DatahubRestEmitter

from datahub.metadata.schema_classes import (
    DatasetSnapshotClass,
    MetadataChangeEventClass,
    OwnerClass,
    OwnershipClass,
    OwnershipTypeClass,
)

properties = {
    "Table Size": "2.45 GB",
    "Data Recency": "10/26/2021 6:43 AM CST",
    "Partition Key": "None",
    "Number of Rows": "142,543,234",
    "Number of Columns": "32",
    "Grain": "[diner_srg_key]",
    "Table Type": "Dimension",
    "Data Location": 's3://grubhub-gdp-marketing-data-assets-prod/shared/integrated_diner/diner_dim/run_id=20211026_1039'
}

platform = 'hive'
env = 'DEV'

dataset_name = 'integrated_diner.diner_dim'

datasetUrn = f"urn:li:dataset:(urn:li:dataPlatform:{platform},{dataset_name},{env})"
dataset_snapshot = DatasetSnapshot(
    urn=datasetUrn,
    aspects=[],
)


dataset_properties = DatasetPropertiesClass(
    description='master data for diners',
    customProperties=properties,
)
dataset_snapshot.aspects.append(dataset_properties)
mce = MetadataChangeEvent(proposedSnapshot=dataset_snapshot)

# try REST emitter
Restemitter = DatahubRestEmitter("http://10.174.24.179:8080")

Restemitter.emit_mce(mce)
