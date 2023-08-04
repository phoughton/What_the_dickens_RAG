import chromadb
from textract import extract_from_txt, read_all_files
import config


books = read_all_files("data_in/charles_dickens/",
                       ".txt",
                       extract_from_txt)

chroma_client = chromadb.PersistentClient(path=config.DB_LOCATION)


collection = chroma_client.create_collection(name=config.DB_NAME)

for book in books:
    print(book)

    collection.add(
        documents=book.get_book_chunks(),
        metadatas=book.get_metadata(),
        ids=book.get_ids()
        )
