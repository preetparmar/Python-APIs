# Importing Library
import dropbox
from os import listdir
import pandas as pd
import configparser
from dropbox.exceptions import AuthError

# Variable
DROPBOX_FOLDER_PATH = '/Apps/SpendingTracker/Exports'
LOCAL_FOLDER_PATH = './spend data'

# Getting all local files
local_files = listdir(LOCAL_FOLDER_PATH)

# Getting the access token
config = configparser.ConfigParser()
config.read('config.ini')
access_token = config['LOGIN']['access_token']

# Initializing Dropbox API
def dropbox_connect():
    """Create a connection to Dropbox."""

    try:
        dbx = dropbox.Dropbox(access_token)
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx

def dropbox_list_files():
    """Return a Pandas dataframe of files in a given Dropbox folder path in the Apps directory.
    """
    dbx = dropbox_connect()

    try:
        files = dbx.files_list_folder(DROPBOX_FOLDER_PATH).entries
        files_list = []
        for file in files:
            if isinstance(file, dropbox.files.FileMetadata):
                metadata = {
                    'name': file.name,
                    'path_display': file.path_display,
                    'client_modified': file.client_modified,
                    'server_modified': file.server_modified
                }
                files_list.append(metadata)

        df = pd.DataFrame.from_records(files_list)
        return dbx, df.sort_values(by='server_modified', ascending=False)

    except Exception as e:
        print('Error getting list of files from Dropbox: ' + str(e))


def dropbox_download_and_save_files():
    """ Downloads and saves the files which don't already exist locally """
    dbx, df = dropbox_list_files()
    for name, path in zip(df.loc[:, 'name'], df.loc[:, 'path_display']):
        if name not in local_files:
            metadata, result = dbx.files_download(path)
            with open(f'{LOCAL_FOLDER_PATH}/{name}', 'wb') as f:
                f.write(result.content)

if __name__ == '__main__':
    dropbox_download_and_save_files()
