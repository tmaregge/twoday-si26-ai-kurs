from src.retrieval import search
import streamlit as st
from src.chat import ask
import random

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
