import os
import platform

this_path = os.path.dirname(os.path.abspath(__file__))

# check linux systems

python = 'python'
if platform.system() != 'Windows':
    python = 'python3'

path = os.path.join(this_path, 'MainMenu/main.py')
os.system(python + ' ' + path)