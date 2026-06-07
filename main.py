from src.clients import get_search_client
from src.chat import chat
from src.document_processing import ingest, chunk, ingest_pypdf
from src.retrieval import get_index, retrieve


scanned = ingest_pypdf("src/data/personalhandbok-twoday.pdf", "src/data/scanned.json")
# chunks = chunk(scanned, "personalhandbok-twoday.pdf")

# index = get_index("idx-torstein")
# search_client = get_search_client()
