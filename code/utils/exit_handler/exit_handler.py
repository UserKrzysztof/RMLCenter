import os
import shutil
from utils.logger.log import Logger


def delete_files_in_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path) 
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

class ExitHandler():
    def handle(self):
        Logger().delete_log()
        delete_files_in_directory('episodes_recaps')
        print('See ya!')