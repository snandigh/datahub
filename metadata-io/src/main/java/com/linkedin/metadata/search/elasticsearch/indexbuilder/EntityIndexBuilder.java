package com.linkedin.metadata.search.elasticsearch.indexbuilder;

import com.linkedin.metadata.models.EntitySpec;
import java.io.IOException;
import java.util.Map;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.elasticsearch.client.RestHighLevelClient;


@Slf4j
@RequiredArgsConstructor
public class EntityIndexBuilder {
  private final RestHighLevelClient searchClient;
  private final EntitySpec entitySpec;
  private final SettingsBuilder settingsBuilder;
  private final String indexName;

  public void buildIndex() throws IOException {
    log.info("Setting up index: {}", indexName);
    Map<String, Object> mappings = MappingsBuilder.getMappings(entitySpec);
    Map<String, Object> settings = settingsBuilder.getSettings();

    new IndexBuilder(searchClient, indexName, mappings, settings).buildIndex();
  }
}
