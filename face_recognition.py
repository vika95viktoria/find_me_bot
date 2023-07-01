from insightface.app import FaceAnalysis


class FaceRecognitionModel:
    def __init__(self):
        self.app = FaceAnalysis(name="buffalo_l", providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
        self.app.prepare(ctx_id=0)

    def get_faces(self, img_arr):
        emb_res = self.app.get(img_arr)
        return [face.embedding for face in emb_res]


