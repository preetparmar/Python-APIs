# Importing Library
import dropbox
from os import listdir
import pandas as pd
import configparser
from dropbox.exceptions import AuthError
from dropbox import DropboxOAuth2FlowNoRedirect

# Variable
DROPBOX_FOLDER_PATH = '/Apps/SpendingTracker/Exports'
LOCAL_FOLDER_PATH = './spend data'

# Getting all local files
local_files = listdir(LOCAL_FOLDER_PATH)

# Getting the access token
config = configparser.ConfigParser()
config.read('config.ini')
# access_token = config['LOGIN']['access_token']
APP_KEY = config['LOGIN']['app_key']
APP_SECRET = config['LOGIN']['app_secret']

# Initializing Dropbox API
def dropbox_connect(key=APP_KEY, secret=APP_SECRET):
    """Create a connection to Dropbox."""
    auth_flow = DropboxOAuth2FlowNoRedirect(key, secret)
    authorize_url = auth_flow.start()
    print("1. Go to: " + authorize_url)
    print("2. Click \"Allow\" (you might have to log in first).")
    print("3. Copy the authorization code.")
    auth_code = input("Enter the authorization code here: ").strip()

    try:
        oauth_result = auth_flow.finish(auth_code)
        # dbx = dropbox.Dropbox(long_term_access_token)
        dbx = dropbox.Dropbox(oauth2_access_token=oauth_result.access_token)
    except Exception as e:
        print('Error: %s' % (e,))
        exit(1)

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
