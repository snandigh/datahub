from typing import Callable, List, Union

import datahub.emitter.mce_builder as builder
from datahub.configuration.common import ConfigModel
from datahub.configuration.import_resolver import pydantic_resolve_key
from datahub.ingestion.api.common import PipelineContext
from datahub.ingestion.transformer.dataset_transformer import DatasetTransformer
from datahub.metadata.schema_classes import (
    DatasetSnapshotClass,
    GlobalTagsClass,
    MetadataChangeEventClass,
    TagAssociationClass,
)


class AddDatasetTagsConfig(ConfigModel):
    # Workaround for https://github.com/python/mypy/issues/708.
    # Suggested by https://stackoverflow.com/a/64528725/5004662.
    get_tags_to_add: Union[
        Callable[[DatasetSnapshotClass], List[TagAssociationClass]],
        Callable[[DatasetSnapshotClass], List[TagAssociationClass]],
    ]

    _resolve_tag_fn = pydantic_resolve_key("get_tags_to_add")


class AddDatasetTags(DatasetTransformer):
    """Transformer that adds tags to datasets according to a callback function."""

    ctx: PipelineContext
    config: AddDatasetTagsConfig

    def __init__(self, config: AddDatasetTagsConfig, ctx: PipelineContext):
        self.ctx = ctx
        self.config = config

    @classmethod
    def create(cls, config_dict: dict, ctx: PipelineContext) -> "AddDatasetTags":
        config = AddDatasetTagsConfig.parse_obj(config_dict)
        return cls(config, ctx)

    def transform_one(self, mce: MetadataChangeEventClass) -> MetadataChangeEventClass:
        if not isinstance(mce.proposedSnapshot, DatasetSnapshotClass):
            return mce
        tags_to_add = self.config.get_tags_to_add(mce.proposedSnapshot)
        if tags_to_add:
            tags = builder.get_or_add_aspect(
                mce,
                GlobalTagsClass(
                    tags=[],
                ),
            )
            tags.tags.extend(tags_to_add)

        return mce


class SimpleDatasetTagConfig(ConfigModel):
    tag_urns: List[str]


class SimpleAddDatasetTags(AddDatasetTags):
    """Transformer that adds a specified set of tags to each dataset."""

    def __init__(self, config: SimpleDatasetTagConfig, ctx: PipelineContext):
        tags = [TagAssociationClass(tag=tag) for tag in config.tag_urns]

        generic_config = AddDatasetTagsConfig(
            get_tags_to_add=lambda _: tags,
        )
        super().__init__(generic_config, ctx)

    @classmethod
    def create(cls, config_dict: dict, ctx: PipelineContext) -> "SimpleAddDatasetTags":
        config = SimpleDatasetTagConfig.parse_obj(config_dict)
        return cls(config, ctx)
