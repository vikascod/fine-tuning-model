from setuptools import find_packages, setup
from typing import List

# Define a function to read requirements from a file and return them as a list.
def get_requirements(file_path: str) -> List[str]:
    requirements = []
    with open(file_path, 'r') as file_obj:
        requirements = file_obj.readlines()
        requirements = [requirement.replace('\n', "") for requirement in requirements]

    return requirements

# Define the setup configuration for the Python package.
setup(
    name="Vertex AI model fine-tuning",
    version='0.0.1',
    author='Vikas',
    author_email='vikas1618072@gmail.com',
    packages=find_packages(),  # Automatically find and include all packages in the project
    install_requires=get_requirements('requirements.txt')  # Specify package dependencies from a requirements file
)