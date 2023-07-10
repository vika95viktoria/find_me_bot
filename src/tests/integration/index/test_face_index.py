import pickle

import cv2
import pytest

from config import TESTS_FOLDER
from index.face_index import FaceIndex
from services.image_service import ImageService

with open(TESTS_FOLDER / 'data/test_index.pkl', 'rb') as index_file:
    faiss_index = pickle.load(index_file)

image_service = ImageService()


def get_face_embedding(image_name):
    img_arr = cv2.imread(f'{TESTS_FOLDER}/data/{image_name}')
    return image_service.get_face_embeddings(img_arr)


@pytest.mark.parametrize("image_name,num_of_photos", [("test_maria.jpg", 3), ("test_olga_2.jpg", 4),
                                                      ("test_olga.jpg", 4), ("test_serj.jpg", 11),
                                                      ("test_pavel.jpg", 1), ("test_alex.png", 1)])
def test_search_face(image_name, num_of_photos):
    face_index = FaceIndex(faiss_index)

    face_embedding = get_face_embedding(image_name)
    found_photos = face_index.search_face(face_embedding)
    assert len(found_photos) == num_of_photos


@pytest.mark.parametrize("image_name,top,num_of_photos", [("test_maria.jpg", 5, 3), ("test_maria.jpg", 2, 2),
                                                          ("test_serj.jpg", 20, 11), ("test_serj.jpg", 10, 10),
                                                          ("test_serj.jpg", 5, 5), ("test_pavel.jpg", 5, 1),
                                                          ("test_pavel.jpg", 3, 1)])
def test_search_face_restrict_top(image_name, top, num_of_photos):
    face_index = FaceIndex(faiss_index)

    face_embedding = get_face_embedding(image_name)
    found_photos = face_index.search_face(face_embedding, top)
    assert len(found_photos) == num_of_photos


@pytest.mark.parametrize("image_name,threshold,num_of_photos", [("test_maria.jpg", 200, 2), ("test_maria.jpg", 100, 20),
                                                                ("test_olga.jpg", 200, 4), ("test_olga.jpg", 100, 11),
                                                                ("test_serj.jpg", 200, 7), ("test_serj.jpg", 100, 20)])
def test_search_face_change_threshold(image_name, threshold, num_of_photos):
    face_index = FaceIndex(faiss_index, threshold)

    face_embedding = get_face_embedding(image_name)
    found_photos = face_index.search_face(face_embedding)
    assert len(found_photos) == num_of_photos
