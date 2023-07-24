import chromadb
import os
import json
from chromadb.config import Settings
from document import extract_from_pdf, extract_from_txt, Document


def read_all_files(file_path: str,
                   file_extension: str,
                   extract_func) -> list:

    books = []

    for file_name in os.listdir(file_path):
        if file_name.endswith(file_extension):
            books.append(Document(file_path,
                                  file_name,
                                  extractor=extract_func))

    return books


books = read_all_files("data_in/bank_of_england/",
                       ".pdf",
                       extract_from_pdf)
books += read_all_files("data_in/charles_dickens/",
                        ".txt",
                        extract_from_txt)

chroma_client = chromadb.Client(
    # Settings(
    # chroma_db_impl="duckdb+parquet",
    # persist_directory="data_store/vector_db")
    )

collection = chroma_client.create_collection(name="book_collection")

for book in books:
    print(book)

    collection.add(
        documents=book.get_book_chunks(),
        metadatas=book.get_metadata(),
        ids=book.get_ids()
        )

results = collection.query(
    query_texts=["guilty", "innocent"],
    n_results=2
)


print(json.dumps(results, indent=4))
