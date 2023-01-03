# from pychatgpt import Chat
import openai
import time
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir,os.path.pardir,'.env'))
load_dotenv(dotenv_path=dotenv_path)

class AIAnalyzer:
    def __init__(self, email = None, password = None, proxies: str or dict = None):
        # Initializing the chat class will automatically log you in, check access_tokens
        # self.chat = Chat(email = email, password = password, proxies = proxies)
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def query_key_words_for_post(self, prompt: str):
        if prompt is None:
            raise AIAnalyzerException("Enter a prompt.")

        if not isinstance(prompt, str):
            raise AIAnalyzerException("Prompt must be a string.")

        if len(prompt) == 0:
            raise AIAnalyzerException("Prompt cannot be empty.")

        question = "Please summary three keys words for the following paragraph and split it with comma: "

        full_prompt = question + prompt

        completion = openai.Completion.create(
            model="text-davinci-003",
            prompt=full_prompt,
            max_tokens=256,
            temperature=0.2
        )
        return completion["choices"][0]["text"]

    def refine_text_and_split(self, text):
        filtered_keywords = [ item for item in text if (not item.startswith('000')) and len(item)!=0]
        refined_keywords = [ item.strip().strip('\\n').strip("Keywords:").strip() for item in filtered_keywords]
        splited_keywords = []
        for data in refined_keywords:
            splited_keywords.extend(data.split(','))
        refined_splited_keywords = [ item.strip().strip('\\n').strip() for item in splited_keywords]
        return refined_splited_keywords

    def query_key_words_for_content(self, content):
        raw_results = {}
        for key, value in content.items():
            print("[OpenAI] Doing query for {}".format(key))
            try:
                rst = self.query_key_words_for_post(value)
                raw_results[key] = rst
            except Exception as e:
                print(e)
            time.sleep(3)
        return raw_results

class AIAnalyzerException(Exception):
    def __init__(self, message):
        self.message = message