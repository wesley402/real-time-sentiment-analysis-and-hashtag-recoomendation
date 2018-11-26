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

# spark config
#sc = ps.SparkContext() # check default spark config
#print(sc.getConf().getAll())
conf = ps.SparkConf().setAll([('spark.executor.memory', '8g'), ('spark.executor.cores', '3'), ('spark.cores.max', '3'), ('spark.driver.memory','8g')])
#sc.stop()
sc = ps.SparkContext(conf=conf)
#print(sc.getConf().getAll())
sqlContext = SQLContext(sc)

# load data sentiment140_clean.csv
df = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('../sentiment_training_pipeline/sentiment140_clean.csv')
# first look at data
#print(type(df))
print(df.count())
print(df.show(5))
df.printSchema()

df = df.dropna()
#print(df.count())

#step_1 Create transformers
# feature extractors: TF-IDF
# Tokenizer.transform() method splits the raw text documents into words, adding a new column with words to the DataFrame.
tokenizer = Tokenizer(inputCol="text", outputCol="words") # feature transformer
# HashingTF.transform() method converts the words column into feature vectors, adding a new column with those vectors to the DataFrame.
# numFeatures should be a power of two otherwise the features will not be mapped evenly to the columns
hashtf = HashingTF(numFeatures=2**16, inputCol="words", outputCol='tf')
idf = IDF(inputCol='tf', outputCol="features", minDocFreq=5) #minDocFreq: remove sparse terms
label_stringIdx = StringIndexer(inputCol = "target", outputCol = "label")

#step_2 Create an estimator
lr = LogisticRegression(maxIter=100, regParam=0.01)

#step_3 Create a pipeline
# A pipeline can be thought of as a chain of multiple discrete stages
pipeline = Pipeline(stages=[tokenizer, hashtf, idf, label_stringIdx, lr])

#step_4 Fitting the model
(train_set, test_set) = df.randomSplit([0.7, 0.3], seed = 666)
# Pipeline.fit() method is called on the original DataFrame, which has raw text documents and labels.
# Pipeline.fit() returns the PipelineModel object that can be used for prediction by calling .transform()
model = pipeline.fit(train_set)
# estimate the model
test_model = model.transform(test_set)
test_model.show(5)

#step_5 Evaluate model's performance
evaluator = BinaryClassificationEvaluator(rawPredictionCol='probability')
test_accu_roc = evaluator.evaluate(test_model,{evaluator.metricName:'areaUnderROC'})
test_accu_pr = evaluator.evaluate(test_model,{evaluator.metricName:'areaUnderPR'})
print("AreaUnderROC: {0:.4f}".format(test_accu_roc)) #  0.8597
print("AreaUnderPR: {0:.4f}".format(test_accu_pr)) # 0.8515

#step_6 Save the model
modelPath = '../sentiment_training_pipeline/output/tfidf_logistic_pipelineModel'
model.write().overwrite().save(modelPath)

#step_7 Load the PipelineModel
loadedPipelineModel = PipelineModel.load(modelPath)
test_reloadedModel = loadedPipelineModel.transform(test_set)
test_reloadedModel.show(5)

#step_8 Evaluate reloaded model's performance
evaluator_reloaded = BinaryClassificationEvaluator(rawPredictionCol='probability')
test_accu_roc_reloaded = evaluator_reloaded.evaluate(test_reloadedModel,{evaluator.metricName:'areaUnderROC'})
test_accu_pr_reloaded = evaluator_reloaded.evaluate(test_reloadedModel,{evaluator.metricName:'areaUnderPR'})
print("AreaUnderROC: {0:.4f}".format(test_accu_roc_reloaded))
print("AreaUnderPR: {0:.4f}".format(test_accu_pr_reloaded))
