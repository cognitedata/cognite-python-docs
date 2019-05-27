<a href="https://cognite.com/">
    <img src="https://github.com/cognitedata/cognite-python-docs/blob/master/img/cognite_logo.png" alt="Cognite logo" title="Cognite" align="right" height="80" />
</a>

Cognite Python Documentation
============================
[![build](https://webhooks.dev.cognite.ai/build/buildStatus/icon?job=github-builds/cognite-python-docs/master)](https://jenkins.cognite.ai/job/github-builds/job/cognite-python-docs/job/master/)

Overview
--------
Here you can find documentation and examples for anything Python related on top of Cognite Data Fusion.

- [Python Documentation](https://cognite-docs.readthedocs-hosted.com/en/latest/)

You may also want to take a look at the documentation for the the API

- [API Reference](https://api.cognitedata.com)
- [API Guide](https://doc.cognitedata.com/guides/api-guide.html)

Examples
--------

### [Basics](examples/basics)

A collection of simple examples to get you started with CDP.

### [Model Hosting](examples/model_hosting)

A collection of Jupyter notebooks showing how to use the model hosting environment.


Prerequisites
-------------
In order to start using these examples, you need to set up the following

### Install Python
Here are instructions for installing Python on your system:

- [macOs](https://wsvincent.com/install-python3-mac/)

### Set Environment Variables
An API key in the COGNITE_API_KEY environment variable.

You can set the environment variable on macOs or Linux like this
```bash
$ export COGNITE_API_KEY=<YOUR-API-KEY>
```

On Windows, you can follows [these instructions](https://www.computerhope.com/issues/ch000549.htm).

### Install Dependencies
You need to install the dependencies required to run through the examples.
You can do this using pip (requirements.txt) or [pipenv](https://pipenv.readthedocs.io/en/latest/).

#### Using requirements.txt
```bash
$ pip install -r requirements.txt
``` 

#### Using Pipenv
```bash
$ pipenv shell
$ pipenv sync --dev
```
