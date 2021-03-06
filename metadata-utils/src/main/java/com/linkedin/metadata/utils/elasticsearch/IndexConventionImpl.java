package com.linkedin.metadata.utils.elasticsearch;

import com.linkedin.data.template.RecordTemplate;
import com.linkedin.metadata.models.EntitySpec;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import javax.annotation.Nonnull;
import javax.annotation.Nullable;
import org.apache.commons.lang3.StringUtils;


// Default implementation of search index naming convention
public class IndexConventionImpl implements IndexConvention {
  private final Map<String, String> indexNameMapping = new HashMap<>();
  private final Optional<String> _prefix;
  private final String _getAllEntityIndicesPattern;
  private final String _getAllTemporalStatIndicesPattern;

  private final static String ENTITY_INDEX_VERSION = "v2";
  private final static String ENTITY_INDEX_SUFFIX = "index";
  private final static String TEMPORAL_STATS_INDEX_VERSION = "v1";
  private final static String TEMPORAL_STATS_ENTITY_INDEX_SUFFIX = "aspect";

  public IndexConventionImpl(@Nullable String prefix) {
    _prefix = StringUtils.isEmpty(prefix) ? Optional.empty() : Optional.of(prefix);
    _getAllEntityIndicesPattern =
        _prefix.map(p -> p + "_").orElse("") + "*" + ENTITY_INDEX_SUFFIX + "_" + ENTITY_INDEX_VERSION;
    _getAllTemporalStatIndicesPattern =
        _prefix.map(p -> p + "_").orElse("") + "*" + TEMPORAL_STATS_ENTITY_INDEX_SUFFIX + "_"
            + TEMPORAL_STATS_INDEX_VERSION;
  }

  private String createIndexName(String baseName) {
    return (_prefix.map(prefix -> prefix + "_").orElse("") + baseName).toLowerCase();
  }

  @Override
  public Optional<String> getPrefix() {
    return _prefix;
  }

  @Nonnull
  @Override
  public String getIndexName(Class<? extends RecordTemplate> documentClass) {
    return this.getIndexName(documentClass.getSimpleName());
  }

  @Nonnull
  @Override
  public String getIndexName(EntitySpec entitySpec) {
    return this.getIndexName(entitySpec.getName()) + ENTITY_INDEX_SUFFIX + "_" + ENTITY_INDEX_VERSION;
  }

  @Nonnull
  @Override
  public String getIndexName(String baseIndexName) {
    return indexNameMapping.computeIfAbsent(baseIndexName, this::createIndexName);
  }

  @Nonnull
  @Override
  public String getTimeseriesAspectIndexName(String entityName, String aspectName) {
    return this.getIndexName(entityName + "_" + aspectName) + TEMPORAL_STATS_ENTITY_INDEX_SUFFIX + "_"
        + TEMPORAL_STATS_INDEX_VERSION;
  }

  @Nonnull
  @Override
  public String getAllEntityIndicesPattern() {
    return _getAllEntityIndicesPattern;
  }

  @Nonnull
  @Override
  public String getAllTimeseriesAspectIndicesPattern() {
    return _getAllTemporalStatIndicesPattern;
  }
}
