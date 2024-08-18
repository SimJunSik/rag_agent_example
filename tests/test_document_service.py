import pytest
from unittest.mock import mock_open, patch
from langchain_core.documents import Document

from services.document import DocumentService


@pytest.fixture
def mock_documents():
    return [Document(page_content="This is a test document.")]


@pytest.fixture
def document_service():
    return DocumentService(
        path="./test_documents", cache_file="./test_cached_files.txt"
    )


@patch("os.listdir")
@patch("os.path.isfile")
def test_get_file_names(mock_isfile, mock_listdir, document_service):
    mock_listdir.return_value = ["file1.txt", "file2.pdf", "file3.docx"]
    mock_isfile.side_effect = lambda path: not path.endswith(".docx")

    file_names = document_service.get_file_names()

    assert file_names == ["file1.txt", "file2.pdf"]
    mock_listdir.assert_called_once_with("./test_documents")


@patch("builtins.open", new_callable=mock_open, read_data="file1.txt\nfile2.pdf\n")
def test_get_cached_documents(mock_open, document_service):
    cached_files = document_service.get_cached_documents()

    assert cached_files == ["file1.txt", "file2.pdf"]
    mock_open.assert_called_once_with("./test_cached_files.txt", "r", encoding="utf-8")
