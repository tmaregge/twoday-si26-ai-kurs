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

from src.clients import get_search_idx_client


client = get_search_idx_client()


def create_index(index_name: str):
    name = index_name
    fields = [
        SimpleField(name="chunkId", type=SearchFieldDataType.String, key=True),
        SimpleField(name="documentId", type=SearchFieldDataType.String),
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


def index_chunks(chunks: list, index_name: str): ...


def retrieve(*args, **kwargs): ...
