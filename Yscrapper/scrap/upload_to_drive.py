# Enable Python3 compatibility
from __future__ import (unicode_literals, absolute_import, print_function,
                        division)
import os

# Import Google libraries
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import GoogleDriveFileList
import googleapiclient.errors

# Import general libraries
from googleapiclient.http import MediaFileUpload

def upload_single_file(service, src_file_name, target_file_name):
    """
    Uploads a file
    """
    file_metadata = {
        "name": target_file_name
    }

    # upload
    media = MediaFileUpload(src_file_name, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='webViewLink, id').execute()

    permission = {
    'role': 'reader',
    'type': 'anyone',
    'allowFileDiscovery': True
    }

    service.permissions().create(body=permission, fileId=file.get("id")).execute()
    
    return file.get("webViewLink")

