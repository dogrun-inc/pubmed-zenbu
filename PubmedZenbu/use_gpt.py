import openai

# load_dotenv()
# openai.api_key = os.getenv("openai_api_key")

def gpt_api(prompt,openai_api_key):
    openai.api_key = openai_api_key
    response = openai.Completion.create(
        engine="gpt-4-1106-preview", #text-davinci-003 has been deprecated https://platform.openai.com/docs/deprecations
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

def gpt4_api(prompt, openai_api_key):
    openai.api_key = openai_api_key
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",  
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,  
        temperature=0.01,  
        frequency_penalty=0.0, 
        presence_penalty=0.0  
    )
    # return response["choices"][0]["text"].replace("\n',")
    # return response
    return response["choices"][0]["message"]["content"].replace("\n", "")
