from vertexai.generative_models import (
    Content,
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Part,
    Tool
)
import google.generativeai as genai
import os
import json
import vertexai
from vertexai.language_models import TextEmbeddingModel
from google.oauth2 import service_account

os.environ["GOOGLE_API_KEY"] = "AIzaSyBFOkj3Cla3JGGYS1xDTEF6Uol3Mv-Jugc"

from langchain_google_genai import GoogleGenerativeAIEmbeddings

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

total_docs= []

from langchain_community.document_loaders import PyPDFLoader
import os


folder_path = 'books'  # Replace with the actual folder path

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        # Process the file
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()
        total_docs.extend(pages)
        
print (len(pages))

from langchain_community.vectorstores import Chroma
from chromadb.config import Settings
import os

ROOT_DIRECTORY = os.path.dirname(os.path.realpath('__file__'))

CHROMA_SETTINGS = Settings(
    anonymized_telemetry=False,
    is_persistent=True,
)

db = Chroma.from_documents(pages, 
                           embeddings, 
                           collection_metadata={'hnsw:space': 'cosine'},
                           persist_directory = f"{ROOT_DIRECTORY}/DB1")