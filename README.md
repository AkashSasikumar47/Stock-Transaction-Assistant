# Stock Transaction Assistant

This project demonstrates the creation and use of an AI assistant powered by OpenAI's API to analyze stock transaction data. The assistant can perform tasks such as identifying items to reorder, calculating total profit, and providing inventory insights.

## Features
- Uses OpenAI's GPT-3.5 Turbo model.
- Handles stock transaction queries like reorder thresholds and profit analysis.
- Interactive and customizable assistant.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/AkashSasikumar47/stock-transaction-assistant.git
   cd stock-transaction-assistant
2. **Install Dependencies**: Ensure you have Python installed, then install the required packages:
   ```bash
   pip install openai python-dotenv
3. **Set Up Environment Variables**:
   - Create a `.env` file in the root directory.
   - Add your OpenAI API key in the following format:
     ```env
     OPENAI_API_KEY=your_api_key_here
     ```
4. **Run the Script**:  
   Execute the Python script:  
   ```bash
   python main.py
## How It Works

1. **Assistant Initialization**: Creates a custom AI assistant with predefined instructions.
2. **User Interaction**: Sends queries like "Which items need to be reordered if the threshold is 50?" to the assistant.
3. **Response Handling**: Retrieves and displays responses from the assistant.

## License

This project is licensed under the MIT License. Feel free to use and modify it as needed.
