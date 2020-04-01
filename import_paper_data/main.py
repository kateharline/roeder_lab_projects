import json
import os
import io
import httplib2
import pickle

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import auth

# from quickstart

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

service = build('drive', 'v3', credentials=creds)

def main():
    # open json file from drive
    file_id = '1HrbNQ85aoeJObK7qVzgqD19liipjnj3U'


    # https://developers.google.com/drive/api/v3/manage-downloads
    request = service.files().export_media(fileId=file_id,
                                                 mimeType='application/json')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print
        "Download %d%%." % int(status.progress() * 100)


if __name__ == '__main__':
    main()