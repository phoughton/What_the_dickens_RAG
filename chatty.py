from decouple import config
import db_query
import openai


openai.api_key = config("API_KEY")
THE_SCORER_URL = str(config("SCORING_URL"))

message_flow = [
    {
        "role": "system", "content": """
You are an expert on Charles Dickens, and you are talking to a student who is studying English literature.
You will reply politely and informative to the student's questions.
"""}
]

# Ask the user to input a question about the works of Charles Dickens
question = input("Ask me a question about the works of Charles Dickens: ")

relavent_data = db_query.get_chroma_response(question)
