import os
import shutil

def run():
    print('resetting environment')
    os.remove('urls.csv')
    shutil.rmtree('html_content')