from typing import Callable, List, Tuple
import PyPDF2


class Document:
    """Document class for storing book information and extracting text from it."""

    ids = []
    book_chunks = []
    name = ""

    def __init__(self, file_path: str,
                 file_name: str,
                 extractor: Callable) -> None:

        self.ids, self.book_chunks = extractor(file_path, file_name)
        self.name = file_name.split(".")[0]

    def __str__(self) -> str:
        return f"Document: {self.name}"

    def __repr__(self) -> str:
        self.__str__()

    def get_book_chunks(self) -> list:
        return self.book_chunks

    def get_ids(self) -> list:
        return self.ids


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

    for num, paragraph in enumerate(paragraphs):
        chunks.append(paragraph)
        ids.append(f"{file_name}: paragraph {num + 1}")

    txt_file_obj.close()

    return ids, chunks
