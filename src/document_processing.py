import json
from pypdf import PdfReader


def ingest_pypdf(pdf_path: str, out_path: str = ""):
    reader = PdfReader(pdf_path)

    pages = []
    all_text = []

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = text.strip()

        pages.append(
            {
                "pageNumber": page_num,
                "content": text,
            }
        )
        if text:
            all_text.append(text)

    result = {
        "content": "\n\n".join(all_text),
        "pages": pages,
    }

    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    return result


