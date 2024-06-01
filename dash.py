from sys import argv
import streamlit as st
import pandas as pd

# File loader in chunks
@st.cache_data
def loadData(filename):
    chunkSize = 10_000
    chunks = []

    for chunk in pd.read_csv(filename, sep=",", chunksize=chunkSize):
        chunks.append(chunk)

    loaded = pd.concat(chunks)
    return loaded


def main(csvFile):
    # Create sidebar
    with st.sidebar:
        # Define rows to be loaded
        rowsLimit = st.select_slider(
            "Select limit of rows to be displayed",
            options=["50k", "100k", "200k", "300k", "500k"]
        )
        # Define chart to be shown
        selectBox = st.selectbox(
            "Pick a chart", ("PnL", "CashFlow")
        )
    
    match rowsLimit:
        case "50k":
            rowsLimit = 50_000
        case "100k":
            rowsLimit = 100_000
        case "200k":
            rowsLimit = 200_000
        case "300k":
            rowsLimit = 300_000
        case "500k":
            rowsLimit = 500_000           

    # Create dataframe from csvFile with limit of rows RowsLimit
    df = loadData(csvFile).head(rowsLimit)

    # Display charts
    match selectBox:
        case "PnL":
            chart = st.line_chart(df, x="ts", y="pnl")
        case "CashFlow":
            chart = st.line_chart(df, x="ts", y="cashflow")
        case _:
            chart = st.line_chart()

# Call main
main("results.csv")
