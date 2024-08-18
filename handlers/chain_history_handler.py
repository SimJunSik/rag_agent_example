from typing import Any, Union
from uuid import UUID

from langchain_core.messages import BaseMessage
from langchain_core.outputs import LLMResult
from langchain_core.callbacks import BaseCallbackHandler

from services.db import Chat, DBService


class ChainHistoryHandler(BaseCallbackHandler):
    def __init__(self, query: str, session_id: str) -> None:
        self.query = query
        self.response = ""
        self.session_id = session_id
        self.db = DBService.get_db()

    def on_chat_model_start(
        self,
        serialized: dict[str, Any],
        messages: list[list[BaseMessage]],
        *,
        run_id: UUID,
        **kwargs: Any
    ) -> Any:
        pass

    def on_llm_end(self, response: LLMResult, *, run_id: UUID, **kwargs: Any) -> None:
        self.response = response.generations[0][0].text

        chat = Chat(
            session_id=self.session_id, query=self.query, response=self.response
        )
        self.db.add(chat)
        self.db.commit()
        self.db.close()

    def on_llm_error(
        self, error: Union[Exception, KeyboardInterrupt], *, run_id: UUID, **kwargs: Any
    ) -> None:
        pass

    @property
    def ignore_retry(self) -> bool:
        return True
