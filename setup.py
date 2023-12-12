import re
from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import sys
import importlib.resources
import os

class CustomInstall(install):
    def run(self):
        print("Running custom install script")
        # Install PyTorch with CUDA if available
        if is_cuda_available():
            cuda = get_cuda_version()
            print("Found CUDA Version: ", cuda)
            install_torch_with_matching_cuda(cuda)
        else:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'torch==2.1.1', 'torchvision==0.16.1'])
            


        # Proceed with the standard installation
        install.run(self)

def get_cuda_version():
    """Get the CUDA toolkit version installed on the system."""
    try:
        nvcc_output = subprocess.check_output(['nvcc', '--version']).decode()
        version_match = re.search(r'release (\d+\.\d+)', nvcc_output)
        if version_match:
            return version_match.group(1)
    except (subprocess.CalledProcessError, FileNotFoundError, AttributeError):
        return None

def install_torch_with_matching_cuda(cuda_version):
    """Install PyTorch with the version matching the system's CUDA version."""
    torch_cuda_version_map = {
        '11.8': 'torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cu118',
        '12.1': 'torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cu121'
    }
    torch_installation_command = torch_cuda_version_map.get(cuda_version)
    if torch_installation_command:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + torch_installation_command.split())
    else:
        raise RuntimeError(f"No compatible PyTorch wheel found for CUDA version {cuda_version}. Compatible versions: 11.8, 12.1")


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
    'ultralytics'
    # Note: torch and torchvision are handled separately in CustomInstall
]

if __name__ == '__main__':
    setup(
        name='mighty-micros', 
        version='0.6', 
        packages=find_packages(),
        entry_points={
            'console_scripts': [
                'mighty-micros = src.entry:run'
            ]
        },
        install_requires=requirements,
        cmdclass={
            'install': CustomInstall,
        },
        package_data={
            'src.pipeline': ['configs/*.py', 'weights/*'],
            'src.recordings': ['*.mp4']
        }
    )

