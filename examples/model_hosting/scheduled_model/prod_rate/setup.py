from setuptools import find_packages, setup

# It's important to specify all dependencies on external packages,
# so that these can be installed.
REQUIRED_PACKAGES = ["scikit-learn==0.20.3", "numpy>=1.8.2", "scipy>=0.13.3", "cognite-model-hosting==0.1.2"]

setup(
    name="prod-rate",
    version="0.1",
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    description="A random forrest regressor used to find production rate for abc equipment",
    url="https://relevant.webpage",
    maintainer="Tutorial",
    maintainer_email="Tutorial",
)
