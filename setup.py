"""
This initializes our code allowing us to import across submodules. 
If you are getting import errors, run pip install -e . while your inside the /MightyMicros/ (project root) directory.
"""
from setuptools import setup, find_packages
import os
import subprocess
import sys


if __name__ == '__main__':
    
    # install_packages()
    setup(
        name='mighty-micros', 
        version='0.3', 
        packages=find_packages(),
        entry_points={
                'console_scripts': [
                    'mighty-micros = src.entry:run'
                ]
            },
        install_requires=[
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
        )