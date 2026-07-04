import asyncio
from pipeline import Pipeline

src_dir = '/Users/dolor.src/code/Nornikel-AI-Science-Hack/test_data/'
dst_dir = '/Users/dolor.src/code/Nornikel-AI-Science-Hack/logs/'
pipe = Pipeline()
asyncio.run(pipe.process(src_dir, dst_dir))