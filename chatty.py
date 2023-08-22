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


msg_flow = [
    {
        "role": "system", "content": """
You will provide relevent search terms that can be used for a vector db function call.
"""}
]

question = input("Ask me a question about the works of Charles Dickens: ")

msg_flow.append({"role": "user",
                 "content": "This will be my query to the vector database of documents or books." +
                 "Use the following text, in 3 back ticks " +
                 f"```{question}``` to phrase search criteria to for the vector db of documents."
                 "The vectoir db will return the most relevent documents and be called in a function"})
functions = [
    {
        "name": "do_vector_db_query",
        "description": "Queries the vector database",
        "parameters": {
            "type": "object",
            "properties": {
                "search_criteria": {
                    "type": "string",
                    "description": "The search criteria for the query",
                }
            },
            "required": ["search_criteria"],
        }
    }
]


response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=msg_flow,
    functions=functions,
    function_call="auto",
    temperature=0,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

print(response)
function = response["choices"][0]["message"]["function_call"]
if function.get("name") == "do_vector_db_query":
    query_criteria = function.get("arguments")
    # relavent_data = db_query.get_chroma_response(question)
    criteria = json.loads(query_criteria)["search_criteria"]
    relavent_data = db_query.get_chroma_response(criteria)
    print()
    print(json.dumps(relavent_data, indent=4))
    print()

    context_additions = extract_context_additions(relavent_data)

    msg_flow2 = [
        {
            "role": "assistant", "content": f"""
            You will answer the following question: \"{question}\""

            Using the following information provided in JSON:

            {context_additions}
            
            Make the response sound authoritative and use the  data aprovided above to answer the question.
            """}
    ]

    print()
    print(json.dumps(msg_flow2, indent=4))
    print()

    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=msg_flow,
        temperature=0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response)
else:
    print("No function call was made")
