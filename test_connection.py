#!/usr/bin/env python3

from clients import *


def check_di():
    try:
        client = get_di_client()
        print("✅ DI client created:", type(client).__name__)
    except Exception as e:
        print("❌ DI:", e)

def check_oai():
    try:
        client = get_oai_client()

        # cheap API call
        models = client.models.list()
        first = next(iter(models.data), None)

        print("✅ OpenAI connected")
        if first:
            print("   first model:", first.id)

    except Exception as e:
        print("❌ OpenAI:", e)

def check_search():
    try:
        client = get_search_client()

        # top=1 avoids fetching much
        results = list(client.search("*", top=1))

        print(f"✅ Search connected ({len(results)} docs returned)")

    except Exception as e:
        print("❌ Search:", e)

def check_search_index():
    try:
        client = get_search_idx_client()

        indexes = list(client.list_index_names())

        print("✅ Search Index connected")
        print("   indexes:", indexes)

    except Exception as e:
        print("❌ Search Index:", e)

if __name__ == "__main__":
    check_di()
    check_oai()
    check_search()
    check_search_index()   
