import os
from langchain_openai import ChatOpenAI
from const import LLMModel


class LLMServices:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

    def get_llm(
        self, model_name: str = LLMModel.GPT4_O_MINI.value, streaming: bool = False
    ) -> ChatOpenAI:
        return ChatOpenAI(
            temperature=0.0,
            openai_api_key=self.openai_api_key,
            model_name=model_name,
            streaming=streaming,
        )
