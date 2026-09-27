import argparse
import os
import sys

from dotenv import load_dotenv
from openai import APIError, APITimeoutError, OpenAI, RateLimitError

from call_function import available_functions, call_function
from config import MAX_ITERATIONS, MODEL
from prompts import system_prompt


def generate_content(client, messages, model: str, verbose: bool = False):
    response = client.chat.completions.create(
        model=model,
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument(
        "--model", type=str, default=MODEL, help=f"Model ID to use (default: {MODEL})"
    )
    return parser.parse_args()


def run_agent(client, messages, args) -> int:
    total_prompt_tokens = 0
    total_response_tokens = 0

    for _ in range(MAX_ITERATIONS):
        response = generate_content(client, messages, args.model, args.verbose)
        if response.usage is not None:
            total_prompt_tokens += response.usage.prompt_tokens
            total_response_tokens += response.usage.completion_tokens

        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            print("Final response:")
            print(message.content)
            if args.verbose:
                print(
                    f"Total tokens: {total_prompt_tokens} prompt, "
                    f"{total_response_tokens} response"
                )
            return 0

        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            if not result_message.get("content"):
                raise Exception(f"Empty function result for: {tool_call.function.name}")
            if args.verbose:
                print(f"-> {result_message['content']}")
            messages.append(result_message)

    print(f"Maximum iterations ({MAX_ITERATIONS}) reached without a final response.")
    return 1


def main() -> None:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError(
            "OPENROUTER_API_KEY not found. Create a .env file in the project "
            "directory containing: OPENROUTER_API_KEY='your_api_key_here'"
        )

    args = parse_args()

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Model: {args.model}")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    try:
        sys.exit(run_agent(client, messages, args))
    except RateLimitError:
        print(
            "Error: rate limited by OpenRouter. The free tier allows ~50 requests "
            "per day; wait for the reset or try a different model with --model.",
            file=sys.stderr,
        )
        sys.exit(1)
    except APITimeoutError:
        print("Error: the request to OpenRouter timed out.", file=sys.stderr)
        sys.exit(1)
    except APIError as e:
        print(f"Error: OpenRouter request failed: {e.message}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
