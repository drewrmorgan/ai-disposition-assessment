import streamlit as st
import pandas as pd

# ----------------------------------
# PASSWORD PROTECTION
# ----------------------------------

password = st.text_input(
    "Enter Dashboard Password",
    type="password"
)

if password != st.secrets["dashboard_password"]:
    st.warning(
        "Enter the dashboard password to access dashboard data."
    )
    st.stop()

# ----------------------------------
# DASHBOARD
# ----------------------------------

st.title("AI Dispositions Dashboard")

try:

    df = pd.read_excel(
        "AI_Disposition_Responses.xlsx",
        engine="openpyxl"
    )

    st.success(f"Total Responses: {len(df)}")

    st.dataframe(df)

except FileNotFoundError:

    st.warning(
        "No responses have been collected yet."
    )
