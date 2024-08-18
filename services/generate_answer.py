from operator import itemgetter
from typing import AsyncGenerator, Optional
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    Runnable,
    RunnableConfig,
    RunnablePassthrough,
    RunnableLambda,
)
from langchain.memory import ConversationBufferWindowMemory
from const import MAX_CONCURRENCY_PER_CHAIN, LLMModel
from handlers.chain_history_handler import ChainHistoryHandler
from models import ChainInput
from services.db import Chat, DBService
from services.document import DocumentService
from services.llm import LLMServices
from services.prompt import PromptService
from services.vector_db import VectorDBService


class GenerateAnswerService:
    def __init__(self):
        self.vector_db_service = VectorDBService()
        self.document_service = DocumentService()
        self.prompt_service = PromptService()
        self.llm_service = LLMServices()
        self.db = DBService.get_db()

    def init_generate_answer_chain(
        self,
        inputs: ChainInput,
        memory: ConversationBufferWindowMemory,
        model_name: str = LLMModel.GPT4_O_MINI.value,
        streaming: bool = False,
    ) -> Runnable:
        llm = self.llm_service.get_llm(model_name=model_name, streaming=streaming)

        prompt = self.prompt_service.get_prompt_by_name("generate_answer")

        return (
            {"utterance": lambda _: inputs.query, "context": lambda _: inputs.context}
            | RunnablePassthrough.assign(
                chat_history=RunnableLambda(memory.load_memory_variables)
                | itemgetter("chat_history")
            )
            | prompt
            | llm
            | StrOutputParser()
        )

    def init_generate_answer_chain_with_image(
        self,
        inputs: ChainInput,
        model_name: str = LLMModel.GPT4_O_MINI.value,
        streaming: bool = False,
    ) -> Runnable:
        llm = self.llm_service.get_llm(model_name=model_name, streaming=streaming)

        prompt = self.prompt_service.get_prompt_template_with_image(
            inputs.query, inputs.context
        )

        return prompt | llm | StrOutputParser()

    def generate_answer(self, query: str) -> str:
        relevent_documents = self.vector_db_service.get_relevent_documents(query)
        context = self.document_service.get_full_content(relevent_documents)

        inputs = ChainInput(query=query, context=context)
        chain = self.init_generate_answer_chain(inputs)

        config = RunnableConfig(
            callbacks=[ChainHistoryHandler()], max_concurrency=MAX_CONCURRENCY_PER_CHAIN
        )

        return chain.invoke({}, config)

    async def generate_answer_with_stream(
        self, query: str, session_id: str, encoded_content: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        if encoded_content:
            inputs = ChainInput(query=query, context=encoded_content)
            chain = self.init_generate_answer_chain_with_image(inputs, streaming=True)
        else:
            relevent_documents = self.vector_db_service.get_relevent_documents(query)
            context = self.document_service.get_full_content(relevent_documents)

            memory = ConversationBufferWindowMemory(
                memory_key="chat_history", return_messages=True, k=5
            )

            chats = self.db.query(Chat).filter(session_id == session_id)
            for chat in chats:
                memory.save_context({"Human": chat.query}, {"AI": chat.response})
            self.db.close()

            inputs = ChainInput(query=query, context=context)
            chain = self.init_generate_answer_chain(
                inputs, memory=memory, streaming=True
            )

        config = RunnableConfig(
            callbacks=[ChainHistoryHandler(query, session_id)],
            max_concurrency=MAX_CONCURRENCY_PER_CHAIN,
        )

        async for result in chain.astream({}, config):
            yield result
