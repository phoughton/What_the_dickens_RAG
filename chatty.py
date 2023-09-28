from decouple import config
import argparse
import time
import sys
import db_query
import openai


parser = argparse.ArgumentParser(
    description='Chat with a Charles Dickens expert.')

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


def type_text(text: str) -> None:
    """Types the text out on the screen"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)


def extract_context_additions(data: dict) -> str:
    """Extracts the context additions from the data"""
    context_additions = ""

    for index, doc in enumerate(data["documents"][0]):
        the_id = data["ids"][0][index]
        context_additions += the_id + f": {doc}\n\n"
    return context_additions


type_text("Hello, I'm an AI with access to the works of Charles Dickens. "
          "I can answer questions about his work")

while True:
    question = input(": ")
    if question in ["exit", "quit", ""]:
        break

    relavent_data = db_query.get_chroma_response(question)

    context_additions = extract_context_additions(relavent_data)

    if args.verbose:
        print("\nContext additions: ")
        print(context_additions)
        print()

    msg_flow = [
        {
            "role": "system",
            "content": ("You are a expert librarian. You will answer "
                        "questions about his works based only on the "
                        "extracts provided by the assistant. You will "
                        "not use your own knowledge. If the extracts "
                        "mention subject or action that you do not "
                        "know about, you will not make up an answer.")
        },
        {
            "role": "assistant",
            "content":
                "The response should be based only on the following sections from the books, contained between these back ticks:\n"  # noqa: E501
                f"```{context_additions}```\n"  # noqa: E501
                "Make the response sound authoritative and use the data provided above to answer the question.\n"  # noqa: E501
                "Quote the extracts provided if needed. The quotes must exactly match the extracts provided.\n"  # noqa: E501
                "Do not comment on the accuracy of the extracts provided or if they are anachronistic.\n"  # noqa: E501
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
            print("Sorry, I can't answer that question, "
                  "please try rephrasing your question.")
        else:
            answer = response.get("choices")[0].get("message").get("content")

            type_text(answer)

    print()
