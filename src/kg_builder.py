from pathlib import Path
from kg_gen import KGGen

class KGBuilder:
    def __init__(self) -> None:
        self.kg = KGGen(model='deepseek/deepseek-v4-flash', temperature=0.0, 
                        api_key='sk-597c9d9a7ff143c386ba73a75605ea90', api_base='https://api.deepseek.com')
    def build(self, src_dir: Path, dst_dir: Path):
        graph = self.kg.generate(model='deepseek/deepseek-v4-pro', input_data=src_dir.read_text(), output_folder=dst_dir, \
                                 context='Моделирование тектонических нарушений с применением связей конечной жёсткости с интеграцией в CAE Fidesys', \
                                 cluster=True)
        KGGen.visualize(graph, output_path=dst_dir / 'graph_viz.html', open_in_browser=True)

