import faiss

class FaceIndex:
    def __init__(self, faiss_index: faiss.IndexFlat, threshold=170):
        self.index = faiss_index
        self.threshold = threshold

    def search_face(self, face_embedding, top=20):
        D, I = self.index.search(face_embedding, top)
        num_of_found = len([d for d in D[0] if d >= self.threshold])
        return I[0][:num_of_found]

