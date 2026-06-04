import json
from src.clients import get_di_client


data_path = "src/data"
pdf_path = f"{data_path}/personalhandbok-twoday.pdf"
scanned_json_path = f"{data_path}/scanned.json"


def ingest():
    client = get_di_client()

    with open(pdf_path, "rb") as f:
        poller = client.begin_analyze_document(model_id="prebuilt-layout", body=f)

    result = poller.result()
    text = result.content

    with open(scanned_json_path, "w", encoding="utf-8") as f:
        json.dump(
            result.as_dict(),
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(text)
    return text


def chunk():
    with open(scanned_json_path, "r") as f:
        scanned = json.load(f)

    return scanned
