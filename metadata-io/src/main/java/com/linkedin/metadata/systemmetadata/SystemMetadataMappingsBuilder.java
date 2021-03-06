package com.linkedin.metadata.systemmetadata;

import com.google.common.collect.ImmutableMap;
import java.util.HashMap;
import java.util.Map;
import lombok.extern.slf4j.Slf4j;


@Slf4j
public class SystemMetadataMappingsBuilder {

  private SystemMetadataMappingsBuilder() { }

  public static Map<String, Object> getMappings() {
    Map<String, Object> mappings = new HashMap<>();
    mappings.put("urn", getMappingsForKeyword());
    mappings.put("aspect", getMappingsForKeyword());
    mappings.put("runId", getMappingsForKeyword());
    mappings.put("lastUpdated", getMappingsForLastUpdated());

    return ImmutableMap.of("properties", mappings);
  }

  private static Map<String, Object> getMappingsForKeyword() {
    return ImmutableMap.<String, Object>builder().put("type", "keyword").build();
  }

  private static Map<String, Object> getMappingsForLastUpdated() {
    return ImmutableMap.<String, Object>builder().put("type", "long").build();
  }
}
