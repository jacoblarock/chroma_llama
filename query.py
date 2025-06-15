from ollama import chat, ChatResponse
import json
import db_cols

model = "llama3.1:8b"

def get_context_needed(query: str) -> list[str]:
    with open("prompts/additional_context") as file:
        prompt = file.read().replace("{user_query}", f'"{query}"')
    try:
        response: ChatResponse = chat(
            model=model,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        message = str(response.message.content)
        message = message[message.find("["):message.find("]")] + "]"
        message = list(json.loads(message))
    except Exception as e:
        print(e)
        message = []
    return message

def answer_with_context(query: str, context: list | None, print_stream: bool = False):
    with open("prompts/answer_with_context") as file:
        prompt = file.read().replace("{user_query}", f'"{query}"').replace("{context}", str(context))
    response: ChatResponse = chat(
        model=model,
        messages=[{
            "role": "user",
            "content": prompt
        }],
        options={
            "num_ctx": 8192
        },
        stream=print_stream
    )
    message = ""
    if print_stream:
        for chunk in response:
            message += chunk.message.content
            print(chunk.message.content, end="", flush=True)
    else:
        message = response.message.content
    return message

if __name__ == "__main__":
    query = input()
    keywords = get_context_needed(query)
    print(keywords)
    client = db_cols.load_client("client")
    col = client.get_collection("default")
    context = db_cols.query(col, keywords)
    print(len(str(context)))
    answer = answer_with_context(query, context, print_stream=True)
    print(answer)