from google.cloud import storage
import pickle


class GCPStorageService:
    def __init__(self, bucket_name):
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.get_bucket(bucket_name)

    def read_pickle(self, filename):
        with self.bucket.blob(filename).open(mode='rb') as f:
            return pickle.load(f)

    def download_as_bytes(self, filename):
        return self.bucket.blob(filename).download_as_bytes(self.storage_client)

    def upload_to_bucket(self, blob_name, path_to_file):
        blob = self.bucket.blob(blob_name)
        blob.upload_from_filename(path_to_file)
