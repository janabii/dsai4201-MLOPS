# support_bot/mistral_client.py
import os
from mistralai import Mistral, UserMessage


def mistral(user_message: str, model: str = "mistral-small-latest", is_json: bool = False) -> str:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise RuntimeError("Missing MISTRAL_API_KEY. Set it in your environment.")

    client = Mistral(api_key=api_key)

    messages = [UserMessage(content=user_message)]
    chat_response = client.chat.complete(
        model=model,
        messages=messages,
    )

    return chat_response.choices[0].message.content
