from pathlib import Path
import json
from src.utils.llm_worker import LLMWokrer
from src.utils.enums import Models
from pydantic import BaseModel
from src.db.data_processor.schemas import ExtractionResult
from src.db.data_processor import prompts
from tqdm.asyncio import tqdm
from loguru import logger

class Extractor:
    def __init__(self, llm_worker: LLMWokrer) -> None:
        self.llm_worker = llm_worker
    
    def validate_output(self, data, model: BaseModel):
            clear_data = []
            for item in data:
                try:
                    clear_data.append(model.model_validate(item))
                except:
                    continue
            return clear_data
    
    async def _aextract(self, text: str, output_path: Path,  model: str) -> None:
        if output_path.exists():
            return 
        
        system_prompt = prompts.EXTRACTION_SYSTEM_PROMPT
        user_prompt = prompts.EXTRACTION_USER_TEMPLATE.format(chunk_text=text)
        response_format = {
            'type': 'json_schema',
            'json_schema': {
                'name': ExtractionResult.__name__,
                'schema': ExtractionResult.model_json_schema(),
                'strict': False,
            }
        }
        result =  await self.llm_worker._ainvoke(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=model,
            response_format=response_format
        )
        result_dict = json.loads(result)
        output_path.write_text(json.dumps(result_dict, indent=4, ensure_ascii=False), encoding='utf-8')

        
    async def process(self, src_dir: Path, dst_dir: Path, model: str = Models.LLM.DEEPSEEK_V4_FLASH.value) -> None:
        if not src_dir.exists():
            logger.error(f"Source directory {src_dir} does not exist.")
            return
        dst_dir.mkdir(parents=True, exist_ok=True)
        tasks = []

        for file_path in src_dir.iterdir():
                file = src_dir / file_path
                text = file.read_text()
                output_path = dst_dir / (file_path.stem + '_extracted.json')
                tasks.append(self._aextract(text, output_path=output_path, model=model))
            
        await tqdm.gather(*tasks, desc='extraction', total=len(tasks))

