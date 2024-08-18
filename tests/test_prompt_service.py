import pytest
from unittest.mock import mock_open, patch
from langchain_core.prompts import ChatPromptTemplate
from services.prompt import PromptService


@pytest.fixture
def mock_prompts_data():
    return {
        "generate_answer": {
            "system": "You are a helpful assistant.",
            "human": "What is the weather today?",
        }
    }


@patch("builtins.open", new_callable=mock_open)
@patch("yaml.safe_load")
def test_get_prompt_by_name(mock_safe_load, mock_open, mock_prompts_data):
    mock_safe_load.return_value = mock_prompts_data

    prompt_service = PromptService(path="dummy/path/to/prompts.yaml")
    prompt = prompt_service.get_prompt_by_name("generate_answer")

    mock_open.assert_called_once_with(
        "dummy/path/to/prompts.yaml", "r", encoding="utf-8"
    )
    mock_safe_load.assert_called_once()

    assert isinstance(prompt, ChatPromptTemplate)
    assert (
        prompt.messages[0].prompt.template
        == mock_prompts_data["generate_answer"]["system"]
    )
    assert (
        prompt.messages[1].prompt.template
        == mock_prompts_data["generate_answer"]["human"]
    )
