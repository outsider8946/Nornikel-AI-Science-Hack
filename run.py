from src.parser import Parser
from src.kg_builder import KGBuilder
from pathlib import Path

#parser = Parser()
builder = KGBuilder()

# src_dir = Path('./test_data')
# dst_dir = Path('./logs/parsed_output')
# parser.process(src_dir, dst_dir)
kg_src_dir = Path('./logs/parsed_output/1 Моделирование тектонических нарушений с применением связей конечной жёсткости с интеграцией в CAE Fidesys (002)_parsed.md')
kg_dst_dir = Path('./logs/kg_output/')
builder.build(kg_src_dir, kg_dst_dir)