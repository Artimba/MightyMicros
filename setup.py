"""
This initializes our code allowing us to import across submodules. 
If you are getting import errors, run pip install -e . while your inside the /MightyMicros/ (project root) directory.
"""
from setuptools import setup, find_packages
import os
import subprocess
import sys

def is_cuda_available():
    try:
        subprocess.check_output(['nvcc', '--version'])
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False

requirements = [
            'pykalman',
            'pyqt5',
            'requests==2.28.2',
            'jupyterlab-server==2.19.0',
            'notebook==6.4.13',
            'tensorboard',
            'opencv-python-headless',
            'opencv-contrib-python',
            'tqdm'
            'mmcv-full==1.7.1',
            'mmdet==2.28.2',
            'mmrotate==0.3.4'
        ]

if __name__ == '__main__':
    if is_cuda_available():
        requirements.append('torch==2.1.1+cu121')
        requirements.append('torchvision==0.16.1+cu121')
    else:
        requirements.append('torch==2.1.1+cpu')
        requirements.append('torchvision==0.16.1+cpu')
    # install_packages()
    setup(
        name='mighty-micros', 
        version='0.4', 
        packages=find_packages(),
        entry_points={
                'console_scripts': [
                    'mighty-micros = src.entry:run'
                ]
            },
        install_requires=requirements,
        )