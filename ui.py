import streamlit as st


def ui():
    if st.button("Knapp"):
        st.write("Knappen ble trykket!")
        st.balloons()
        st.toast("Hurra!")

    pdf = st.file_uploader("Last opp en PDF")
    if pdf:
        st.pdf(pdf)


if __name__ == "__main__":
    ui()
