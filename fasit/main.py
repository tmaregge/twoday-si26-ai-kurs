from src.clients import get_search_client
from src.chat import chat
from src.document_processing import ingest, chunk, ingest_pypdf
from src.retrieval import get_index, index_chunks, retrieve


# scanned = ingest_pypdf("src/data/personalhandbok-twoday.pdf", "src/data/scanned.json")
# chunks = chunk(scanned["result"], "personalhandbok-twoday.pdf")
# index_result = index_chunks(chunks, "idx-torstein")
