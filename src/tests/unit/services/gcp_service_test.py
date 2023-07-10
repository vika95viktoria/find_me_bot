from unittest import TestCase
from unittest.mock import patch

from services.gcp_service import GCPStorageService


class GCPStorageServiceTestCase(TestCase):

    def setUp(self) -> None:
        self.client_patcher = patch('services.gcp_service.storage.Client')
        self.mock_client = self.client_patcher.start()
        self.gcp_service = GCPStorageService('bucket_name')
        self.blob_name = 'blob'
        self.file_name = 'test_file'

    def test_upload_to_bucket(self):
        self.gcp_service.upload_to_bucket(self.blob_name, self.file_name)

        blob = self.gcp_service.bucket.blob
        blob.assert_called_with(self.blob_name)
        blob().upload_from_filename.assert_called_with(self.file_name)

    def test_download_as_bytes(self):
        blob = self.gcp_service.bucket.blob
        self.gcp_service.download_as_bytes(self.file_name)

        blob.assert_called_with(self.file_name)
        blob().download_as_bytes.assert_called_with(self.mock_client())

    @patch("services.gcp_service.pickle")
    def test_read_pickle(self, mock_pickle):
        blob = self.gcp_service.bucket.blob
        self.gcp_service.read_pickle(self.file_name)

        blob.assert_called_with(self.file_name)
        blob = blob()
        file = blob.open().__enter__()
        mock_pickle.load.assert_called_with(file)

    def tearDown(self):
        self.client_patcher.stop()
