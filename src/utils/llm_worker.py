import os
import asyncio
from typing import Any, Optional
import openai
from dotenv import load_dotenv


class LLMWokrer:
    def __init__(self, llm_batch: int = 20, embedding_batch: int = 20):
        self._llm_semaphore = asyncio.Semaphore(llm_batch)
        self._embedding_semaphore = asyncio.Semaphore(embedding_batch)
        load_dotenv()
        self._folder_id = os.environ.get('FOLDER_ID')
        self._client = openai.AsyncOpenAI(
            api_key=os.environ.get('API_KEY'),
            project=self._folder_id,
            base_url='https://ai.api.cloud.yandex.net/v1'
        )

    async def _ainvoke(self, 
            system_prompt: str, 
            user_prompt: str,
            model: str, 
            max_tokens: Optional[int] = None,
            temperature: float=0.0, 
            stream: bool= False,
            response_format: dict[str, Any] = None,
        ) -> Any:
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt},
        ]
        async with self._llm_semaphore:
            response = await self._client.chat.completions.create(
                model=f'gpt://{self._folder_id}/{model}',
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=stream,
                response_format=response_format if response_format else {"type": "text"},
            )
            return response.choices[0].message.content
    
    async def _aembed(self, text: str, model: str) -> list[float]:
        async with self._embedding_semaphore:
            response = await self._client.embeddings.create(
                input=text, 
                model=f'emb://{self._folder_id}/{model}', 
                encoding_format='float'
            )
            return response.data[0].embedding


        


        