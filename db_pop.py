import chromadb
from textract import extract_from_txt, get_file_names, Document
import config


books = get_file_names(config.DATA_IN_LOCATION, ".txt")

chroma_client = chromadb.PersistentClient(path=config.DB_LOCATION)

collection = chroma_client.get_or_create_collection(name=config.DB_NAME)

for book_name in books:
    print(f"Parsing: {book_name}")
    book = Document(config.DATA_IN_LOCATION, book_name,
                    extractor=extract_from_txt)
    print(f"Adding: {book_name}")
    print(f"Book chunks: {len(book.get_book_chunks())}")
    collection.add(
        documents=book.get_book_chunks(),
        metadatas=book.get_metadata(),
        ids=book.get_ids()
        )
