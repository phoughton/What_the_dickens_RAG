# Using the OpenAI API & Chroma DB to build a Q&A Chatbot

This will answer questions on the subject of Charles Dickens books.

## Setup

```bash
pip install -r requirements.txt
```

Add the OpenAI API key to the .env file
```
API_KEY="sk-YOUR_API_KEY
ORG_ID="org-YOUR ORG_ID"
```


## Run the setup code

```bash
python db_pop.py
```

## What does it do?

`db_pop.py` will load several files into a Chroma Vector Database, persisted to the file system.


## Run the Q&A Chatbot
And then you can start the Q&A Chatbot with:

```bash
python chatty.py
```

Under the hood, the `db_query.py` will execute a query on that db, and `chatty.py` handles the user and LLM prompting and presentation.
