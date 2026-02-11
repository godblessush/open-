import datetime
import os

def get_time():
    return datetime.datetime.now().strftime("%I:%M %p")
print(get_time())

def open_notepad():
    os.system("notepad")
    
