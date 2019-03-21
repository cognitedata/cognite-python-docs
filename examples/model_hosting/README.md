<a href="https://cognite.com/">
    <img src="https://github.com/cognitedata/cognite-python-docs/blob/master/img/cognite_logo.png" alt="Cognite logo" title="Cognite" align="right" height="80" />
</a>

Model Hosting Examples
======================

## Prerequisites
In order to start using these examples, you need to be using Python 3.5.0

## Examples

### [Deploying and scheduling a simple function](simple_function/SimpleFunction.ipynb)

This example shows a source package for applying a trivial transformation to two time series and setting up a schedule 
run this transformation on incoming data every minute. This example is a good place to get comfortable with how the 
hosting environment works.

### [Deploying and scheduling a pretrained model](scheduled_model/ScheduledPrediction.ipynb)

This example is a slightly more complex version of the simple function example. We will still be scheduling a 
transformation on some time series data, but we will do so using a model we train locally and upload to the hosting 
environment.

### [Training and deploying a model in the hosting environment](simple_train_predict/TrainAndPredict.ipynb)

This example shows the how you can both train and deploy a model in the hosting environment.

### [Using Data Specs and the Data Fetcher](data_fetcher/)

This is a collection of a few examples showing how to use the data specs and the data fetcher found in the 
cognite-model-hosting library.

### Deploying Jupyter notebooks

If your model is simple enough to fit into a Jupyter notebook we offer a solution for easily deploying a
notebook directly to Model Hosting from within the the notebook itself.
Basically creating a source package from a notebook.
This functionality is available throught the `cognite-model-hosting-notebook` package.
Here are some examples showing how to use this package.

#### [Deploy a very simple temperature converter](notebook/simple_temperature_converter/SimpleTemperatureConverter.ipynb)

Deploy a simple model that convert from Fahrenheit to Celsius.

#### [Deploy a more advanced temperature converter](notebook/advanced_temperature_converter/AdvancedTemperatureConverter.ipynb)

Deploy a model that can convert arbitrarily between arrays of Kelvin, Celsius and Fahrenheit.

#### [Train locally and deploy in Model Hosting](notebook/training/LocalTraining.ipynb)

Train a simple linear regression model locally and deploy the trained model to model hosting.

#### [Train and deploy in Model Hosting](notebook/training/CloudTraining.ipynb)

Train a simple linear regression model in Model Hosting and have it deployed afterwards.

#### [Deploy and schedule a simple calculation](notebook/simple_scheduled_calculation/SimpleScheduledCalculation.ipynb)

Deploy a simple model that find the average between to time series.
Then schedule it to run continuously on two actual time series and outputting to a third time series.
