from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    ComplexField,
    CorsOptions,
    SearchIndex,
    ScoringProfile,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
)

from src.clients import get_search_idx_client, get_search_client


client = get_search_idx_client()


def create_index(index_name: str):
    name = index_name
    fields = [
        SimpleField(name="chunkId", type=SearchFieldDataType.String, key=True),
        SimpleField(name="documentId", type=SearchFieldDataType.String, filterable=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
    ]
    cors_options = CorsOptions(allowed_origins=["*"], max_age_in_seconds=60)
    scoring_profiles = []
    index = SearchIndex(
        name=name,
        fields=fields,
        scoring_profiles=scoring_profiles,
        cors_options=cors_options,
    )

    result = client.create_or_update_index(index)
    return result


def get_index(idx_name: str):
    return client.get_index(idx_name)

def recreate_index(index_name: str):
    try:
        client.delete_index(index_name)
    except Exception:
        # If it doesn't exist yet, just create it
        pass

    return create_index(index_name)


def index_chunks(chunks: list[dict], index_name: str):
    search_client = get_search_client()

    result = search_client.upload_documents(documents=chunks)

    succeeded = sum(1 for r in result if r.succeeded)
    failed = len(result) - succeeded

    print(f"Indexed {succeeded} documents, {failed} failed")

    return result


def search(search_text: str, document_id: str = "", top: int = 5):
    search_client = get_search_client()

    if (document_id):
        results = search_client.search(
            search_text=search_text,
            filter=f"documentId eq '{document_id}'",
            top=top,
        )
    else:
        results = search_client.search(
            search_text=search_text,
            top=top,
        )

    return [
        {
            "chunkId": result["chunkId"],
            "content": result["content"],
        }
        for result in results
    ]
