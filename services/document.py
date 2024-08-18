import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class DocumentService:
    def __init__(
        self, path: str = "./documents", cache_file: str = "./cached_files.txt"
    ):
        self.path = path
        self.cache_file = cache_file

        if not os.path.exists(self.cache_file):
            with open(self.cache_file, "w") as file:
                pass

        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def load_document(self, file_name: str) -> list[Document]:
        file_full_path = f"{self.path}/{file_name}"

        if file_name.endswith(".txt"):
            loader = TextLoader(file_full_path)
        elif file_name.endswith(".pdf"):
            loader = PyPDFLoader(file_full_path)
        else:
            raise ValueError(f"Unsupported file type: {file_name}")

        documents = loader.load()
        return documents

    def get_full_content(self, documents: list[Document]) -> str:
        return "".join([document.page_content for document in documents])

    def split_documents(self, documents: list[Document]) -> list[Document]:
        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=500,
            chunk_overlap=100,
            encoding_name="cl100k_base",
        )
        return splitter.split_documents(documents)

    def get_file_names(self) -> list[str]:
        try:
            files = os.listdir(self.path)
            file_names = [
                f for f in files if os.path.isfile(os.path.join(self.path, f))
            ]
            return file_names
        except FileNotFoundError:
            return f"The path '{self.path}' does not exist."
        except Exception as e:
            return str(e)

    def get_cached_documents(self) -> list[str]:
        try:
            with open(self.cache_file, "r", encoding="utf-8") as file:
                lines = file.readlines()
                lines = [line.strip() for line in lines]
            return lines
        except FileNotFoundError:
            return f"The file '{self.cache_file}' does not exist."
        except Exception as e:
            return str(e)

    def cache_document(self, file_name: str) -> None:
        with open(self.cache_file, "a", encoding="utf-8") as file:
            file.write(f"{file_name}\n")
