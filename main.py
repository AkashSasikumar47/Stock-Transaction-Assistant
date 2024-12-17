import openai
from dotenv import find_dotenv, load_dotenv
import time
import logging
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API client
openai.api_key = "your_openai_api_key_here"  # Ensure your OpenAI API key is loaded correctly

# Define the model to use
model = "gpt-4o-mini"

# Hardcoded Assistant and Thread IDs (replace these with actual generated values)
assistant_id = "generated_assistant_id"
thread_id = "generated_thread_id"

# Function to ask the assistant a question
def ask_question(thread_id, assistant_id, question):
    try:
        # Send the user's question to the assistant thread
        user_message = openai.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=question
        )

        # Create a run for the assistant to process the user's question
        run = openai.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            instructions="Please address the user as Akash."  # Customize instructions as needed
        )

        # Poll for the run status until it's completed
        while True:
            run_status = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run_status.status == "completed":
                break
            time.sleep(2)

        # Retrieve all messages from the thread
        messages = openai.beta.threads.messages.list(thread_id=thread_id)

        # Extract the assistant's response from the messages
        assistant_response = None
        for msg in messages.data:
            if msg.role == "assistant":
                assistant_response = msg.content[0].text.value if msg.content else "No content found."
                break

        # Output the response
        if assistant_response:
            print(f"Your Question: {question}")
            print(f"Assistant Response: {assistant_response}\n")
        else:
            print("No assistant response found.")
    
    except Exception as e:
        # Log any errors that occur
        logging.error(f"Error occurred: {e}")
        print(f"An error occurred: {e}")

# Main loop to continuously ask questions
while True:
    question = input("Ask your question (or type 'exit' to quit): ")
    if question.lower() == "exit":
        print("Session ended.")
        break
    ask_question(thread_id, assistant_id, question)
