from decouple import config
import json
import db_query
import openai


openai.api_key = config("API_KEY")
THE_SCORER_URL = str(config("SCORING_URL"))


def extract_context_additions(data: dict) -> str:
    """Extracts the context additions from the data"""
    context_additions = ""
    for index, doc in enumerate(data["documents"]):
        the_id = data["ids"][0][index]
        context_additions = the_id + f": {doc}"
    return context_additions


question = input("Ask me a question about the works of Charles Dickens: ")

relavent_data = db_query.get_chroma_response(question)
print()
print(json.dumps(relavent_data, indent=4))
print()

context_additions = extract_context_additions(relavent_data)

msg_flow = [
        {
            "role": "assistant", "content": 
f"""You will answer the following question or statement in 3 back ticks: ```{question}```
The response should be based on the following paragraphs from the book, contained in the 3 back ticks:```{context_additions}```
Make the response sound authoritative and use the  data aprovided above to answer the question."""}
    ]

print()
print(json.dumps(msg_flow, indent=4))
print()
print()

response = openai.ChatCompletion.create(
    model="gpt-4-0613",
    messages=msg_flow,
    temperature=0,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)
if "choices" not in response:
    print("Sorry no answer in the response from ChatGPT")
else:
    print(response.get("choices")[0].get("message").get("content"))
