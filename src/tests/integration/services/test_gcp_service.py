import pytest

from config import TEST_BUCKET, TESTS_FOLDER
from services.gcp_service import GCPStorageService

gcp_service = GCPStorageService(TEST_BUCKET)


@pytest.fixture()
def clean_up_gcp_files():
    file_names = []
    yield file_names
    for file_name in file_names:
        gcp_service.bucket.blob(file_name).delete(gcp_service.storage_client)


@pytest.mark.parametrize("filename", ['no_face.jpg', 'one_face.jpg', 'test_index.pkl'])
def test_upload_to_bucket(clean_up_gcp_files, filename):
    assert gcp_service.bucket.blob(filename).exists() is False
    gcp_service.upload_to_bucket(filename, TESTS_FOLDER / f'data/{filename}')
    clean_up_gcp_files.append(filename)
    assert gcp_service.bucket.blob(filename).exists() is True


@pytest.mark.parametrize("filename", ['test_olga_2.jpg', 'three_faces.jpg'])
def test_download_as_bytes(filename):
    byte_content = gcp_service.download_as_bytes(filename)
    with open(TESTS_FOLDER / f'data/{filename}', 'rb') as local_file:
        local_byte_content = local_file.read()
    assert byte_content == local_byte_content


@pytest.mark.parametrize("filename", ['test_file_0.pkl', 'test_file_1.pkl'])
def test_read_pickle(filename):
    deserialized_obj = gcp_service.read_pickle(filename)
    assert deserialized_obj is not None
