import io

import faiss
import fitz
import numpy as np
import spacy


nlp = spacy.load("en_core_web_lg")
FAISS_INDEX_PATH = 'faiss_index/faiss_index_file.index'


def extract_text_from_pdf(pdf_file):
    text = ''
    pdf_stream = io.BytesIO(pdf_file.read())
    with fitz.open(stream=pdf_stream, filetype='pdf') as pdf:
        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)
            text += page.get_text()
    return text


def vectorize_text(text):
    doc = nlp(text)
    return doc.vector


def create_faiss_index(vectors, dimension):
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(vectors))
    faiss.write_index(index, FAISS_INDEX_PATH)
    return index


def load_faiss_index(index_path):
    try:
        return faiss.read_index(index_path)
    except Exception as e:
        print(f"Error loading FAISS index: {e}")
        return None


def get_vector_from_text(text):
    return vectorize_text(text)


def add_document_to_index(pdf_id, text):
    vector = get_vector_from_text(text)
    dimension = len(vector)

    index = load_faiss_index(FAISS_INDEX_PATH)
    if index is None:
        index = faiss.IndexFlatL2(dimension)

    vector = np.array([vector], dtype=np.float32)
    index.add(vector)
    faiss.write_index(index, FAISS_INDEX_PATH)
