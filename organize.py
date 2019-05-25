import os, sys, json, shutil

# change working directory
os.chdir(os.path.dirname(__file__))

class Organize:
    def __init__(self, folder='Downloads'):
        self.folder = self.get_folder_path(folder)
        self.json = self.load_json()

    
    def get_folder_path(self, folder):
        ''' Generate folder path '''
        path = os.path.join('~', folder)
        return os.path.expanduser(path)


    def load_json(self):
        ''' Load json file '''
        extension_file = open('extensions.json', 'r')
        return json.load(extension_file)


    def execute(self):
        ''' Execute main flow of program '''
        print(f'\nWorking in directory: {self.folder}\n')
        files = os.listdir(self.folder)
        
        for file in files:
            name, extension = os.path.splitext(file)
            folder = self.map_folder(extension[1:])     # [1:] removing . from extension like .mp4
            
            if folder is not None:
                print(f'{folder.upper()} <--- {file}')
                folder = folder.upper()
                file = os.path.join(self.folder, file)
                new_folder = os.path.join(self.folder, folder)
                if not os.path.isdir(new_folder):
                    os.mkdir(new_folder)
                self.move(file, folder)

        print(f'\nProcess complete.\n')


    def map_folder(self, ext):
        ''' Compare file extensions with extensions present in json file '''
        for folder, extensions in self.json.items():
            if ext.lower() in extensions:
                return folder


    def move(self, file, folder):
        ''' Move files to a folder '''
        folder = folder.upper()
        folder = os.path.join(self.folder, folder)
        file = os.path.join(folder, file)
        try:
            shutil.move(file, folder)
        except shutil.Error as err:
            # handle file already exist error
            print(f"Replacing old file >>> {err}")
            shutil.copy(file, folder)               # copy file instead of moving
            os.remove(file)                         # remove copied file


if __name__ == '__main__':

    arguments = sys.argv
    try:
        if len(arguments) > 1:
            for argument in arguments[1:]:
                # print(os.getcwd())
                Organize(argument).execute()
        else:
            Organize().execute()
    except FileNotFoundError as err:
        sys.exit(f'No such directory found. {err}')