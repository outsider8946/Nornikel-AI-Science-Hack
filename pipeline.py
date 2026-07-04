from pathlib import Path
import json
from db.data_processor.parser import Parser
from typing import Any
from src.utils.enums import Models
from loguru import logger
from src.db.data_processor.extractor import Extractor
from src.db.data_loader.neo4j_builder import Neo4jBuilder
from src.db.data_processor.schemas import ExtractionResult
from src.utils.llm_worker import LLMWokrer

class Pipeline:
    def __init__(self, llm_batch: int = 20, embedding_batch: int = 20, neo4j_batch: int = 100) -> None:
        self.parser = Parser()
        llm_worker = LLMWokrer(llm_batch=llm_batch, embedding_batch=embedding_batch)
        self.extractor = Extractor(llm_worker=llm_worker)
        self.builder = Neo4jBuilder(neo4j_batch) 
    
    def prepare_data(self, extractor_dst_dir: Path) -> dict[str, Any]:
        """Загрузка JSON-файлов без преобразований"""
        flatten_data = {
            "entities": [],
            "facts": [],
            "relations": [],
            "claims": []
        }
        
        for file_path in extractor_dst_dir.iterdir():
            if not file_path.is_file() or file_path.suffix != '.json':
                continue
                
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)

            for key in flatten_data.keys():
                if key in json_data:
                    flatten_data[key].extend(json_data[key])

        
        return flatten_data
    
    async def process(self, src_dir: str, dst_dir: str, model: str = Models.LLM.DEEPSEEK_V4_FLASH.value) -> None:
        src_dir = Path(src_dir)
        dst_dir = Path(dst_dir)

        parser_dst_dir = dst_dir / 'parsed_output'
        logger.info('Processing parsing...')
        self.parser.process(src_dir=src_dir, dst_dir=parser_dst_dir)

        extractor_dst_dir = dst_dir / 'extracted_output'
        logger.info('Processing LLM extraction...')
        await self.extractor.process(src_dir=parser_dst_dir, dst_dir=extractor_dst_dir, model=model)
        data = self.prepare_data(extractor_dst_dir)
        logger.info('Processing building KG...')
        self.builder.process(data)
        logger.info('Pipeline is ended')
