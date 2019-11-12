from setuptools import find_packages, setup

REQUIRED_PACKAGES = ["cognite-model-hosting==0.2.0"]

setup(name="transform", version="0.1", install_requires=REQUIRED_PACKAGES, packages=find_packages())
