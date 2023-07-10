import cv2
import numpy as np

from recognition.face_recognition import FaceRecognitionModel


class ImageService:
    """
    Class representing wrapper for FaceRecognitionModel
    """
    def __init__(self):
        self.face_model = FaceRecognitionModel()

    def get_face_embeddings(self, img_arr: np.ndarray) -> np.ndarray:
        """
        Get face embeddings as numpy array
        :param img_arr: array representing image to get face embeddings from
        :return: array of face embeddings
        """
        return np.array(self.face_model.get_faces(img_arr))

    def get_face_embeddings_from_bytes(self, img_bytes: bytes) -> np.ndarray:
        """
        Get face embeddings from bytes object

        Read image object from bytes using OpenCV and get face embeddings from it
        :param img_bytes: image as bytes
        :return: array of face embeddings
        """
        img_arr = np.asarray(bytearray(img_bytes), dtype="uint8")
        img_arr = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
        return self.get_face_embeddings(img_arr)








