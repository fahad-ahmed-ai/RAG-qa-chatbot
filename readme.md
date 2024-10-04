# Open AI Q&A Chatbot Backend

## Features

- Engage users with intelligent responses using AI.
- Persistent chat history stored in MongoDB
- Utilizes the OpenAI language model for generating responses

## Prerequisites

- Python 3.10 or higher
- MongoDB database
- OpenAI API key
- LLAMA CLOUD API KEY

## Installation


1. Navigate to the project directory:


2. Create a virtual environment and activate it:

```
python -m venv env
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

4. Set up the environment variables:

Create a `.env` file in the project root directory and add the following variables:

```
OPENAI_API_KEY = 
LLAMA_CLOUD_API_KEY = 
MONGO_URI = 
DATABASE_NAME = 
```

Replace the placeholders with your actual API keys and MongoDB connection details.

## Running the Application

1. Start the FastAPI server:

```
uvicorn main:application --reload
```

The server will start running at `http://localhost:8000`.

2. Access the application in your web browser:

```
http://localhost:8000
```

You should see the "server is up and running" message.

## API Endpoints

- `POST /chat`: Ask Query to Chatbot
- `POST /knowledge`: Add Knowledge Base via PDF
## Project Structure

- `main.py`: The main entry point of the application, where the FastAPI app is defined and the routes are included.
- `routes.py`: Defines the API routes for the chat functionality.
- `prompt.py`: Defines System Prompts
- `schema.py`: Defines Pydantic Models
- `views.py`: Implements the logic for generating responses and handling chat history.
- `db.py`: Handles database operations related to MongoDB.
- `config.py`: Loads the environment variables and defines the configuration settings.
- `responses.py`: Provides utility functions for generating success and error responses.
