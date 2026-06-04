import argparse
from src.chat import chat
from src.document_processing import ingest, chunk
from src.retrieve import retrieve


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["chat", "ingest", "chunk", "retrieve"])
    args = parser.parse_args()

    if args.mode == "chat":
        chat()
    elif args.mode == "ingest":
        ingest()
    elif args.mode == "chunk":
        chunk()
    elif args.mode == "retrieve":
        retrieve()


if __name__ == "__main__":
    main()
