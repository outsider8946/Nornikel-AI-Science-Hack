from tqdm.asyncio import tqdm
from src.utils.llm_worker import LLMWokrer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Any

class Deduplicator:
    def __init__(self, llm_worker: LLMWokrer, model: str, threshold: float = 0.85) -> None:
        self.llm_worker = llm_worker
        self.model = model
        self.threshold = threshold
    
    def _merge_entities_by_types(self, entities: list[dict[str, Any]]) -> dict[str, Any]:
        type_map = {}
        for entity in entities:
            entity_type = entity['type']
            if entity_type not in type_map:
                type_map[entity_type] = []
            type_map[entity_type].append(entity)
        return type_map
    
    def _get_entity_text(self, entity: dict[str, Any]) -> str:
        synonyms = ' | '.join(entity['synonyms'])
        return ' | '.join([entity['name'], synonyms])
    
    async def _deduplication_by_type(self, entitiy_type: str, enities_by_type: list[dict[str, Any]]):
        entities_text_by_type = [self._get_entity_text(entity) for entity in enities_by_type]
        tasks = [self.llm_worker._aembed(text, self.model) for text in entities_text_by_type]
        embeddings = await tqdm.gather(*tasks, desc=f'Compute embeddings for entity type: {entitiy_type}', total=len(tasks))
        sim_matrix = cosine_similarity(embeddings)
        pairs = []
        n = len(embeddings)
        for i in range(n):
            for j in range(i + 1, n):
                score = sim_matrix[i][j]
                if score >= self.threshold:
                    pairs.append((i, j, score))


