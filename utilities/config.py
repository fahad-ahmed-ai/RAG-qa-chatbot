import os
from dotenv import load_dotenv
import chromadb
from motor.motor_asyncio import AsyncIOMotorClient
from chromadb.config import Settings


load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")


chroma_client = chromadb.Client(
    Settings(chroma_db_impl="duckdb+parquet", persist_directory="db/")
)


client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]
