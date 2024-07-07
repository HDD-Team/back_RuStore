import csv
import os.path

from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.document_loaders import CSVLoader
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma


name="faiss_try1"
data = r"link1 - Sheet1.csv"
embeddings_model = HuggingFaceEmbeddings(model_name="cointegrated/rubert-tiny2")
columns_to_embed = ["title","link"]
columns_to_metadata = ["category"]

def convertizaor(data):
    docs = []
    with open(data, newline="", encoding='utf-8-sig') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for i, row in enumerate(csv_reader):
            to_metadata = {col: row[col] for col in columns_to_metadata if col in row}
            values_to_embed = {k: row[k] for k in columns_to_embed if k in row}
            to_embed = "\n".join(f"{k.strip()}: {v.strip()}" for k, v in values_to_embed.items())
            newDoc = Document(page_content=to_embed, metadata=to_metadata)
            docs.append(newDoc)
    splitter = CharacterTextSplitter(separator = "\n",
                                    chunk_size=250,
                                    chunk_overlap=0,
                                    length_function=len)
    documents = splitter.split_documents(docs)
    return documents


def vectorstore():
    if not os.path.exists(f"./{name}"):
        loader = CSVLoader(data, encoding="utf-8")
        documents = loader.load()
        vectorstore = FAISS.from_documents(convertizaor(data),embeddings_model)
        vectorstore.save_local(name)
    return name,embeddings_model
vectorstore()



