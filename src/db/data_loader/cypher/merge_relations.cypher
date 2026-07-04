UNWIND $batch AS row
MATCH (source:Entity {name: row.source})
MATCH (target:Entity {name: row.target})
MERGE (source)-[r:LINK {type: row.relation_type}]->(target)
SET r.properties = row.properties