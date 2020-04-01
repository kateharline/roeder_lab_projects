import json
import os



def main():
    # open json file from drive
    fileId = ''

    # https://developers.google.com/drive/api/v3/manage-downloads

    request = drive_service.files().export_media(fileId=file_id,
                                                 mimeType='application/pdf')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print
        "Download %d%%." % int(status.progress() * 100)


if __name__ == '__main__':
    main()