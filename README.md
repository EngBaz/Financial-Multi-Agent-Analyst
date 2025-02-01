# AI Financial Analyst Bot

Note: You need to know the cryptocurrency's ticker name for a better analysis.

## Overview

### What is AI Financial Analyst Bot?
The AI Financial Analyst Bot is an intelligent application designed to provide comprehensive financial analysis and insights for any given cryptocurrency. 
It leverages OpenAI's GPT models for analysis, yfinance for historical cryptocurrency data, and serper for news retrieval.

### Why is it Useful?
Investing in the cryptocurrency market often requires hours of research, financial literacy, and keeping up with news. 
This bot automates these tasks by providing a one-stop solution for all your research needs. 
It not only provides raw data but also offers AI-powered insights to make your investment decisions more informed.

## Setup

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

## :robot: Implementation

The application is structured using AI agents, each specializing in a particular aspect of cryptocurrency analysis:

1- <code>Data Collector Agent:</code> Gathers historical price data and key financial metrics

2- <code>Crypto Researcher Agent:</code> Scrapes the web for general information on a specific cryptocurrency

3- <code>Fundamental Analysis Agent:</code> Assesses a cryptocurrency’s vision, team, partnerships, and long-term potential

4- <code>Technical Analysis Agent:</code> Calculates key technical indicators (SMA 50, SMA 200) and identifies market trends

5- <code>Financial Analyst Agent:</code> Integrates fundamental and technical data to suggest investment strategies

6- <code>Reporting Agent:</code> Generates a comprehensive summary based on all analyses

## :hammer_and_wrench: Technologies used

* Python
* Streamlit
* CrewAI
* Docker
* Yahoo finance
* Serper
