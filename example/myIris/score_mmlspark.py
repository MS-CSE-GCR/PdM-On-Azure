# This script contains the init and run functions needed to 
# deploy the trained model as a web service.
# Test the functions before deploying the web service.

def init():
    # One-time initialization of PySpark and predictive model
    import pyspark
    from azureml.assets import get_local_path
    from mmlspark.TrainClassifier import TrainedClassifierModel

    global trainedModel
    global spark
    spark = pyspark.sql.SparkSession.builder.appName("irisapp").getOrCreate()

    # load the model file using link file reference
    # local_path = get_local_path('mmlspark_model/AdultCensusModel.link')
    local_path = "./iris.mml"
    print(local_path)
    
    trainedModel = TrainedClassifierModel.load(local_path)
   
def run(input_df):
    # Compute prediction
    prediction = trainedModel.transform(input_df)
    
    results = {
        "Prediction": str(prediction.first().scored_labels),
        "sepal length": float(input_df.iloc[0,0]),
        "sepal width": float(input_df.iloc[0,1]),
        "petal length": float(input_df.iloc[0,2]),
        "petal width": float(input_df.iloc[0,3]),
        "Location": str(input_df.iloc[0,4]),
        "Timestamp": str(input_df.iloc[0,5])
    }
    
    # return just the first prediction
    return json.dumps(results)
    # return prediction.first().scored_labels

if __name__ == "__main__":
    # Test scoring
    init()
    sample = spark.createDataFrame([(3.0, 3, 1, 0.25, "Beijing", "06/28/2018")],['sepal length', 'sepal width','petal length','petal width', 'Location', 'Timestamp'])
    print('Positive vs negative prediction: ',run(sample))