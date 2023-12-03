"""
This initializes our code allowing us to import across submodules. 
If you are getting import errors, run pip install -e . while your inside the /MightyMicros/ (project root) directory.
"""
from setuptools import setup, find_packages
import os
import subprocess
import sys

def parse_requirements(filename):
    """ Load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

def install_packages():
    # Install mmcv
    os.environ['MMCV_WITH_OPS'] = '1'
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', './mmcv'])

    # Install openmim
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'openmim'])
    
    # Install mmdet
    # subprocess.check_call(['mim', 'install', 'mmdet==2.27.0'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'mmdet==2.27.0'])

    # Install mmrotate
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', './mmrotate'])
    
    # Install requirements
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])



if __name__ == '__main__':
    
    install_packages()
    setup(
        name='mighty-micros', 
        version='0.3', 
        packages=find_packages(),
        entry_points={
                'console_scripts': [
                    'mighty-micros = src.entry:run'
                ]
            }
        )