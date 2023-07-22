import chromadb
import PyPDF2
import os
import json
from chromadb.config import Settings


def extract_text_from_pdf(file_path: str, pdf_file_name: str) -> list:
    pdf_file_obj = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
    text = []

    for num, page in enumerate(pdf_reader.pages):
        text.append({"id": f"{pdf_file_name}: page {num + 1}",
                    "piece_of_text": page.extract_text()})

    pdf_file_obj.close()

    return text


def extract_text_from_txt_file(file_path: str, txt_file_name: str) -> list:
    txt_file_obj = open(file_path, 'r')
    text = []

    # split file into paragraphs
    paragraphs = txt_file_obj.read().split("\n\n")

    for num, paragraph in enumerate(paragraphs):
        text.append({"id": f"{txt_file_name}: paragraph {num + 1}",
                    "piece_of_text": paragraph})

    txt_file_obj.close()

    return text


def read_all_files(folder_path: str, 
                   file_extension: str, 
                   extract_func) -> list:

    files = os.listdir(folder_path)
    books_n_text = []

    for file_name in files:
        if file_name.endswith(file_extension):
            print(file_name)
            file_path = os.path.join(folder_path, file_name)
            text = extract_func(file_path, file_name)
            books_n_text += (text)

    return books_n_text


books_and_text = read_all_files("data_in/bank_of_england",
                                ".pdf", 
                                extract_text_from_pdf)
books_and_text += read_all_files("data_in/charles_dickens",
                                 ".txt", 
                                 extract_text_from_txt_file)

ids = []
for text_chunk_details in books_and_text:
    ids.append(text_chunk_details["id"])

document_pieces = []
for text_chunk_details in books_and_text:
    document_pieces.append(text_chunk_details["piece_of_text"])

print()

chroma_client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="data_store/vector_db"))

collection = chroma_client.create_collection(name="book_collection")

with open("data_store/books_and_text.json", "w") as f:
    json.dump(books_and_text, f, indent=4)

book_names_metadata = []
for id in ids:
    book_names_metadata.append({id.split(":")[0]: id.split(":")[1]})

for counter in range(0, len(book_names_metadata)):
    print(ids[counter])
    collection.add(
        documents=document_pieces[counter],
        metadatas=book_names_metadata[counter],
        ids=ids[counter]
        )

results = collection.query(
    query_texts=["guilty", "innocent"],
    n_results=2
)


print(json.dumps(results, indent=4))
