import openai
import sqlalchemy
import pandas as pd
from dotenv import load_dotenv
import os
import logging
import time

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

connection_string = (
    "mssql+pyodbc://democloud:erpDubai@150.129.119.226/FactsERP-DemoCLOUD?driver=ODBC+Driver+17+for+SQL+Server"
)
engine = sqlalchemy.create_engine(connection_string)

def fetch_data(table_name, row_limit):
    query = f"""
    SELECT TOP {row_limit} * 
    FROM [{table_name}]
    ORDER BY (SELECT NULL);
    """
    with engine.connect() as conn:
        return pd.read_sql(query, conn)

def prep_data(chunk):
    chunk_summary = chunk.head(50).to_string()
    return chunk_summary[:256000]

def send_to_openai(chunk_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": chunk_text}],
            max_tokens=500,
            temperature=0.15
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        logging.error(f"Error during API call: {e}")
        return None

def process_data(table_name, row_limit=100):
    data = fetch_data(table_name, row_limit)
    if data.empty:
        logging.info("No data found.")
        return []

    chunk_text = prep_data(data)
    if chunk_text.strip():
        result = send_to_openai(chunk_text)
        return [result]
    return []

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        logging.info("Connected to the database successfully.")
        table_name = "StockTransaction-26Aug23-26Aug24-GPT"
        logging.info("Processing data...")

        results = process_data(table_name)

        for result in results:
            logging.info(f"Assistant Response: {result}")

        while True:
            question = input("Ask a follow-up question (or type 'exit' to quit): ")
            if question.lower() == "exit":
                break
            followup_result = send_to_openai(question)
            logging.info(f"Follow-up Response: {followup_result}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")