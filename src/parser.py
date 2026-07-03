from docling.document_converter import DocumentConverter
from tqdm import tqdm
from pathlib import Path
from docling.datamodel.base_models import InputFormat

from loguru import logger

class Parser:
    def __init__(self):
        self.converter = DocumentConverter(allowed_formats=[InputFormat.PDF, InputFormat.DOCX, InputFormat.PPTX])
        logger.info("Docling parser initialized")
    
    def postprocessing(self, text: str) -> str:
        clear_text = []
        for line in text.split('\n'):
            if 'Рисунок' in line or '<!-- image -->' in line:
                continue
            clear_text.append(line)

        return '\n'.join(clear_text)
    
    def process(self, src_dir: Path, dst_dir: Path) -> None:
        if not src_dir.exists():
            logger.error(f"Source directory {src_dir} does not exist.")
            return
        
        dst_dir.mkdir(parents=True, exist_ok=True)

        for file_path in tqdm(src_dir.iterdir(), desc="Processing files"):
            if file_path.suffix.lower() in {".pdf", ".docx"}:
                raw = self.converter.convert(file_path).document.export_to_markdown()
                result = self.postprocessing(raw)                
            else:
                logger.warning(f"Unsupported file format: {file_path.suffix}")
                continue
            
            with open(dst_dir / (file_path.stem + "_parsed.md"), "w", encoding="utf-8") as f:
                f.write(result)