# Advanced Cryptocurrency Analysis Dashboard

DEVELOPING A CRYPTO FINANCIAL ANALYST. THIS IS NOT A USED FOR FINANCIAL ADVICE!

![Bitcoin](images/bitcoin.png)

## :hammer_and_wrench: Setup

To setup this project on your local machine, follow the below steps:
1. Clone this repository: <code>git clone github.com/EngBaz/Financial-Multi-Agent-Analyst</code>

2. Create a virtual enviromnent
   ```console
    $ python -m venv .venv
    $ .venv\Scripts\activate.bat
    ```
3. Install the required dependencies by running <code>pip install -r requirements.txt</code>

4. Obtain an API key from OpenAI, Cohere AI and Groq. Store the APIs in a <code>.env</code> file as follows:
    ```console
    
    $ OPENAI_API_KEY="your api key"
    $ GROQ_API_KEY="your api key"
    $ SERPER_API_KEY="your api key"
    ```
5. run the streamlit app: <code> streamlit run main.py </code>

## Implementation

The application is structured using AI agents, each specializing in a particular aspect of cryptocurrency analysis:

1- <code>Data Collector Agent:</code> Gathers historical price data and key financial metrics

2- <code>Crypto Researcher Agent:</code> Scrapes the web for whitepapers, team details, and project credibility

3- <code>Fundamental Analysis Agent:</code> Assesses a cryptocurrency’s vision, team, partnerships, and long-term potential

4- <code>Technical Analysis Agent:</code> Calculates key technical indicators (SMA 50, SMA 200) and identifies market trends

5- <code>Financial Analyst Agent:</code> Integrates fundamental and technical data to suggest investment strategies

6- <code>Reporting Agent:</code> Generates a comprehensive summary based on all analyses
