import os, sys, json, shutil

class Organize:
    def __init__(self, folder='Downloads'):
        self.folder = self.get_folder_path(folder)
        self.json = self.load_json()
        os.chdir(self.folder)

    
    def get_folder_path(self, folder):
        path = '~/' + folder
        return os.path.expanduser(path)


    def load_json(self):
        extension_file = open('extensions.json', 'r')
        return json.load(extension_file)


    def execute(self):
        
        print(f'\nWorking in directory: {self.folder}\n')
        files = os.listdir(self.folder)
        
        for file in files:
            name, extension = os.path.splitext(file)
            folder = self.map_folder(extension[1:])     # [1:] removing . from extension like .mp4
            
            if folder is not None:
                print(f'{folder.upper()} <--- {file}')
                if not os.path.isdir(folder):
                    folder = folder.upper()
                    os.mkdir(folder)
                self.move(file, folder)

        print(f'\nProcess complete.\n')


    def map_folder(self, ext):
        for folder, extensions in self.json.items():
            if ext.lower() in extensions:
                return folder


    def move(self, file, folder):
        folder = folder.upper()
        shutil.move(file, folder)


if __name__ == '__main__':

    arguments = sys.argv
    try:
        if len(arguments) > 1:
            directory = arguments[1]
            process = Organize(directory)
        else:
            process = Organize()
    except FileNotFoundError:
        sys.exit('No such directory found.')
    process.execute()