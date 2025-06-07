from ollama import chat, ChatResponse
import json

def get_context_needed(query):
    with open("prompts/additional_context") as file:
        prompt = file.read().replace("{user_query}", f'"{query}"')
    try:
        response: ChatResponse = chat(
            model="llama3.1:8b",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        message = str(response.message.content)
        message = message[message.find("["):message.find("]")] + "]"
        message = json.loads(message)
    except Exception as e:
        message = {}
        print(e)
    return message

if __name__ == "__main__":
    query = input()
    print(get_context_needed(query))
