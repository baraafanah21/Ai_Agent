import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from prompts import system_prompt

MAX_ITERATIONS = 20


def generate_content(client, messages, verbose: bool = False):
    response = client.chat.completions.create(
        model="cohere/north-mini-code:free",
        messages=messages,
        tools=available_functions,
        temperature=0,
    )

    if response.usage is None:
        raise RuntimeError(
            "No usage metadata in the response; the API request likely failed."
        )

    if verbose:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    return response


def main() -> None:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError(
            "OPENROUTER_API_KEY not found. Create a .env file in the project "
            "directory containing: OPENROUTER_API_KEY='your_api_key_here'"
        )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(MAX_ITERATIONS):
        response = generate_content(client, messages, args.verbose)
        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            print("Final response:")
            print(message.content)
            return

        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            if not result_message.get("content"):
                raise Exception(f"Empty function result for: {tool_call.function.name}")
            if args.verbose:
                print(f"-> {result_message['content']}")
            messages.append(result_message)

    print(f"Maximum iterations ({MAX_ITERATIONS}) reached without a final response.")
    sys.exit(1)


if __name__ == "__main__":
    main()
