import faiss
import numpy as np


class FaceIndex:
    def __init__(self, faiss_index: faiss.IndexFlat, threshold: int = 170):
        self.index = faiss_index
        self.threshold = threshold

    def search_face(self, face_embedding: np.ndarray, top: int = 20) -> np.ndarray:
        D, I = self.index.search(face_embedding, top)
        num_of_found = len([d for d in D[0] if d >= self.threshold])
        return I[0][:num_of_found]
