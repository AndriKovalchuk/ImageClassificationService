import faiss

index = faiss.read_index("faiss_index_file.index")

print(f"Number of vectors in the index: {index.ntotal}")
print(f"Dimension of vectors: {index.d}")
