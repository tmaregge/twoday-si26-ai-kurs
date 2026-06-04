from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from openai import OpenAI
from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient


import os

load_dotenv()

# Document Intelligence
di_endpoint = os.environ["DI_ENDPOINT"]
di_key = os.environ["DI_KEY"]
di_client = DocumentIntelligenceClient(di_endpoint, AzureKeyCredential(di_key))

# OpenAI Service
oai_endpoint = os.environ["OAI_ENDPOINT"]
oai_key = os.environ["OAI_KEY"]
oai_client = OpenAI(base_url=oai_endpoint, api_key=oai_key)

# Azure AI Search
search_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
search_key = os.environ["AZURE_SEARCH_API_KEY"]
index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
search_client = SearchClient(search_endpoint, index_name, AzureKeyCredential(key))
