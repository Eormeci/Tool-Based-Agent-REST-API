# Tool-Based Agent Developed with Flask using LangChain and ChromaDB Database

This Flask application is a web application that includes a calculator, vector similarity search, and question answering functionalities using the "gemma-1.1-7b-it" model.

## Features
- Users can perform four operations with the calculator.
- Users can utilize vector similarity search to find values closest to the desired value within the dataset of their choice.
- Users can ask questions locally and benefit from the answers provided by the "gemma-1.1-7b-it" model.

## Installation
# Clone the repo
git clone https://github.com/Eormeci/Tool-Based-Agent-REST-API.git
cd Tool-Based-Agent-REST-API
# Create and activate a Python virtual environment:
python -m venv venv
venv\Scripts\activate
# Install the required dependencies:
pip install -r requirements.txt
# Run the API
python app.py

## Usage
# For the vector search part
- Users can upload any CSV file and enter a value to search.
- I created a dataset myself using ChatGPT 3.5.
# For the question answering part
- Users can ask any question. ("how do .. works", "what is the tallest building in the world" etc.)
