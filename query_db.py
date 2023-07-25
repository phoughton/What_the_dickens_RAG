import chromadb
import json
from chromadb.config import Settings
import config


chroma_client = chromadb.Client(
    Settings(
        chroma_db_impl=config.DB_IMPL,
        persist_directory=config.DB_LOCATION
    ))

collection = chroma_client.get_collection(name=config.DB_NAME)

results = collection.query(
    query_texts=["guilty or innocent"],
    n_results=2
)

print(json.dumps(results, indent=4))
