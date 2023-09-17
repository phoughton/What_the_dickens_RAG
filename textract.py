from typing import Callable, List, Tuple
import PyPDF2
import os
import re
from config import MIN_SECTION_SIZE, BIG_SECTION_SIZE
from unidecode import unidecode


class Document:
    """For storing book information and extracting text from it."""

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

    # Group lines into sentences and small paragraphs into larger sections
    text_sections = tidy_paragraphs(txt_file_obj.read())

    # Remove confusing characters and image references
    cleaned_sections = remove_unwanted_chars(text_sections)

    current_chunk_id = ""
    for num, section in enumerate(cleaned_sections):
        current_chunk_id = f"{file_name.split('.')[0]}, section: {num}"
        chunks.append(section)
        ids.append(current_chunk_id)

        if len(section) > BIG_SECTION_SIZE:
            print(f"WARNING: {file_name} section {num + 1} is: {len(section)} chars long")

    txt_file_obj.close()

    for section_num, section_text in enumerate(chunks):
        with open(f"logs/{file_name}_log.txt", "a") as f:
            f.write(f"Chunk ID: {ids[section_num]}")
            f.write("\n")
            f.write(section_text)
            f.write("\n\n")

    return ids, chunks


def get_file_names(file_path: str,
                   file_extension: str) -> list:

    books = []

    for file_name in os.listdir(file_path):
        if file_name.endswith(file_extension):
            books.append(file_name)

    return books


def tidy_paragraphs(text: str) -> list:
    paragraphs = text.strip().split('\n\n')

    sections = [' '.join(para.split('\n')) for para in paragraphs]

    return group_chunks_into_bigger_chunks(sections, MIN_SECTION_SIZE)


def remove_unwanted_chars(list_of_texts: list) -> list:

    cleaned_texts = []

    for text in list_of_texts:
        no_whitespace = re.sub(r'\s+', ' ', text)

        no_quotes = no_whitespace.replace('\u2019', "'").replace('\u2018', "'") \
            .replace('\u201c', "'").replace('\u201d', "'")

        cleaned_texts.append(re.sub(r'\[Illustration\]', ' ', no_quotes))

    return cleaned_texts


def group_chunks_into_bigger_chunks(chunks: list,
                                    chunk_size: int) -> list:

    grouped_chunks = []
    current_chunk = ""

    for chunk in chunks:
        chunk = unidecode(chunk.strip())
        if len(current_chunk) + len(chunk) < chunk_size:
            current_chunk += f" {chunk}"
        else:
            grouped_chunks.append(current_chunk)
            current_chunk = chunk

    return grouped_chunks
