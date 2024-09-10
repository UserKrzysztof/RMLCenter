import os
from datetime import datetime

class Logger():
    def __init__(self) -> None:
        self.LOG_PATH = 'log.txt'

    def print_to_log(self,message:str):
        with open(self.LOG_PATH, 'a') as f:
            f.write(f'\n{datetime.today().strftime("%Y-%m-%d %H:%M:%S")}: {message}')
    
    def read_from_log(self):
        with open(self.LOG_PATH, 'r') as f:
            return f.read()
        
    def delete_log(self):
        if os.path.exists(self.LOG_PATH):
            os.remove(self.LOG_PATH)
            print("Log deleted")
        else:
            print("The log file does not exist")
    
    def serialize_log(self):
        #TODO put old log into archive 
        pass
