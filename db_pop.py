import chromadb
import PyPDF2
import os
import json


def extract_text_from_pdf(file_path: str, pdf_file_name: str) -> list:
    pdf_file_obj = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
    text = []

    for num, page in enumerate(pdf_reader.pages):
        text.append({"source": {pdf_file_name: f"page {num + 1}"},
                    "page_of_text": page.extract_text()})

    pdf_file_obj.close()

    return text


def read_all_pdfs(pdf_folder: str) -> list:
    pdf_files = os.listdir(pdf_folder)
    books_n_text = []

    for pdf_file in pdf_files:
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            text = extract_text_from_pdf(pdf_path, pdf_file)
            books_n_text += (text)

    return books_n_text


books_and_text = read_all_pdfs("data/")

metadata_sources = []
for page in books_and_text:
    metadata_sources.append(page["source"])

document_pages = []
for page in books_and_text:
    document_pages.append(page["page_of_text"])

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="test_collection")

collection.add(
    documents=document_pages,
    metadatas=metadata_sources,
    ids=[f"id{i+1}" for i in range(len(document_pages))]
    )

results = collection.query(
    query_texts=["money flow"],
    n_results=2
)


print(json.dumps(results, indent=4))