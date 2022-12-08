from pychatgpt import Chat

class AIAnalyzer:
    def __init__(self, email, password, proxies: str or dict = None):
        # Initializing the chat class will automatically log you in, check access_tokens
        self.chat = Chat(email = email, password = password, proxies = proxies)

    def query_key_words_for_post(self, prompt: str):
        if prompt is None:
            raise AIAnalyzerException("Enter a prompt.")

        if not isinstance(prompt, str):
            raise AIAnalyzerException("Prompt must be a string.")

        if len(prompt) == 0:
            raise AIAnalyzerException("Prompt cannot be empty.")

        question = "Please summary three keys words for the following paragraph or sentence: "

        full_prompt = question + prompt

        answer = chat.ask(full_prompt)
        print(answer)
        return answer


class AIAnalyzerException(Exception):
    def __init__(self, message):
        self.message = message