from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = "-e ."

def get_requirements(file_path: str) -> List[str]:
    requirements = []
    with open(file_path) as file_obj:
        # Read lines and strip newline characters correctly
        requirements = [req.strip() for req in file_obj.readlines()]

    # Remove '-e .' if it is in the requirements list
    if HYPEN_E_DOT in requirements:
        requirements.remove(HYPEN_E_DOT)

    return requirements

setup(
    name='mlproject',
    version='0.0.1',
    author='Guhan',
    author_email='cguhan03@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),  
)