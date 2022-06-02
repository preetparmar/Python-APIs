""" Reading the token """
# Importing Library
import configparser

# Reading the access token
config = configparser.ConfigParser()
config.read('config.ini')
access_token = config['LOGIN']['access_token']
long_term_access_token = config['LOGIN']['long_term_access_token']

""" Connecting to dropbox """
# Importing Library
import dropbox
from dropbox.exceptions import AuthError

# Connecting to dropbox
try:
    dbx = dropbox.Dropbox(long_term_access_token)
except AuthError as e:
    print(f'Error connecting to Dropbox using the access token: {e}')

""" Getting metadata of all the files inside the desired folder """
dropbox_folder_path = '/Apps/SpendingTracker/Exports'
files = dbx.files_list_folder(dropbox_folder_path).entries
files_list = []
for file in files:
    if isinstance(file, dropbox.files.FileMetadata):
        metadata = {
            'name': file.name,
            'path_display': file.path_display,
        }
        files_list.append(metadata)

""" Saving the metadata into a Pandas DataFrame """
# Importing Library
import pandas as pd

df = pd.DataFrame.from_records(files_list)

""" Iterate over the DataFrame and download the files """
# Importing Library
from os import listdir

local_folder_path = './spend data'
local_files = listdir(local_folder_path)

for name, path in zip(df.loc[:, 'name'], df.loc[:, 'path_display']):
        if name not in local_files:
            metadata, result = dbx.files_download(path)
            with open(f'{local_folder_path}/{name}', 'wb') as f:
                f.write(result.content)

""" Testing new oAuth """
import dropbox
import configparser
from dropbox import DropboxOAuth2FlowNoRedirect

config = configparser.ConfigParser()
config.read('config.ini')

APP_KEY = config['LOGIN']['app_key']
APP_SECRET = config['LOGIN']['app_secret']
lt_access_token = config['LOGIN']['long_term_access_token']

auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, use_pkce=True, token_access_type='offline')

authorize_url = auth_flow.start()

lt_access_token.strip()


print(f'Go to: {authorize_url}')

try:
    oauth_result = auth_flow.finish(lt_access_token.strip())
except Exception as e:
    print(f'Error: {e}')

