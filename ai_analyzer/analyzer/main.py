# from pychatgpt import Chat
import openai
import time
import os
from dotenv import load_dotenv
import json
import ast
from tenacity import retry, stop_after_attempt, wait_random_exponential, RetryError
import random

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir,os.path.pardir,'.env'))
load_dotenv(dotenv_path=dotenv_path)

class AIAnalyzer:
    def __init__(self, email = None, password = None, proxies: str or dict = None):
        # Initializing the chat class will automatically log you in, check access_tokens
        # self.chat = Chat(email = email, password = password, proxies = proxies)
        self.api_keys = os.getenv('OPENAI_API_KEY').split(',')

    def query_key_words_for_post_with_davinci(self, prompt: str):
        if prompt is None:
            raise AIAnalyzerException("Enter a prompt.")

        if not isinstance(prompt, str):
            raise AIAnalyzerException("Prompt must be a string.")

        if len(prompt) == 0:
            raise AIAnalyzerException("Prompt cannot be empty.")

        question = "Please summary three keys words for the following paragraph and split it with comma: "

        full_prompt = question + prompt

        openai.api_key = random.choice(self.api_keys)
        completion = openai.Completion.create(
            model="text-davinci-003",
            prompt=full_prompt,
            max_tokens=256,
            temperature=0.2
        )
        return completion["choices"][0]["text"]

    def query_key_words_for_post(self, prompt: str):
        if prompt is None:
            raise AIAnalyzerException("Enter a prompt.")

        if not isinstance(prompt, str):
            raise AIAnalyzerException("Prompt must be a string.")

        if len(prompt) == 0:
            raise AIAnalyzerException("Prompt cannot be empty.")

        question = "Summary three keys words for the paragraph and split it with comma: "

        full_message = [
            {"role": "system", "content": "You are a helpful assistant that summary the key words from the content"},
            {"role": "user", "content": question + prompt}
        ]
        openai.api_key = random.choice(self.api_keys)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=full_message,
            max_tokens=512,
            temperature=0.2
        )
        return completion["choices"][0]["message"]["content"]

    @retry(wait=wait_random_exponential(min=20, max=60), stop=stop_after_attempt(3))
    def query_key_words_for_multi_post(self, prompt: str):
        if prompt is None:
            raise AIAnalyzerException("Enter a prompt.")

        if not isinstance(prompt, str):
            raise AIAnalyzerException("Prompt must be a string.")

        if len(prompt) == 0:
            raise AIAnalyzerException("Prompt cannot be empty.")

        system_role = "You are a helpful assistant that summary the key words from the contents. \
            The contents would be given in a dict string, the key is the index and the value is the content, such as \{'0': 'I'm a dog', '1': 'You're a chat'\}\
            Summary three keys words for each item in the list and split it with comma.\
            The response should be in a list that can be used in ast.literal_eval, such as ['I, a, dog', 'you, a, chat'].\
            The number of the response should be same with the dict length"

        full_message = [
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt}
        ]
        openai.api_key = random.choice(self.api_keys)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=full_message,
            max_tokens=512,
            temperature=0.2
        )
        return completion["choices"][0]["message"]["content"]

    def refine_text_and_split(self, text):
        filtered_keywords = [ item for item in text if (not item.startswith('000')) and len(item)!=0]
        refined_keywords = [ item.strip().strip('\\n').strip("Keywords:").strip().rstrip('.') for item in filtered_keywords]
        splited_keywords = []
        for data in refined_keywords:
            splited_keywords.extend(data.split(','))
        refined_splited_keywords = [ item.strip().strip('\\n').strip() for item in splited_keywords]
        return refined_splited_keywords

    # def query_key_words_for_content(self, content):
    #     for key, value in content.items():
    #         print("[OpenAI] Doing query for {}".format(key))
    #         try:
    #             rst = self.query_key_words_for_post(value)
    #             yield key, rst
    #         except Exception as e:
    #             print(e)
    #         time.sleep(6)

    def query_key_words_for_content(self, content):
        for index, value in content.items():
            print("[OpenAI] Doing query for {}".format(value["ids"]))
            try:
                rst = self.query_key_words_for_multi_post(json.dumps({i: val for i, val in enumerate(value["contents"])}))
                yield index, value["ids"], ast.literal_eval(rst)
            except RetryError as e:
                print("Execution failed after multiple retries")
            except openai.error.InvalidRequestError as e:
                print(e)
            except Exception as e:
                print(e)
            time.sleep(3)

class AIAnalyzerException(Exception):
    def __init__(self, message):
        self.message = message