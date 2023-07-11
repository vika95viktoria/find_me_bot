import pickle

from google.cloud import storage


class GCPStorageService:
    """
    Class providing interface for interaction with GCP Storage
    """

    def __init__(self, bucket_name):
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.get_bucket(bucket_name)

    def read_pickle(self, filename: str):
        """
        Read pickle file directly from GCP bucket

        Open pickle file stored in GCP bucket and load it into object using pickle module
        :param filename: name of the pickle file with full path inside the bucket.
               For example: 'folder/sub_folder/file.pkl'
        :return: object deserialized from pickle file
        """
        with self.bucket.blob(filename).open(mode='rb') as f:
            return pickle.load(f)

    def download_as_bytes(self, filename: str) -> bytes:
        """
        Read data from object stored in GCP bucket as bytes

        Reads blob content directly from GCP bucket without downloading it as file to the container instance
        :param filename: name of the blob with full path inside the bucket. For example: 'folder/sub_folder/file.txt'
        :return: file content as bytes
        """
        return self.bucket.blob(filename).download_as_bytes(self.storage_client)

    def upload_to_bucket(self, blob_name: str, path_to_file: str):
        """
        Upload locally stored file to GCP bucket

        :param blob_name: name of the future blob in GCP bucket
        :param path_to_file: local filepath to the file to be uploaded
        """
        blob = self.bucket.blob(blob_name)
        blob.upload_from_filename(path_to_file)
