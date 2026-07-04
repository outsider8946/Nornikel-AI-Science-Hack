UNWIND $batch AS row
MERGE (e:Entity {name: row.name})
ON CREATE SET 
    e.type = row.type,
    e.created_at = timestamp()
SET 
    e.synonyms = row.synonyms,
    e.attributes = row.attributes,
    e.updated_at = timestamp()