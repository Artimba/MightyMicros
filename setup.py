from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import sys

class CustomInstall(install):
    def run(self):
        # Install mmcv-full, mmdet, and mmrotate using mim
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'openmim'])
        subprocess.check_call(['mim', 'install', 'mmcv-full==1.7.1'])
        subprocess.check_call(['mim', 'install', 'mmdet==2.28.2'])
        subprocess.check_call(['mim', 'install', 'mmrotate==0.3.4'])

        # Proceed with the standard installation
        install.run(self)

def is_cuda_available():
    try:
        subprocess.check_output(['nvcc', '--version'])
        return True
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
    'tqdm',
    'openmim'
]

if __name__ == '__main__':
    if is_cuda_available():
        requirements.append('torch==2.1.1+cu121')
        requirements.append('torchvision==0.16.1+cu121')
    else:
        requirements.append('torch==2.1.1+cpu')
        requirements.append('torchvision==0.16.1+cpu')

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
        cmdclass={
            'install': CustomInstall,
        }
    )
