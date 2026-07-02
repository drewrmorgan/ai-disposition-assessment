import streamlit as st
import pandas as pd

st.title("AI Dispositions Dashboard")

try:

    df = pd.read_excel(
    "AI_Disposition_Responses.xlsx",
    engine="openpyxl"
)

    st.write(df)

except FileNotFoundError:

    st.warning(
        "No responses have been collected yet."
    )
