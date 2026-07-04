UNWIND $batch AS row
MERGE (f:Fact {id: row.id})
SET 
    f.parameter = row.parameter,
    f.value = row.value,
    f.unit = row.unit,
    f.condition = row.condition,
    f.confidence = row.confidence