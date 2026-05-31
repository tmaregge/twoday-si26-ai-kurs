from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeOutputOption, AnalyzeResult

from dotenv import load_dotenv

import streamlit as st
import os

load_dotenv()

di_endpoint = os.environ["DI_ENDPOINT"]
di_key = os.environ["DI_KEY"]

di_credential = AzureKeyCredential(di_key)

di_client = DocumentIntelligenceClient(di_endpoint, di_credential)

document_path = "documents/personalhandbok-twoday.pdf"
output_dir = "outputs"


def analyze_document():
    with open(document_path, "rb") as f:
        poller = di_client.begin_analyze_document(
            "prebuilt-read",
            body=f,
            output=[AnalyzeOutputOption.PDF],
        )
        result: AnalyzeResult = poller.result()

        return result


def main():
    if st.button("Analyze document"):
        result = analyze_document()

        if st.button("Show result"):
            st.write(result)
            print(result)


if __name__ == "__main__":
    main()
