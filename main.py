import os
import streamlit as st
import yfinance as yf
import pandas as pd
import time

from crewai import Agent, Task, Crew
# from langchain_groq import ChatGroq
from crewai_tools import ScrapeWebsiteTool, SerperDevTool, BaseTool

from dotenv import load_dotenv
load_dotenv()

# Set API keys for the services used (GROQ, Cohere, Google and OpenAI) from environment variables 
GROQ_API_KEY = os.environ["GROQ_API_KEY"]
#COHERE_API_KEY = os.environ["COHERE_API_KEY"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
#GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]

# llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

#import yfinance as yf

#ticker = "BTC-USD"
#period = "1y"

#btc = yf.Ticker(ticker)
#historical_data = btc.history(period=period)
#info = btc.info

#name = info.get('name', 'N/A')
#symbol = info.get('symbol', 'N/A')
#market_cap = info.get('marketCap', 'N/A')
#circulating_supply = info.get('circulatingSupply', 'N/A') 

#print("Historical Data:")
#print(historical_data.head())

#print("\nInfo Data:")
#print(info)

#print("---------")
#print(name)
#print(symbol)
#print(market_cap)
#print(circulating_supply)


class CryptoInfoTool(BaseTool):
    name: str = "get_basic_crypto_info"
    description: str = "Fetch basic crypto information for a given ticker and period."

    def _run(self, ticker: str, period: str = '1y') -> str:
        try:
            btc = yf.Ticker(ticker)
            historical_data = btc.history(period=period)
            info = btc.info

            # Extract values with default fallbacks
            name = info.get('name', 'N/A')
            symbol = info.get('symbol', 'N/A')
            market_cap = info.get('marketCap', 'N/A')
            circulating_supply = info.get('circulatingSupply', 'N/A')

            stock_avg = round(historical_data['Close'].mean(), 2) if not historical_data.empty else 'N/A'
            stock_max = round(historical_data['Close'].max(), 2) if not historical_data.empty else 'N/A'
            stock_min = round(historical_data['Close'].min(), 2) if not historical_data.empty else 'N/A'

            # Construct the response
            response = f"""
            **Cryptocurrency Analysis:**
            - Name: {name}
            - Symbol: {symbol}
            - Market Cap: {market_cap}
            - Circulating Supply: {circulating_supply}
            - Stock Price (Last {period}):
              - Average: {stock_avg}
              - Max: {stock_max}
              - Min: {stock_min}
            """
            return response

        except Exception as e:
            return f"An error occurred while fetching crypto data: {str(e)}"

crypto_info_tool = CryptoInfoTool()

print(crypto_info_tool)

crypto_researcher = Agent(
    role="Cryptocurrency Researcher",
    goal="Gather and display detailed financial metrics and performance data for a given cryptocurrency, including its name, ticker, market cap, circulating supply, and historical stock price metrics over a specified period.",
    backstory="An experienced cryptocurrency researcher dedicated to providing concise, actionable insights about cryptocurrency performance and key financial metrics.",
    tools=[crypto_info_tool],
    verbose=True,
    allow_delegation=False,
)

collect_crypto_info = Task(
    description=''' 
    1. Retrieve detailed information about the cryptocurrency mentioned in the user query, including its name, ticker, market cap, circulating supply, and historical stock price data (average, maximum, and minimum) over the specified timeframe.
    2. If no ticker or timeframe is mentioned, identify the cryptocurrency and use a default timeframe of 1 year.
    3. Provide a clear and concise summary of the financial metrics and performance data gathered.

    User query: {query}.

    Your response should include:
    - Cryptocurrency Name and Ticker
    - Market Cap
    - Circulating Supply
    - Stock Price Average, Maximum, and Minimum over the specified period
    - Any relevant additional insights based on the query.
    ''',
    expected_output="A detailed report summarizing the cryptocurrency's financial metrics and historical performance.",
    agent=crypto_researcher,
    dependencies=[],
    context=[]
)

crew = Crew(
    agents=[crypto_researcher],
    tasks=[collect_crypto_info]
)

def stream_data(response):
    
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.06)

## Streamlit application Configuration      
st.set_page_config(page_title="Advanced Cryptocurrency Analysis Dashboard", layout="wide")

st.title("Advanced Cryptocurrency Analysis Dashboard")

st.sidebar.header("Cryptocurrency Analysis Query")
query = st.sidebar.text_area("Enter your cryptocurrency analysis question", 
                             value="Is Bitcoin a safe long-term bet for a risk-averse individual?", height=100)
analyze_button = st.sidebar.button("Analyze")

if analyze_button:
    st.info(f"Starting analysis. This may take a few minutes...")
    result = crew.kickoff(inputs={"query": query})
    st.success("Analysis complete!")
    st.markdown(result)
