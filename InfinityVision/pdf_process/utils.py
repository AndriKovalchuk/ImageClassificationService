import io
import pathlib

import docx
import faiss
import fitz  # PyMuPDF
import numpy as np
import spacy

nlp = spacy.load("en_core_web_lg")  # повертає вектор довжиною - 300

FAISS_INDEX_PATH = 'faiss_index/faiss_index_file.index'


def extract_text_from_document(document):
    text = ''
    file_extension = pathlib.Path(document.name).suffix.lower().replace('.', '')

    if file_extension == 'pdf':
        pdf_stream = io.BytesIO(document.read())
        with fitz.open(stream=pdf_stream, filetype='pdf') as pdf:
            for page_num in range(len(pdf)):
                page = pdf.load_page(page_num)
                text += page.get_text()

    elif file_extension == 'docx':
        doc = docx.Document(document)
        for para in doc.paragraphs:
            text += para.text + '\n'

    elif file_extension == 'txt':
        text = document.read().decode('utf-8')

    else:
        raise ValueError("Unsupported file type")

    return text


def add_document_to_index(pdf_id, text):
    vector = get_vector_from_text(text)  # перетворюємо текст на вектор, розмірністю 300
    dimension = len(vector)
    print(dimension)

    # завантажуємо існуючий index або створюємо новий, якщо не існує
    index = load_faiss_index(FAISS_INDEX_PATH)
    if index is None:
        index = faiss.IndexFlatL2(
            dimension)  # створюємо новий індекс FAISS типу IndexFlatL2 (метрика євклідову відстань для пошуку найближчих сусідів) + розмірність

    vector = np.array([vector], dtype=np.float32)  # перетворюємо вектор у формат масиву numpy

    index.add(vector)
    faiss.write_index(index, FAISS_INDEX_PATH)  # зберігаємо index у файл


def get_vector_from_text(text):
    doc = nlp(text)
    print(doc.vector)
    return doc.vector


def load_faiss_index(index_path):
    try:
        return faiss.read_index(index_path)
    except Exception as e:
        print(f"Error loading FAISS index: {e}")
        return None
