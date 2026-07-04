UNWIND $batch AS row
MERGE (c:Claim {id: row.id})
SET 
    c.statement = row.statement,
    c.evidence_level = row.evidence_level