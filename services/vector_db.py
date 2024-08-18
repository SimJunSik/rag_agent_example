from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from unicodedata import normalize

from services.document import DocumentService
import os


class VectorDBService:
    def __init__(
        self,
        embedding_model: Embeddings = None,
        persist_directory: str = "./db/vector/",
    ):
        self.embedding_model = (
            embedding_model
            if embedding_model
            else OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        )
        self.persist_directory = persist_directory
        self.document_service = DocumentService()

        if not os.path.exists(self.persist_directory):
            os.makedirs(self.persist_directory)

    def persist(self, splited_documents: list[Document]) -> None:
        texts = [document.page_content for document in splited_documents]
        vector_db = Chroma.from_texts(
            texts=texts,
            embedding=self.embedding_model,
            persist_directory=self.persist_directory,
        )
        vector_db.persist()

    def embed_document(self, file_name: str) -> None:
        cached_files = self.document_service.get_cached_documents()

        normalized_file_name = normalize("NFC", file_name)
        print(normalized_file_name, end="/ ")
        if normalized_file_name in cached_files:
            print("Already cached")
            return

        documents = self.document_service.load_document(normalized_file_name)
        splited_documents = self.document_service.split_documents(documents)
        self.persist(splited_documents)

        self.document_service.cache_document(normalized_file_name)

    def init_vector_db(self) -> None:
        file_names = self.document_service.get_file_names()
        for file_name in file_names:
            self.embed_document(file_name)

    def get_relevent_documents(self, query: str) -> list[Document]:
        vector_db = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_model,
        )

        retriever = vector_db.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 5, "fetch_k": 50},
        )

        return retriever.get_relevant_documents(query)
