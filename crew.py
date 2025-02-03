import yfinance as yf

from crewai import Agent, Task, Crew, Process
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from crewai.project import CrewBase, agent, task, crew, before_kickoff
from crewai.tools import BaseTool 


class CryptoDataCollectorTool(BaseTool):
    name: str = "get_crypto_data"
    description: str = "Fetch basic crypto data for a given ticker and period."
    
    def _run(self, ticker: str, period: str) -> str:
        try:
            crypto = yf.Ticker(ticker)
            history= crypto.history(period=period)
            info = crypto.info

            if history.empty:
                return f"No data available for {ticker}. Please check the symbol."
            
            name = info.get('name', 'N/A')
            symbol = info.get('symbol', 'N/A')
            market_cap = info.get('marketCap', 'N/A')
            circulating_supply = info.get('circulatingSupply', 'N/A')

            crypto_avg = round(history['Close'].mean(), 2) if not history.empty else 'N/A'
            crypto_max = round(history['Close'].max(), 2) if not history.empty else 'N/A'
            crypto_min = round(history['Close'].min(), 2) if not history.empty else 'N/A'

            response = f"""
            - Name: {name}
            - Symbol: {symbol}
            - Market Cap: {market_cap}
            - Circulating Supply: {circulating_supply}
            - Cryptocurrency Price (Last {period}):
              - Average: {crypto_avg}
              - Max: {crypto_max}
              - Min: {crypto_min}
            """
            return response

        except Exception as e:
            return f"An error occurred while fetching crypto data: {str(e)}"
        
class CryptoTechnicalAnalysisTool(BaseTool):
    name: str = "get_crypto_technical_analysis"
    description: str = "Perform technical analysis on a given cryptocurrency ticker and period."
    
    def _run(self, ticker: str, period: str) -> str:
        try:
            crypto = yf.Ticker(ticker)
            history = crypto.history(period=period)
            
            if history.empty:
                return f"No data available for {ticker}. Please check the symbol."

            moving_avg_50 = history['Close'].rolling(window=50).mean().iloc[-1]
            moving_avg_200 = history['Close'].rolling(window=200).mean().iloc[-1]
            latest_close = history['Close'].iloc[-1]
            rsi = (history['Close'].diff().gt(0).sum() / len(history)) * 100

            return {
                "Latest Close": {latest_close},
                "50-Day Moving Average": {moving_avg_50},
                "200-Day Moving Average": {moving_avg_200},
                "RSI": {rsi}
            }
        except Exception as e:
            return f"Error fetching technical data: {str(e)}"

@CrewBase
class FinancialAnalystCrew():
    """Financial Analyst crew"""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
                
    @agent
    def data_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_data_analyst'],
            tools=[CryptoDataCollectorTool()],
            verbose=True,
            memory=False,
            )

    @agent
    def news_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['news_researcher'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True,
            memory=False,
            )
        
    @agent
    def fundamental_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['fundamental_analyst'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True,
            memory=False,
            )
        
    @agent
    def technical_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['technical_analyst'],
            tools=[CryptoTechnicalAnalysisTool()],
            verbose=True,
            memory=False,
            )
        
    @agent
    def financial_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_analyst'],
            verbose=True,
            memory=False,
            )

    @agent
    def technical_report(self) -> Agent:
        return Agent(
            config=self.agents_config['technical_report'],
            verbose=True,
            memory=False,
            )
    
    @task
    def data_analyst_task(self) -> Task:
        return Task(
            config=self.tasks_config['senior_data_analyst_task'],
            agent=self.data_analyst(),
            async_execution=True,
            )

    @task
    def news_researcher_task(self) -> Task:
        return Task(
            config=self.tasks_config['news_researcher_task'],
            agent=self.news_researcher(),
            async_execution=True,
            )

    @task
    def fundamental_analyst_task(self) -> Task:
        return Task(
            config=self.tasks_config['fundamental_analyst_task'],
            agent=self.fundamental_analyst(),
            async_execution=True,
            )

    @task
    def technical_analyst_task(self) -> Task:
        return Task(
            config=self.tasks_config['technical_analyst_task'],
            agent=self.technical_analyst(),
            async_execution=True,
            )

    @task
    def financial_analyst_task(self) -> Task:
        return Task(
            config=self.tasks_config['financial_analyst_task'],
            agent=self.financial_analyst(),
            context=[self.fundamental_analyst_task(), self.technical_analyst_task()],
            )

    @task
    def technical_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['technical_report_task'],  
            agent=self.technical_report(),
            context=[self.data_analyst_task(), self.news_researcher_task(), self.financial_analyst_task()],
            )
        
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            )