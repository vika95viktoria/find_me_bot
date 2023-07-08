from unittest import TestCase
from unittest.mock import patch
from recognition.face_recognition import FaceRecognitionModel

import numpy as np


class FaceRecognitionModelTestCase(TestCase):
    def setUp(self) -> None:
        self.client_patcher = patch('recognition.face_recognition.FaceAnalysis')
        self.mock_face_model = self.client_patcher.start()
        self.face_recognition_model = FaceRecognitionModel()

    def test_get_faces(self):
        image_array = np.ones((100, 100))
        self.face_recognition_model.get_faces(image_array)
        self.mock_face_model().get.assert_called_with(image_array)

    def tearDown(self):
        self.client_patcher.stop()
