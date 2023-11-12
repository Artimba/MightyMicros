"""
This initializes our code allowing us to import across submodules. 
If you are getting import errors, run pip install -e . while your inside the /MightyMicros/ (project root) directory.
"""
from setuptools import setup, find_packages

setup(name='mighty-micros', version='0.1', packages=find_packages())