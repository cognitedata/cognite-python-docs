from setuptools import find_packages, setup

REQUIRED_PACKAGES = ["cognite-model-hosting"]

setup(name="transform", version="0.1", install_requires=REQUIRED_PACKAGES, packages=find_packages())
