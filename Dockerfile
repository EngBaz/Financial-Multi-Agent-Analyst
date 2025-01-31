FROM python:3.12.4

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install --upgrade crewai_tools

COPY . /app

EXPOSE 8501

CMD ["streamlit", "run", "main.py"]
