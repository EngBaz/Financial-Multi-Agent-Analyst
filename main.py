import os
import streamlit as st

from crew import *
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
SERPER_API_KEY = os.environ["SERPER_API_KEY"]

def main():
    st.set_page_config(page_title="Advanced Cryptocurrency Analysis Dashboard", layout="wide")
    st.title("Advanced Cryptocurrency Analysis Dashboard!")
    st.sidebar.header("Cryptocurrency Analysis")

    crypto_tickers = ["BTC-USD", "ETH-USD", "ADA-USD", "XRP-USD", "SOL-USD", "BNB-USD", "DOGE-USD", "TRX-USD", "DOT-USD", "AVAX-USD",
                      "SHIB-USD", "MATIC-USD", "LUNA-USD", "LTC-USD", "LINK-USD", "UNI-USD", "ALGO-USD"]
    selected_crypto_ticker = st.sidebar.selectbox("Select a crypto:", crypto_tickers)

    period = ["1y", "2y", "3y", "4y", "5y", "6y"]
    selected_period = st.sidebar.selectbox("Select a timeframe:", period)

    analyze_button = st.sidebar.button("Analyze")

    if analyze_button:
        st.info(f"Starting analysis. This may take a few minutes...")
    
        result = FinancialAnalystCrew().crew().kickoff(inputs={"ticker": selected_crypto_ticker,"period": selected_period})
        
        st.success("Analysis complete!")
        st.markdown(result)

if __name__ == "__main__":
    main()
