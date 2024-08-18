from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import HumanMessage
import yaml


class PromptService:
    def __init__(self, path: str = "./prompts.yaml"):
        self.path = path

    def get_prompt_by_name(self, name: str) -> ChatPromptTemplate:
        with open(self.path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        prompt_template = data[name]

        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(prompt_template["system"]),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template(prompt_template["human"]),
            ]
        )

    def get_prompt_template_with_image(
        self,
        query: str,
        base64_image: str,
        ext: str = "png",
    ) -> ChatPromptTemplate:
        messages = [HumanMessage(content="")]

        contents = [{"type": "text", "text": query}]
        content = {
            "type": "image_url",
            "image_url": {"url": f"data:image/{ext};base64,{base64_image}"},
        }
        contents.append(content)

        messages[-1].content = contents
        return ChatPromptTemplate.from_messages(messages)
