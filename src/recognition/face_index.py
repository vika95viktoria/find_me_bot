import faiss
import numpy as np


class FaceIndex:
    """
    Class representing wrapper for the Faiss IndexFlat
    """
    def __init__(self, faiss_index: faiss.IndexFlat, threshold: int = 170):
        self.index = faiss_index
        self.threshold = threshold

    def search_face(self, face_embedding: np.ndarray, top: int = 20) -> np.ndarray:
        """
        Find the photos with the face in the index

        Perform nearest neighbour search in Faiss index to indentify the photos containing vectors close
        to face_embedding vector. Number of nearest neighbours can be equal or less than top, cause additional filtering
        by threshold is performed. Vectors with similarity metric between itself and face_embedding lower than threshold
        are disregarded.

        :param face_embedding: numpy array representing face_embedding
        :param top: number of nearest neighbours we are looking for
        :return: array of indexes of top nearest neighbours(vectors in faiss index)
        """
        D, I = self.index.search(face_embedding, top)
        num_of_found = len([d for d in D[0] if d >= self.threshold])
        return I[0][:num_of_found]
