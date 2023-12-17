import os
import time
import openai
from dotenv import load_dotenv
from ratelimit import limits, sleep_and_retry

load_dotenv(override=True)
openai.api_key = os.getenv("OPENAI_API_KEY")

@sleep_and_retry
@limits(calls=int(os.getenv("OPENAI_RATE_LIMIT")), period=int(os.getenv("OPENAI_TIMEOUT_INTERVAL")))
def call_openai_api(input_data):
    return openai.ChatCompletion.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that translates JSON objects."
            },
            {
                "role": "user",
                "content": input_data
            }
        ],
        temperature=float(os.getenv("OPENAI_TEMPERATURE")),
        max_tokens=int(os.getenv("OPENAI_MAX_TOKENS")),
        top_p=float(os.getenv("OPENAI_TOP_P")),
        frequency_penalty=float(os.getenv("OPENAI_FREQUENCY_PENALTY")),
        presence_penalty=float(os.getenv("OPENAI_PRESENCE_PENALTY"))
    )
