import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompt import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument(
        "user_prompt",
        type=str,
        help="User prompt to be sent to the gemini-2.5-flash model",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    print("Hello from coding-agent!")

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0,
            ),
        )

        if response.candidates is not None:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.usage_metadata is None:
            raise RuntimeError("Response property usage_metadata is None")

        if args.verbose is True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.function_calls is not None:
            function_results = []

            for function_call in response.function_calls:
                result = call_function(function_call, args.verbose)
                if (
                    not result.parts
                    or not result.parts[0].function_response
                    or not result.parts[0].function_response.response
                ):
                    raise RuntimeError(
                        f"Empty function response for {function_call.name}"
                    )

                if args.verbose:
                    print(f"-> {result.parts[0].function_response.response}")

                function_results.append(result.parts[0])

            messages.append(types.Content(role="user", parts=function_results))

        else:
            print(response.text)
            exit(0)
    print(
        "The model could not answer your prompt in 20 iterations exiting the program."
    )
    exit(1)


if __name__ == "__main__":
    main()
