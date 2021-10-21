# This is  temporary place to keep the JSON/AVRO schema for ATLAS integration

create_update_json_schema=StructType() \
    .add("version", StructType() \
         .add("version", StringType()) \
         .add("versionParts", ArrayType(LongType())) ) \
    .add("msgCompressionKind", StringType()) \
    .add("msgSplitIdx", LongType()) \
    .add("msgSplitCount", LongType()) \
    .add("msgSourceIP", StringType()) \
    .add("msgCreatedBy", StringType()) \
    .add("msgCreationTime", LongType()) \
    .add("message", StructType() \
         .add("type", StringType()) \
         .add("user", StringType()) \
         .add("entities",StructType() \
              .add("referredEntities", MapType(
    StringType(),
    StructType()
        .add("typeName", StringType()) \
        .add("attributes", StructType() \
             .add("owner", StringType()) \
             .add("qualifiedName", StringType()) \
             .add("name",StringType() ) \
             .add("comment",StringType() ) \
             .add("position", LongType()) \
             .add("type", StringType()) \
             .add("table", StructType()
                  .add("guid", StringType()) \
                  .add("typeName", StringType()) \
                  .add("uniqueAttributes", StructType()
                       .add("qualifiedName", StringType())
                       ) \
                  ) \
             ) \
        .add("guid", StringType()) \
        .add("provenanceType", LongType()) \
        .add("proxy", BooleanType()) \
        .add("version", LongType())
)
                   )
              .add("entities", ArrayType(StructType() \
                                         .add("attributes", StructType() \
                                              .add("columns", ArrayType(StructType() \
                                                                        .add("guid", StringType()) \
                                                                        .add("typeName", StringType()) \
                                                                        .add("uniqueAttributes", StructType()
                                                                             .add("qualifiedName", StringType())))
                                                   )
                                              .add("comment", StringType())
                                              .add("createTime", LongType())
                                              .add("db", StructType()
                                                   .add("guid", StringType())
                                                   .add("typeName", StringType())
                                                   .add("uniqueAttributes", StructType()
                                                        .add("qualifiedName", StringType())
                                                        ))
                                              .add("lastAccessTime", LongType())
                                              .add("name", StringType())
                                              .add("owner", StringType())
                                              .add("parameters", StructType()
                                                   .add("COLUMN_STATS_ACCURATE", StringType())
                                                   .add("numFiles", StringType())
                                                   .add("numRows", StringType())
                                                   .add("rawDataSize", StringType())
                                                   .add("totalSize", StringType())
                                                   .add("transient_lastDdlTime", StringType()))
                                              .add("partitionKeys", ArrayType(StringType()))
                                              .add("qualifiedName", StringType())
                                              .add("retention", StringType())
                                              .add("sd", StructType()
                                                   .add("guid", StringType())
                                                   .add("typeName", StringType())
                                                   .add("uniqueAttributes", StructType()
                                                        .add("qualifiedName", StringType())
                                                        ))
                                              .add("tableType", StringType())
                                              .add("temporary", BooleanType())
                                              )
                                         .add("guid", StringType())
                                         .add("provenanceType", LongType())
                                         .add("proxy", BooleanType())
                                         .add("typeName", StringType())
                                         .add("version", LongType())
                                         )
                   )
              )
         )
