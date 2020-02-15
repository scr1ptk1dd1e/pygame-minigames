import os
import platform

# check linux systems

python = 'python'
if platform.system() != 'Windows':
    python = 'python3'

os.system(python + ' MainMenu/main.py')