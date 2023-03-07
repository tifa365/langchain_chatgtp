"""Load html from files, clean up, split, ingest into Weaviate."""
import pickle

from langchain.document_loaders import ReadTheDocsLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.document_loaders import DirectoryLoader

# This code will create a DirectoryLoader object and use it to load all HTML files from the specified path.
# The glob parameter is used to control which files to load. In this case, we’re using it to only load 
# files with the .html extension. 
path = './docs.wordliner.com'
loader = DirectoryLoader(path, glob='**/*.html')
docs = loader.load()

# Print the conent of the documents
print(f'Loaded {len(docs)} documents')


# loader = UnstructuredFileLoader("./jungeimmobilieerzgebirge.WordPress.2023-03-06.xml")

# docs = loader.load()

# docs[0].page_content[:400]

loader = UnstructuredHTMLLoader("docs.wordliner.com/index.html")

data = loader.load()
data

"""Get documents from web pages."""
# Create an instance of the ReadTheDocsLoader class with the specified URL
loader = ReadTheDocsLoader("docs.wordliner.com/")

# Load raw documents from the specified URL using the loader instance
raw_documents = loader.load()

# Create an instance of the RecursiveCharacterTextSplitter class with specified chunk size and overlap
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
)

# Split raw documents into smaller chunks using the text_splitter instance
documents = text_splitter.split_documents(raw_documents)

# Create an instance of the OpenAIEmbeddings class to generate embeddings for documents
embeddings = OpenAIEmbeddings()
# Create a FAISS vectorstore from documents and embeddings using the from_documents method
vectorstore = FAISS.from_documents(documents, embeddings)

# Save vectorstore to a file using pickle.dump()
with open("vectorstore.pkl", "wb") as f:
    pickle.dump(vectorstore, f)


# def ingest_docs():
#     """Get documents from web pages."""
#     # Create an instance of the ReadTheDocsLoader class with the specified URL
#     loader = ReadTheDocsLoader("docs.wordliner.com/kunden/wordliner-docs-kunden/")
#     # Load raw documents from the specified URL using the loader instance
#     raw_documents = loader.load()
#     # Create an instance of the RecursiveCharacterTextSplitter class with specified chunk size and overlap
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=200,
#     )
#     # Split raw documents into smaller chunks using the text_splitter instance
#     documents = text_splitter.split_documents(raw_documents)
#     # Create an instance of the OpenAIEmbeddings class to generate embeddings for documents
#     embeddings = OpenAIEmbeddings()
#     # Create a FAISS vectorstore from documents and embeddings using the from_documents method
#     vectorstore = FAISS.from_documents(documents, embeddings)

#     # Save vectorstore to a file using pickle.dump()
#     with open("vectorstore.pkl", "wb") as f:
#         pickle.dump(vectorstore, f)


if __name__ == "__main__":
    ingest_docs()