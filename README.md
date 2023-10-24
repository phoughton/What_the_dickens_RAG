# Using the OpenAI API & Chroma DB to build a Q&A Chatbot

This will answer questions on the subject of Charles Dickens' books.

It uses a Chroma DB instance created using the commands below.

## Setup

```bash
pip install -r requirements.txt
```

Add the OpenAI API key to the .env file
```
API_KEY="sk-YOUR_API_KEY
ORG_ID="org-YOUR ORG_ID"
```
You can get these from the OpenAI site, warning: you will be charged for your requests to their API.

## Run the setup code

```bash
python db_pop.py
```

This will slice up some of the files in the data_in folder. 

## What does it do?

`db_pop.py` will load several files into a Chroma Vector Database, persisted to the file system.

A log of the sections created from the input files will be placed the logs folder.

It will create embeddings from the blocks of text ('sections') and then place these and some identifiers into Chroma DB. The Chroma DB API handles the creation of embeddings, this is using a free model that is automatically downloaded at runtime. 

## Run the Q&A Chatbot
And then you can start the Q&A Chatbot with:

```bash
python chatty.py
```

Under the hood, the `db_query.py` will execute a query on that db, and `chatty.py` handles the user and LLM prompting and presentation.

The LLM used is GPT4 from Open AI. Hence the need for the OpenAI API key (see above).
