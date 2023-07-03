from insightface.app import FaceAnalysis
from config import RECOGNITION_MODEL
from typing import List
import numpy as np


class FaceRecognitionModel:
    def __init__(self):
        self.app = FaceAnalysis(name=RECOGNITION_MODEL, providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
        self.app.prepare(ctx_id=0)

    def get_faces(self, img_arr: np.ndarray) -> List[np.ndarray]:
        emb_res = self.app.get(img_arr)
        return [face.embedding for face in emb_res]


