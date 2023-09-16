from decouple import config
import argparse
import time
import sys
import db_query
import openai


parser = argparse.ArgumentParser(description='Chat with a Charles Dickens expert.')

parser.add_argument('-v', '--verbose',
                    help='Show details of the query being handled',
                    required=False,
                    default=False,
                    action='store_true')
parser.add_argument('-n', '--noai',
                    help='Disable the AI and just use the database',
                    required=False,
                    default=False,
                    action='store_true')
args = parser.parse_args()

openai.api_key = config("API_KEY")
THE_SCORER_URL = str(config("SCORING_URL"))


def type_text(text: str) -> None:
    """Types the text out on the screen"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)
    print()


def extract_context_additions(data: dict) -> str:
    """Extracts the context additions from the data"""
    context_additions = ""

    for index, doc in enumerate(data["documents"][0]):
        the_id = data["ids"][0][index]
        context_additions += the_id + f": {doc}\n\n"
    return context_additions


type_text("Hello, I am a system expert in the works of Charles Dickens. I will answer questions about his works, based only on the extracts provided by the assistant.")

while True:
    question = input(":")
    if question in ["exit", "quit"]:
        break

    relavent_data = db_query.get_chroma_response(question)

    context_additions = extract_context_additions(relavent_data)

    if args.verbose:
        print("\nContext additions: ")
        print(context_additions)
        print()

    msg_flow = [
        {
            "role": "system", "content": "You are a system expert in the works of Charles Dickens. You will answer questions about his works, based only on the extracts provided by the assistant."
        },
        {
            "role": "assistant", "content":
                f"""The response should be based only on the following paragraphs from the books, contained between these back ticks:```{context_additions}```. Make the response sound authoritative and use the  data aprovided above to answer the question."""
        },
        {
            "role": "user", "content": question
        }
    ]

    if args.verbose:
        print("Message flow: ")
        print(msg_flow)
        print()

    if args.noai:

        print("AI answering is disabled.")

    else:
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=msg_flow,
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        if "choices" not in response:
            print("Sorry, I can't answer that question, pleasw try rephrasing your question.")
        else:
            answer = response.get("choices")[0].get("message").get("content")

            type_text(answer)
