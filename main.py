import argparse
from src.chat import chat
from src.ingest import ingest
from src.retrieve import retrieve


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["chat", "ingest", "retrieve"])
    args = parser.parse_args()

    if args.mode == "chat":
        chat()
    elif args.mode == "ingest":
        ingest()
    elif args.mode == "retrieve":
        retrieve()


if __name__ == "__main__":
    main()
