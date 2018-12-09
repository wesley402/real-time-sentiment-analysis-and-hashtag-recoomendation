import pandas as pd
import pyspark as ps
import warnings
from pyspark.ml.feature import HashingTF, IDF, Tokenizer, CountVectorizer
from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.classification import LogisticRegression,LogisticRegressionModel
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.sql import SQLContext
from pyspark.sql.functions import *
from pyspark import SparkContext,SparkConf
import shutil

#refer https://github.com/tthustla/setiment_analysis_pyspark/blob/master/Sentiment%20Analysis%20with%20PySpark.ipynb

conf = ps.SparkConf().setAll([('spark.executor.memory', '2g'), ('spark.executor.cores', '1'), ('spark.cores.max', '3'), ('spark.driver.memory','2g')])
sc = ps.SparkContext(conf=conf)
sqlContext = SQLContext(sc)


df = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('../sentiment_training_pipeline/sentiment_test.csv')
# first look at data
#print(type(df))
print(df.count())
print(df.show(5))
df.printSchema()



modelPath = '../sentiment_training_pipeline/output/tfidf_logistic_pipelineModel'



# step_7 Load the PipelineModel
loadedPipelineModel = PipelineModel.load(modelPath)
test_reloadedModel = loadedPipelineModel.transform(df)
test_reloadedModel.show(5)
