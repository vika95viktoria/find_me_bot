from unittest import TestCase
from unittest.mock import patch
from services.image_service import ImageService

import numpy as np


class ImageServiceTestCase(TestCase):

    def setUp(self) -> None:
        self.face_model_patcher = patch('services.image_service.FaceRecognitionModel')
        self.mock_face_model = self.face_model_patcher.start()
        self.image_service = ImageService()

    def test_get_face_embedding(self):
        image = np.zeros((100, 200))
        result = self.image_service.get_face_embeddings(image)
        self.mock_face_model().get_faces.assert_called_with(image)
        self.assertIs(type(result), np.ndarray)

    @patch("services.image_service.np")
    @patch("services.image_service.cv2")
    def test_get_face_embedding_from_bytes(self, mock_cv2, mock_np):
        img_byte_array = bytes(100)
        self.image_service.get_face_embeddings_from_bytes(img_byte_array)
        mock_np.asarray.assert_called_with(bytearray(img_byte_array), dtype="uint8")
        img_arr = mock_np.asarray()
        mock_cv2.imdecode.assert_called_with(img_arr, mock_cv2.IMREAD_COLOR)
        img_arr = mock_cv2.imdecode()
        self.mock_face_model().get_faces.assert_called_with(img_arr)

    def tearDown(self):
        self.face_model_patcher.stop()
