from decouple import config
import openai
import requests



openai.api_key = config("API_KEY")
THE_SCORER_URL = str(config("SCORING_URL"))

message_flow = [
    {
        "role": "system", "content": """
You are an expert on Charles Dickens, and you are talking to a student who is studying English literature.
You will reply politely and informative to the student's questions.
"""}
]
