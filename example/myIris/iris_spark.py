import numpy as np
import pandas as pd
import pyspark
import os
import urllib
import sys

from pyspark.sql.functions import *
from pyspark.ml.classification import *
from pyspark.ml.evaluation import *
from pyspark.ml.feature import *

from azureml.logging import get_azureml_logger

import pickle
import inspect, os
from azure.storage.blob import BlockBlobService, PublicAccess

# initialize logger
run_logger = get_azureml_logger() 

# start Spark session
spark = pyspark.sql.SparkSession.builder.appName('Iris').getOrCreate()

# print runtime versions
print ('****************')
print ('Python version: {}'.format(sys.version))
print ('Spark version: {}'.format(spark.version))
print ('****************')

# load iris.csv into Spark dataframe
dataFile = "iris.csv"
if not os.path.isfile(dataFile):
    local_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    block_blob_service = BlockBlobService(
        account_name='pdms', 
        account_key='0+fcK61ROcuGbQQ9MdY0tNtb/tnxpeNuskQWAew1gufb3Fld+BOJkDa6LOZkw6RQW0oo3Z5fIMJu5HthFc/dQA=='
        )
    block_blob_service.get_blob_to_path(
        "azureml", 
        dataFile, 
        os.path.join(local_path , dataFile)
    )
data = spark.createDataFrame(pd.read_csv(dataFile, header=None, names=['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']))
print("First 10 rows of Iris dataset:")
data.show(10)

# vectorize all numerical columns into a single feature column
feature_cols = data.columns[:-1]
assembler = pyspark.ml.feature.VectorAssembler(inputCols=feature_cols, outputCol='features')
data = assembler.transform(data)

# convert text labels into indices
data = data.select(['features', 'class'])
label_indexer = pyspark.ml.feature.StringIndexer(inputCol='class', outputCol='label').fit(data)
data = label_indexer.transform(data)

# only select the features and label column
data = data.select(['features', 'label'])
print("Reading for machine learning")
data.show(10)

# change regularization rate and you will likely get a different accuracy.
reg = 0.01
# load regularization rate from argument if present
if len(sys.argv) > 1:
    reg = float(sys.argv[1])

# log regularization rate
run_logger.log("Regularization Rate", reg)

# use Logistic Regression to train on the training set
train, test = data.randomSplit([0.70, 0.30])
lr = pyspark.ml.classification.LogisticRegression(regParam=reg)
model = lr.fit(train)

# predict on the test set
prediction = model.transform(test)
print("Prediction")
prediction.show(10)

# evaluate the accuracy of the model using the test set
evaluator = pyspark.ml.evaluation.MulticlassClassificationEvaluator(metricName='accuracy')
accuracy = evaluator.evaluate(prediction)

print()
print('#####################################')
print('Regularization rate is {}'.format(reg))
print("Accuracy is {}".format(accuracy))
print('#####################################')
print()

# log accuracy
run_logger.log('Accuracy', accuracy)

# create the outputs folder
os.makedirs('./outputs', exist_ok=True)

print("******** SAVE THE MODEL ***********")
model.write().overwrite().save("./outputs/iris.mml")

# create web service schema
from azureml.api.schema.dataTypes import DataTypes
from azureml.api.schema.sampleDefinition import SampleDefinition
from azureml.api.realtime.services import generate_schema

# Define the input dataframe
sample = spark.createDataFrame([(3.0, 3, 1, 0.25, "Beijing", "06/28/2018")],['sepal length', 'sepal width','petal length','petal width', 'Location', 'Timestamp'])
inputs = {"input_df": SampleDefinition(DataTypes.SPARK, sample)}

# Create the schema file (service_schema.json) the the output folder.
import score_mmlspark
generate_schema(run_func=score_mmlspark.run, inputs=inputs, filepath='./outputs/service_schema.json')
