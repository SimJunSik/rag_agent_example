from pydantic import BaseModel


class ChainInput(BaseModel):
    query: str
    context: str
