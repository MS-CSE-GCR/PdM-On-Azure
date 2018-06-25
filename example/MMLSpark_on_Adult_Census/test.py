import inspect, os
from azure.storage.blob import BlockBlobService, PublicAccess

# https://d3ykhwqrp6tfe.blob.core.windows.net/spark4pdms/example/data/AdultCensusIncome.csv

dataFile = "AdultCensusIncome.csv"
if not os.path.isfile(dataFile):
    local_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    block_blob_service = BlockBlobService(
        account_name='d3ykhwqrp6tfe', 
        account_key='x92h32DEPZRglqM06Oi6aWPG7OrNooAAkttvUL6qc6LR2TtiN7cpQU4F9CyZHMp4B1YsH/NysUSQEFAVQpgkgA=='
        )
    block_blob_service.get_blob_to_path("spark4pdms", "example/data/AdultCensusIncome.csv", os.path.join(local_path , dataFile))