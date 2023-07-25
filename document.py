from typing import Callable, List, Tuple
import PyPDF2
import os


class Document:
    """Document class for storing book information and extracting text from it."""

    def __init__(self, file_path: str,
                 file_name: str,
                 extractor: Callable) -> None:

        self.ids = []
        self.book_chunks = []
        self.name = ""
        self.metadata_dicts = []

        self.ids, self.book_chunks = extractor(file_path, file_name)
        self.name = file_name.split(".")[0]
        for id in self.ids:
            self.metadata_dicts.append({self.name: id})

    def __str__(self) -> str:
        return f"Document: {self.name}"

    def __repr__(self) -> str:
        self.__str__()

    def get_book_chunks(self) -> list:
        return self.book_chunks

    def get_ids(self) -> list:
        return self.ids
    
    def get_metadata(self) -> list:
        return self.metadata_dicts


def extract_from_pdf(file_path: str, file_name: str) -> list:
    pdf_file_obj = open(file_path+file_name, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
    ids = []
    chunks = []

    for num, page in enumerate(pdf_reader.pages):
        chunks.append(page.extract_text())
        ids.append(f"{file_name}: page {num + 1}"),

    pdf_file_obj.close()

    return ids, chunks


def extract_from_txt(file_path: str,
                     file_name: str) -> Tuple[List[str], List[str]]:

    txt_file_obj = open(file_path+file_name, 'r')
    ids = []
    chunks = []

    paragraphs = txt_file_obj.read().split("\n\n")

    current_chunk = ""
    current_chunk_id = ""
    for num, paragraph in enumerate(paragraphs):
        if len(current_chunk) + len(paragraph) > 4000:
            chunks.append(current_chunk)
            ids.append(current_chunk_id)
            current_chunk = ""
            current_chunk_id = ""
        current_chunk += paragraph + "\n\n"
        current_chunk_id += f"{file_name}: paragraph {num + 1}, "

    if current_chunk:
        chunks.append(current_chunk)
        ids.append(current_chunk_id)

    txt_file_obj.close()

    return ids, chunks


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