import os
import json
import hashlib
from typing import Any
from neo4j import GraphDatabase
from pathlib import Path
from loguru import logger

class Neo4jBuilder:
    def __init__(self, batch_size: int = 100) -> None:
        self.batch_size = batch_size
        self.cypher_base_path = Path('/Users/dolor.src/code/Nornikel-AI-Science-Hack/src/db/data_loader/cypher')
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=(os.environ.get("NEO4J_USERNAME"), os.environ.get("NEO4J_PASSWORD")))
        
    
    def _run_cypher(self, script: str) -> str:
        script_path = self.cypher_base_path  / f'{script}.cypher'
        return script_path.read_text(encoding='utf-8')
    
    def _setup(self) -> None:
        with self.driver.session() as session:
            session.run(self._run_cypher('entity_constraints'))
            session.run(self._run_cypher('fact_constraints'))
            session.run(self._run_cypher('claim_constraints'))
            session.run(self._run_cypher('entity_index'))
    
    def _merge_entities_tx(self, tx, batch):
        query = self._run_cypher('merge_entities')
        tx.run(query, batch=batch)
    
    def _load_entities(self, entities: list[dict[str, Any]]):
        """Загрузка сущностей пакетами"""
        logger.info(f"Loading {len(entities)} entities...")
        
        for i in range(0, len(entities), self.batch_size):
            batch = entities[i:i + self.batch_size]
            
            with self.driver.session() as session:
                session.execute_write(self._merge_entities_tx, batch)
                
        logger.success(f"✅ Loaded {len(entities)} entities")

    
    def _merge_relations_tx(self, tx, batch):
        query = self._run_cypher('merge_relations')
        tx.run(query, batch=batch)

    def _load_relations(self, relations: list[dict]):
        """Загрузка связей"""
        logger.info(f"Loading {len(relations)} relations...")
        
        for i in range(0, len(relations), self.batch_size):
            batch = relations[i:i + self.batch_size]
            
            with self.driver.session() as session:
                session.execute_write(self._merge_relations_tx, batch)
                
        logger.success(f"✅ Loaded {len(relations)} relations")
    
    def _create_facts_tx(self, tx, batch):
        query = self._run_cypher('create_facts')
        tx.run(query, batch=batch)
    
    def _load_facts(self, facts: list[dict]):
        """Загрузка числовых фактов"""
        logger.info(f"Loading {len(facts)} facts...")
        
        for i in range(0, len(facts), self.batch_size):
            batch = facts[i:i + self.batch_size]
            
            with self.driver.session() as session:
                session.execute_write(self._create_facts_tx, batch)
                
        logger.success(f"✅ Loaded {len(facts)} facts")
    
    def _create_claims_tx(self, tx, batch):
        query = self._run_cypher('create_claims')
        tx.run(query, batch=batch)

    def _load_claims(self, claims: list[dict]):
        """Загрузка утверждений"""
        logger.info(f"Loading {len(claims)} claims...")
        
        for i in range(0, len(claims), self.batch_size):
            batch = claims[i:i + self.batch_size]
            
            with self.driver.session() as session:
                session.execute_write(self._create_claims_tx, batch)
                
        logger.success(f"✅ Loaded {len(claims)} claims")


    def prepare_data(self, obj):
        if isinstance(obj, dict):
            return {k: self.prepare_data(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.prepare_data(item) for item in obj]
        elif isinstance(obj, (dict,)):  # уже выше обработано
            return json.dumps(obj, ensure_ascii=False)
        else:
            return obj
    def process(self, data: dict[str, Any]) -> None:
        data = self.prepare_data(data)
        entities = data.get("entities", [])
        relations = data.get("relations", [])
        facts = data.get("facts", [])
        claims = data.get("claims", [])

        for entity in entities:
            if "attributes" in entity and isinstance(entity["attributes"], dict):
                entity["attributes"] = json.dumps(entity["attributes"], ensure_ascii=False)

        # Преобразуем properties у связей
        for relation in relations:
            if "properties" in relation and isinstance(relation["properties"], dict):
                relation["properties"] = json.dumps(relation["properties"], ensure_ascii=False)


        for fact in facts:
            if "id" not in fact:
                fact["id"] = f"fact_{hashlib.md5(fact['parameter'].encode() + str(fact['value']).encode()).hexdigest()}"
            
        for claim in claims:
            if "id" not in claim:
                claim["id"] = f"claim_{hashlib.md5(claim['statement'].encode()).hexdigest()}"
    
        self._load_entities(entities)
        self._load_relations(relations)
        self._load_facts(facts)
        self._load_claims(claims)
        self.driver.close()


    