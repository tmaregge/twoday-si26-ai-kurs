import random
import sys
import importlib.util
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent)) # find clients.py

# Load fasit/rag.py explicitly to avoid picking up the outer rag.py
_spec = importlib.util.spec_from_file_location("rag", Path(__file__).parent / "rag.py")
_rag = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_rag)
search = _rag.search
ask = _rag.ask

import streamlit as st

blurbs = [
    "Tenker",
    "Grubler",
    "Vurderer",
    "Tar stilling til",
    "Konkluderer"
]


def ui():
    st.title("Søk i dokumenter")

    question = st.text_input("Spørsmål")

    if st.button("Spør"):
        blurb = random.choice(blurbs)
        with st.status(blurb, expanded=False) as status:
            search_results = search(question)
            status.write("Søkeresultater")
            status.write(search_results)
            answer = ask(question)
            status.update(label="Ferdig", state="complete")

        st.write("Spørsmål:", question)
        st.write("Svar:", answer)

if __name__ == "__main__":
    ui()
