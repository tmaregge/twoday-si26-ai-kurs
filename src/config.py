from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from dotenv import load_dotenv

import os

load_dotenv()

di_endpoint = os.environ["DI_ENDPOINT"]
di_key = os.environ["DI_KEY"]

di_credential = AzureKeyCredential(di_key)

di_client = DocumentIntelligenceClient(di_endpoint, di_credential)
