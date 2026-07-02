import streamlit as st
import pandas as pd

st.title("AI Dispositions Dashboard")

try:

    df = pd.read_csv("responses.csv")

    st.write(df)

except FileNotFoundError:

    st.warning(
        "No responses have been collected yet."
    )
