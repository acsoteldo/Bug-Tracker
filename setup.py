import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="bugtrak",
    version="2022",
    packages=find_packages(),
    include_package_data=True,
    license="MIT License",  # example license
    description="System to track bugs.",
    long_description=README,
    url="",
    author="",
    author_email="",
    classifiers=[
        "",
    ],
)
