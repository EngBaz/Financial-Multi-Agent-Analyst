import os
import streamlit as st
import yfinance as yf
import pandas as pd
import time
import yaml

from crewai import Agent, Task, Crew, Process
from crewai_tools import ScrapeWebsiteTool, SerperDevTool, BaseTool
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
#COHERE_API_KEY = os.environ["COHERE_API_KEY"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
#GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# Define file paths for YAML files

files = {
    'agents': 'configs/agents.yaml',
    'tasks' : 'configs/tasks.yaml',
    }

configs = {}
for config_type, file_path in files.items():
    with open(file_path, 'r') as file:
        configs[config_type] = yaml.safe_load(file)


agents_config = configs['agents']
tasks_config = configs['tasks']


class CryptoDataTool(BaseTool):
    name: str = "get_basic_crypto_info"
    description: str = "Fetch basic crypto information for a given ticker and period."

    def _run(self, ticker: str, period: str) -> str:
        try:
            btc = yf.Ticker(ticker)
            historical_data = btc.history(period=period)
            info = btc.info

            name = info.get('name', 'N/A')
            symbol = info.get('symbol', 'N/A')
            market_cap = info.get('marketCap', 'N/A')
            circulating_supply = info.get('circulatingSupply', 'N/A')

            stock_avg = round(historical_data['Close'].mean(), 2) if not historical_data.empty else 'N/A'
            stock_max = round(historical_data['Close'].max(), 2) if not historical_data.empty else 'N/A'
            stock_min = round(historical_data['Close'].min(), 2) if not historical_data.empty else 'N/A'

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

crypto_data_tool = CryptoDataTool()
search_tool = SerperDevTool()

data_analyst_agent = Agent(
    config=agents_config['data_analyst_agent'],
    tools=[crypto_data_tool],
)

news_analyst_agent = Agent(
    config=agents_config['news_analyst_agent'],
    tools=[search_tool],
)
    
data_analyst_task = Task(
    config=tasks_config['data_analyst_task'],
    agent=data_analyst_agent,
)

news_analyst_task = Task(
    config=tasks_config['news_analyst_task'],
    agent=news_analyst_agent,
)

crew = Crew(
    agents=[data_analyst_agent, news_analyst_agent],
    tasks=[data_analyst_task, news_analyst_task],
    process=Process.hierarchical,
    verbose=True,
    manager_llm=ChatOpenAI(model="gpt-4-turbo", temperature=0),
)

def stream_data(response):
    
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.06)
     
st.set_page_config(page_title="Advanced Cryptocurrency Analysis Dashboard", layout="wide")
st.title("Advanced Cryptocurrency Analysis Dashboard")
st.sidebar.header("Cryptocurrency Analysis Input")

crypto_tickers = ["BTC-USD", "ETH-USD", "ADA-USD", "XRP-USD"]
selected_crypto_ticker = st.sidebar.selectbox("Select a crypto:", crypto_tickers)

period = ["1y", "2y", "3y"]
selected_period = st.sidebar.selectbox("Select a period:", period)

analyze_button = st.sidebar.button("Analyze")

if analyze_button:
    st.info(f"Starting analysis. This may take a few minutes...")
    result = crew.kickoff(inputs={"ticker": selected_crypto_ticker,
                                  "period": selected_period})
    st.success("Analysis complete!")
    st.markdown(result)
