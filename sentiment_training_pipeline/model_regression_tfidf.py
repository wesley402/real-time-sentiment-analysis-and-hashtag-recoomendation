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
import os, sys
import pickle

#refer https://github.com/tthustla/setiment_analysis_pyspark/blob/master/Sentiment%20Analysis%20with%20PySpark.ipynb

# spark config
#sc = ps.SparkContext() # check default spark config
#print(sc.getConf().getAll())
conf = ps.SparkConf().setAll([('spark.executor.memory', '3g'), ('spark.executor.cores', '2'), ('spark.cores.max', '2'), ('spark.driver.memory','3g')])
#sc.stop()
sc = ps.SparkContext(conf=conf)
#print(sc.getConf().getAll())
sqlContext = SQLContext(sc)

# load data sentiment140_clean.csv
df = sqlContext.read.format('csv').options(header='true', inferschema='true').load('sentiment140_clean.csv')
# first look at data
#print(type(df))
print(df.count())
print(df.show(5))
df.printSchema()

df = df.dropna()
#print(df.count())

# extract feature
(train_set, val_set, test_set) = df.randomSplit([0.98, 0.01, 0.01], seed = 2000)
tokenizer = Tokenizer(inputCol="text", outputCol="words")
hashtf = HashingTF(numFeatures=2**16, inputCol="words", outputCol='tf')
idf = IDF(inputCol='tf', outputCol="features", minDocFreq=5) #minDocFreq: remove sparse terms
label_stringIdx = StringIndexer(inputCol = "target", outputCol = "label")
pipeline = Pipeline(stages=[tokenizer, hashtf, idf, label_stringIdx])

pipelineFit = pipeline.fit(train_set)
train_df = pipelineFit.transform(train_set)
val_df = pipelineFit.transform(val_set)
train_df.show(5)

#build model
lr = LogisticRegression(maxIter=100)
lrModel = lr.fit(train_df)

# evaluate model
predictions = lrModel.transform(val_df)
evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction")
print(evaluator.evaluate(predictions))
print(evaluator.getMetricName())
accuracy = predictions.filter(predictions.label == predictions.prediction).count() / float(val_set.count())
print('sameModel accuracy {}'.format(accuracy))

# Save and load model (not work right now)
#output_dir = os.path.abspath('/output/model')
filename = 'sentiment_model.pkl'
# now you can save it to a file
lrModel.write().save('/output')

print("save model done!")
