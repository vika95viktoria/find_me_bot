import cv2
import numpy as np
from tqdm import tqdm
import os
from google.cloud import storage

from face_recognition import FaceRecognitionModel


class ImageService:
    def __init__(self):
        self.face_model = FaceRecognitionModel()
        self.storage_client = storage.Client()

    def get_face_embedding(self, img_arr):
        return np.array(self.face_model.get_faces(img_arr))

    def read_image_from_gcp(self, blob):
        image_bytes = bytearray(blob.download_as_bytes(self.storage_client))
        img_arr = np.asarray(image_bytes, dtype="uint8")
        return cv2.imdecode(img_arr, cv2.IMREAD_COLOR)


    def process_batch_from_gcp(self, folder: str):
        bucket = self.storage_client.get_bucket('epam_photos')
        face_mapping = {}
        face_embeddings = []
        ind = 0
        for blob in tqdm(bucket.list_blobs(prefix=folder)):
            img_arr = self.read_image_from_gcp(blob)
            faces = self.face_model.get_faces(img_arr)
            for _ in faces:
                face_mapping[ind] = blob.name
                ind += 1
            face_embeddings.extend(faces)
        return face_mapping, np.array(face_embeddings)

    def process_batch_local(self, folder_name):
        face_mapping = {}
        face_embeddings = []
        ind = 0
        for dirpath, dirnames, filenames in os.walk(folder_name):
            for file_name in tqdm(filenames):
                img_arr = cv2.imread(f'{dirpath}/{file_name}')
                faces = self.face_model.get_faces(img_arr)
                for _ in faces:
                    face_mapping[ind] = f'{dirpath}/{file_name}'
                    ind += 1
                face_embeddings.extend(faces)
        return face_mapping, np.array(face_embeddings)








