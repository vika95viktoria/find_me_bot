from unittest import TestCase
from unittest.mock import Mock

import numpy as np

from index.face_index import FaceIndex


class FaceIndexTestCase(TestCase):
    def setUp(self) -> None:
        self.mock_faiss_index = Mock()
        self.distance_threshold = 100
        self.face_index = FaceIndex(self.mock_faiss_index, self.distance_threshold)

    def test_get_faces(self):
        face_embedding = np.ones((100, 100))
        distance = [200, 150, 101, 100, 90, 20, 10]
        indexes = [0, 1, 2, 3, 4, 6, 7]
        self.mock_faiss_index.search.return_value = [distance], [indexes]
        result = self.face_index.search_face(face_embedding, 10)
        self.mock_faiss_index.search.assert_called_with(face_embedding, 10)
        self.assertEqual(len([x for x in distance if x <= self.distance_threshold]), len(result))
