from setuptools import setup,find_packages
from typing import List


# Declaring variables for setup function
PROJECT_NAME = "Insurance premium predictor"
VERSION = "0.0.1"
AUTHOR = "Remya Premdas"
PACKAGES=find_packages()
REQUIREMENT_FILE_NAME="requirements.txt"

# -> List[str] will Return the list of requirements in list format. NOte : list we use and the List here are different.. L is in Caps
def get_requirement_list()->List[str]:
    """
    Description:This function will return the requiremnts mentioned in the requirements.txt file
    return : returns list of the libraries present in requirements.txt file
    """
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        return (requirement_file.readlines().remove("-e ."))

setup(
    name= PROJECT_NAME,
    version = VERSION,
    author = AUTHOR,
    description = "this is the internship project for Insurance premium prediction",
    packages=PACKAGES,
    install_requires=get_requirement_list()
)

#if __name__=="__main__":
    #print(get_requirement_list())
