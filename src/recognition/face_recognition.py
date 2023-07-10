from insightface.app import FaceAnalysis
from config import RECOGNITION_MODEL
from typing import List
import numpy as np


class FaceRecognitionModel:
    """
    Class representing wrapper for the FaceAnalysis class providing interface for pretrained insightface model
    """
    def __init__(self):
        self.app = FaceAnalysis(name=RECOGNITION_MODEL, providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
        self.app.prepare(ctx_id=0)

    def get_faces(self, img_arr: np.ndarray) -> List[np.ndarray]:
        """
        Get face embeddings from the photo

        Obtain face embeddings of all people present on the photo using pretrained insightface model.
        :param img_arr: array representing image object
        :return: list of arrays representing face embeddings of all people from the image
        """
        emb_res = self.app.get(img_arr)
        return [face.embedding for face in emb_res]


