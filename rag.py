def ingest_pypdf(pdf_path: str, out_path: str = "") -> str:
    ...

def ingest_di(pdf_path: str, out_path: str = "") -> AnalyzeResult:
    ...

def chunk(document):
    ...

def create_index(index_name: str):
    fields = [
            SimpleField(
                name="chunk_id",
                type=SearchFieldDataType.String,
                key=True,
            ),
            SimpleField(
                name="document_id",
                type=SearchFieldDataType.String,
                filterable=True,
            ),
            SearchableField(
                name="content",
                type=SearchFieldDataType.String,
            ),
        ]
    ...

def index_chunks(chunks: list[dict], index_name: str):
    ...

def search(search_text: str, document_id: str = "", top: int = 5):
    ...

def chat(question: str, context: str):
    ...

def ask(question: str, document_id: str = ""):
    ...
    
def embed(text):
    ...
