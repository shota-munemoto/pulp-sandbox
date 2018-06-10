import os
import subprocess

project_root_directory = os.path.dirname(os.path.abspath(__file__))

os.chdir(os.path.join(project_root_directory, 'static'))
subprocess.run(['npm', 'run', 'build'])

os.chdir(project_root_directory)
subprocess.run(['pyinstaller', 'main.spec', '--clean'])
