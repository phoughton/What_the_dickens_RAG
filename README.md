# Simple Vector database

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

## Run the query code

```bash
python db_query.py
```

## What does it do?

`db_pop.py` will load several files into a Chroma Vector Database, persisted to the file system.

And then `db_query.py` will execute a query on that db.

