from enum import Enum

class Models:
    class LLM(Enum):
        ALICE = "aliceai-llm"
        ALICE_FLASH = "aliceai-llm-flash"
        YAGPT_PRO_5_1 = "yandexgpt-5.1"
        YAGPT_PRO_5 = "yandexgpt-5-pro"
        YAGPT_LITE_5 = "yandexgpt-5-lite"
        DEEPSEEK_V4_FLASH = "deepseek-v4-flash"
        QWEN_3_235 = "qwen3-235b-a22b-fp8"
        GPT_OSS_120 = "gpt-oss-120b"
        GPT_OSS_20 = "gpt-oss-20b"
        QWEN_3_6_35 = "qwen3.6-35b-a3b"
        
    class Embeddings(Enum):
        YAEMB_DOC_V1 = "text-search-doc/latest"
        YAEMB_QUERY_V1 = "text-search-query/latest"