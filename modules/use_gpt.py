import openai
import os


# load_dotenv()
# openai.api_key = os.getenv("openai_api_key")

def gpt_api(prompt,openai_api_key):
    openai.api_key = openai_api_key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.01,
        max_tokens=1000,
        top_p=0.1,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    # return response["choices"][0]["text"].replace("\n',")
    # return response
    return response["choices"][0]["text"].replace("\n", "")

