# Importing Library
from kaggle.api.kaggle_api_extended import KaggleApi


class myKaggleAPI:

    def __init__(self):
        self.api = KaggleApi()
        self.api.authenticate()


    def search_competition(self, name:str=None, category:str=None, page:int=1, detail:bool=False) -> list:
        """ 

        Returns a list of competitons available on Kaggle
        
        Parameters:
            name: str, optional
                text you want to search in the title of the competiton
            category: str, optional
                specific category you want to search
            page: int, optional
                returns the competition on a specific page
            detail: bool, optional, default=False
                toggle it to true to get competition details printed
        Retuns:
            list of competions fiiting the search
        
        """
        category_list = ['all', 'featured', 'research', 'recruitment', 'gettingStarted', 'masters', 'playground']
        if category is not None and category not in category_list:
            raise ValueError("Invalid Catgory Name!\nValid Options are: 'all', 'featured', 'research', 'recruitment', 'gettingStarted', 'masters', 'playground'")
        
        if detail:
            self.api.competitions_list_cli(search=name, category=category, page=page)
        
        comp_list = self.api.competitions_list(search=name, category=category)
        return [str(comp) for comp in comp_list]


    def get_list_of_files(self, competition:str, details:bool=False) -> list:
        """
        Get list of all the files available for the competion
        
        Parameter:
            competions: str
                name of the competion
        
        Return:
            list of all the files
        """
        file_details = self.api.competitions_data_list_files(competition)
        files = [file['name'] for file in file_details]
        if details: 
            print(*file_details, sep='\n')
        return files


    def download_all_files(self, competition:str, path:str=None):
        """
        Downloads all files from competion
        Parameters:
            competion: str
                name of the competition
            path: str, optional
                path where you want to save the file
                *if the path is invalid, it will create a folder with the given name in the base folder
                *it will create a folder if not present in the path
        Return:
            downloads all the file in the specified location
        """
        try:
            self.api.competition_download_files(competition, path, force=True, quiet=True)
            if path is None:
                print('All files were successfully downloaded to the base folder')
            else:
                print(f'All files were successfully downlaoded to {path}')
        except:
            print('Unable to download file\nPlease check the Competition Name or File Name')


    def download_specific_file(self, competition:str, file_name:str, path:str=None):
        """
        Downloads a specific file from competion
        Parameters:
            competion: str
                name of the competition
            file_name: str
                name of the file you want to download
            path: str, optional
                path where you want to save the file
                *if the path is invalid, it will create a folder with the given name in the base folder
                *it will create a folder if not present in the path
        Return:
            downloads the file in the specified location
        """
        try:
            self.api.competition_download_file(competition, file_name, path=path, force=True, quiet=True)
            if path is None:
                print('File was successfully downloaded to the base folder')
            else:
                print(f'File was successfully downlaoded to {path}')
        except:
            print('Unable to download file\nPlease check the Competition Name or File Name')


my_kaggle = myKaggleAPI()  # Initiating my class

# Search for a competition by Name
comp_list = my_kaggle.search_competition(name='tit', detail=True)

# Getting list of files within a competition
competition = comp_list[0]
file_list = my_kaggle.get_list_of_files(competition, details=True)

# Downloading specific file
path = 'D:/Titanic_Kaggle'
file_to_download = file_list[2]

my_kaggle.download_specific_file(competition, file_to_download, path)

# Download all the files
my_kaggle.download_all_files(competition, path)