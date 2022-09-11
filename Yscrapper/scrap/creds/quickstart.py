from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']


def authorize_gdrive_creds():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(r"D:\personal\YoutubeScrapper-Backend\Yscrapper\scrap\creds\token.json"):
        creds = Credentials.from_authorized_user_file(r"D:\personal\YoutubeScrapper-Backend\Yscrapper\scrap\creds\token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r'D:\personal\YoutubeScrapper-Backend\Yscrapper\scrap\creds\credentialsProd.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(r"D:\personal\YoutubeScrapper-Backend\Yscrapper\scrap\creds\token.json", 'w') as token:
            token.write(creds.to_json())

    try:
        return build('drive', 'v3', credentials=creds)

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')



def upload_file(service, folder_id, src_file_name, target_file_name):
    """
    Creates a folder and upload a file to it
    """
    # authenticate account
    # service = authorize_gdrive_creds()
    # folder details we want to make
    # folder_metadata = {
    #     "name": "Downloads",
    #     "mimeType": "application/vnd.google-apps.folder"
    # }
    # create the folder
    # file = service.files().create(body=folder_metadata, fields="id").execute()
    # get the folder id
    # folder_id = file.get("id")
    # print("Folder ID:", folder_id)
    # upload a file text file
    # first, define file metadata, such as the name and the parent folder ID
    file_metadata = {
        "name": target_file_name,
        "parents": [folder_id]
    }
    # upload
    media = MediaFileUpload(src_file_name, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print("File created, id:", file.get("id"))


if __name__ == '__main__':
    authorize_gdrive_creds()