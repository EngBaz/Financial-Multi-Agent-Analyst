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
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
SERPER_API_KEY = os.environ["SERPER_API_KEY"]

#groq_llm = "groq/llama-3.3-70b-versatile"

files = {
    'agents':'configs/agents.yaml',
    'tasks':'configs/tasks.yaml',
    }

configs = {}
for config_type, file_path in files.items():
    with open(file_path, 'r') as file:
        configs[config_type] = yaml.safe_load(file)

agents_config = configs['agents']
tasks_config = configs['tasks']

@tool
class CryptoDataCollectorTool(BaseTool):
    name: str = "get_crypto_data"
    description: str = "Fetch basic crypto data for a given ticker and period."

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

crypto_data_colloctor_tool = CryptoDataCollectorTool()

data_collector_agent = Agent(
    config=agents_config['data_collector_agent'],
    tools=[crypto_data_colloctor_tool],
)

crypto_researcher_agent = Agent(
    config=agents_config['crypto_researcher_agent'],  
    tools=[SerperDevTool(), ScrapeWebsiteTool()],    
)

reporting_agent = Agent(
    config=agents_config['reporting_agent'],
)

data_collector_task = Task(
    config=tasks_config['data_collector_task'],    
    agent=data_collector_agent,
    async_execution=True,                        
)

crypto_researcher_task = Task(
    config=tasks_config['crypto_researcher_task'],   
    agent=crypto_researcher_agent,
    async_execution=True,                            
)

reporting_task = Task(
    config=tasks_config['reporting_task'],  
    agent=reporting_agent,
    context=[data_collector_task, crypto_researcher_task],  
)

crew = Crew(
    agents=[data_collector_agent, 
            crypto_researcher_agent, 
            reporting_agent
            ],
    tasks=[data_collector_task, 
           crypto_researcher_task, 
           reporting_task
           ],
    process=Process.sequential,
    verbose=True,
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
