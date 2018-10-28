import sys
import pyspark as ps
import warnings
from pyspark.ml.feature import HashingTF, IDF, Tokenizer, CountVectorizer
from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression,LogisticRegressionModel
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.sql import SQLContext
from pyspark.sql.functions import *
from pyspark import SparkContext,SparkConf
import shutil
# spark config
#sc = ps.SparkContext() # check default spark config
#print(sc.getConf().getAll())
conf = ps.SparkConf().setAll([('spark.executor.memory', '8g'), ('spark.executor.cores', '3'), ('spark.cores.max', '3'), ('spark.driver.memory','8g')])
#sc.stop()
sc = ps.SparkContext(conf=conf)
train_df = None
lr = LogisticRegression(maxIter=100)
lrModel = lr.fit(train_df)

from pyspark.ml.classification import LogisticRegressionModel
output_dir = 'output/model_rgr'
sameModel = LogisticRegressionModel.load(sc, output_dir)
print("load model done!")
