#taken from this StackOverflow answer: https://stackoverflow.com/a/39225039

import requests
import logging
logging.basicConfig(level=logging.INFO)

GOOGLE_DOC_URL = "https://docs.google.com/uc?export=download"

class GoogleDriveDownloader: 

    def __init__(self, fileId, destination):
        self._fileid = fileId
        self._destination = destination
        self._session = requests.Session()
        self.logger = logging.getLogger("GoogleDriveDownloader")        

    def download_file_from_google_drive(self):
        id = self._fileid
        destination = self._destination
        response = self._session.get(GOOGLE_DOC_URL, params={
                                     'id': id}, stream=True)
        token = self.get_confirm_token(response)

        if token:
            params = { 'id' : id, 'confirm' : token }
            response = self._session.get(
                GOOGLE_DOC_URL, params=params, stream=True)

        self.logger.info(f"downloading file : {self._destination}")
        self.save_response_content(response)
        self.logger.info(f"download complete for file : {self._destination}")
        return destination
    
    def get_confirm_token(self, response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    def save_response_content(self, response):
        CHUNK_SIZE = 32768
        destination = self._destination
        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

if __name__ == "__main__":
    destination = 'export.pkl'
    googleDriveFileId = '1Z3SvYdGNR_k7yrtGWgU73r2W_tMVL3XE'
    gd = GoogleDriveDownloader(googleDriveFileId, destination)
    gd.download_file_from_google_drive()
