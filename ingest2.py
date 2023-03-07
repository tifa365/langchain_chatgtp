"""Load html from files, clean up, split, ingest into Weaviate."""
import pickle
import json
from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from typing import List


class QuartoLoader(BaseLoader):
    """Load Quarto search.json files."""

    def __init__(self, file_path: str):
        """Initialize with file path."""
        # Set the file path attribute to the specified value
        self.file_path = file_path

    def load(self) -> List[Document]:
        """Load json from file path."""
        # Open the specified file and read its contents as a string
        with open(self.file_path) as f:
            index = json.loads(f.read())
        
        # Create an empty list to store documents
        docs = []
        # Iterate over each document in the index and extract relevant metadata and text content
        for doc in index:
            metadata = {k: doc[k] for k in ("objectID", "href", "section")}
            docs.append(Document(page_content=doc["text"], metadata=metadata))
        # Return the list of documents
        return docs


def ingest_docs():
    """Get documents from web pages."""
    # Create an instance of the QuartoLoader class with the specified file path
    loader = QuartoLoader("search.json")
    # Load raw documents from the specified file using the loader instance
    raw_documents = loader.load()
    # Create an instance of the RecursiveCharacterTextSplitter class with specified chunk size and overlap
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    # Split raw documents into smaller chunks using the text_splitter instance
    documents = text_splitter.split_documents(raw_documents)
    # Create an instance of the OpenAIEmbeddings class to generate embeddings for documents
    embeddings = OpenAIEmbeddings()
    # Create a FAISS vectorstore from documents and embeddings using the from_documents method
        vectorstore = FAISS.from_documents(documents, embeddings)
    # Return the vectorstore
    return vectorstore


if __name__ == "__main__":
    # Call the ingest_docs function if this script is run directly
    ingest_docs()