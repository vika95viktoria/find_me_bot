import cv2
import pytest

from config import TESTS_FOLDER
from services.image_service import ImageService

image_service = ImageService()


@pytest.mark.parametrize("image_name,num_of_faces", [("no_face.jpg", 0), ("one_face.jpg", 1),
                                                     ("three_faces.jpg", 3)])
def test_get_face_embeddings(image_name, num_of_faces):
    img_arr = cv2.imread(f'{TESTS_FOLDER}/data/{image_name}')
    face_embeddings = image_service.get_face_embeddings(img_arr)
    assert len(face_embeddings) == num_of_faces


@pytest.mark.parametrize("image_name,num_of_faces", [("no_face.jpg", 0), ("one_face.jpg", 1),
                                                     ("three_faces.jpg", 3)])
def test_get_face_embeddings_from_bytes(image_name, num_of_faces):
    with open(TESTS_FOLDER / f'data/{image_name}', 'rb') as byte_file:
        byte_image = byte_file.read()
    face_embeddings = image_service.get_face_embeddings_from_bytes(byte_image)
    assert len(face_embeddings) == num_of_faces
