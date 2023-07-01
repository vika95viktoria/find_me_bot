import numpy as np
import cv2

from face_recognition import FaceRecognitionModel


class ImageService:
    def __init__(self):
        self.face_model = FaceRecognitionModel()

    def get_face_embedding(self, img_arr):
        return np.array(self.face_model.get_faces(img_arr))

    def get_face_embedding_from_bytes(self, bytes):
        img_arr = np.asarray(bytearray(bytes), dtype="uint8")
        img_arr = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
        return self.get_face_embedding(img_arr)








