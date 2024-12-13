import openai
from dotenv import find_dotenv, load_dotenv
import time
import logging
from datetime import datetime

load_dotenv()

# Set up OpenAI API client
client = openai.OpenAI()
model = "gpt-4o-mini"

# # Create the assistant
# assistant = client.beta.assistants.create(
#     name="Stock Transaction Assistant",
#     instructions="""
#     You are an intelligent assistant that helps analyze stock transaction data. 
#     You can calculate total profit, identify items to reorder based on thresholds, and provide inventory insights. 
#     The data is in a tabular format with columns like 'Item', 'Stock', 'Price', 'Cost', 'Transactions'.
#     """,
#     model=model,
# )
# assistant_id = assistant.id
# print(f"Assistant ID: {assistant_id}")

# # Create a thread for user interactions
# thread = client.beta.threads.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Which items need to be reordered if the threshold is 50?",
#         }
#     ]
# )
# thread_id = thread.id
# print(f"Thread ID: {thread_id}")

# Hardcoded Assistant and Thread IDs
assistant_id = "generated_assistant_id"
thread_id = "generated_thread_id"

# Send a user message to the assistant
user_message = "Can you make a simple PPT for the items present in the data in .pptx format and I can download??"
message = client.beta.threads.messages.create(
    thread_id=thread_id, role="user", content=user_message
)

# Run the assistant
run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id,
    instructions="Please address the user as Akash.",
)

# Function to wait for the run to complete
def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    while True:
        try:
            run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            logging.info(f"Run status: {run_status}")
            if run_status.completed_at:
                elapsed_time = run_status.completed_at - run_status.created_at
                print(f"Run completed in {elapsed_time}")
                logging.info(f"Run completed in {elapsed_time}")

                messages = client.beta.threads.messages.list(thread_id=thread_id)
                logging.info(f"Messages: {messages.data}")

                if messages.data:
                    last_message = messages.data[-1]

                    if isinstance(last_message.content, list):
                        response = ''.join([block.value for block in last_message.content if hasattr(block, 'value')])
                    else:
                        response = last_message.content.value

                    print(f"Assistant Response: {response}")
                else:
                    print("No messages found.")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break

        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)

# Wait for the run to complete
wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)

# Retrieve and print run steps for debugging
run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
if run_steps.data:
    print(f"Steps---> {run_steps.data[0]}")
