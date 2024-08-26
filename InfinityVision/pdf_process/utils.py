import io

import faiss
import fitz  # PyMuPDF
import numpy as np
import spacy

nlp = spacy.load("en_core_web_lg")  # повертає вектор довжиною - 300

FAISS_INDEX_PATH = 'faiss_index/faiss_index_file.index'


def extract_text_from_pdf(pdf_file):
    text = ''
    pdf_stream = io.BytesIO(
        pdf_file.read())  # перетворюємо байти PDF-файлу у буфер у пам'яті, що дозволяє працювати з ним як з файлом без збереження на диск
    with fitz.open(stream=pdf_stream, filetype='pdf') as pdf:
        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)
            text += page.get_text()
    return text


def add_document_to_index(pdf_id, text):
    vector = get_vector_from_text(text)  # перетворюємо текст на вектор, розмірністю 300
    dimension = len(vector)
    print(dimension)

    # завантажуємо існуючий index або створюємо новий, якщо не існує
    index = load_faiss_index(FAISS_INDEX_PATH)
    if index is None:
        index = faiss.IndexFlatL2(dimension)  # створюємо новий індекс FAISS типу IndexFlatL2 (метрика євклідову відстань для пошуку найближчих сусідів) + розмірність

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
