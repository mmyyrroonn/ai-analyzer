import requests
import os
from os import path
from dotenv import load_dotenv
import logging

d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir,os.path.pardir,'.env'))
load_dotenv(dotenv_path=dotenv_path)

class API:
    def __init__(self):
        self.endpoint = os.getenv('API_ENDPOINT')
        self.logger = logging.getLogger("api")

    def get_all_posts(self, profile_id):
        api_url = self.endpoint + "/api/v0/publication/post?profile=" + str(profile_id)
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except:
            return None

    def get_all_ai_results(self, profile_id):
        api_url = self.endpoint + "/api/v0/ai/fetchResults?profile=" + str(profile_id)
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except:
            return None

    def update_ai_results(self, profile_id, raw_results, refined_results):
        api_url = self.endpoint + "/api/v0/ai/updateResults"
        request_body = {
            'post_ids': list(refined_results.keys()),
            'profile': profile_id,
            'raw': raw_results,
            'refined': refined_results
        }
        self.logger.info("AI results are {}".format(request_body))
        try:
            response = requests.post(api_url, json=request_body)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except:
            return None

    def fetch_next_waiting_profile(self):
        api_url = self.endpoint + "/api/v0/ai/fetchProfile"
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except:
            return None

    def update_profile_status(self, id, unprocessed):
        api_url = self.endpoint + "/api/v0/ai/updateProfile?id=" + str(id)
        request_body = {
            'unprocessed': unprocessed,
        }
        try:
            response = requests.post(api_url, json=request_body)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except:
            return None

    def fetch_next_ai_tag_profile(self):
        api_url = self.endpoint + "/api/v0/ai/fetchNextAITag"
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except:
            return None

    def push_nft(self, request_body):
        api_url = self.endpoint + "/api/v0/nft/pushNft"
        try:
            response = requests.post(api_url, json=request_body)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except:
            return None

    # def push_ai_tag_generator(self, id):
    #     api_url = self.endpoint + "/api/v0/ai/pushAITag?profile=" + str(id)
    #     try:
    #         response = requests.post(api_url)
    #         if response.status_code == 200:
    #             return response.json()
    #         else:
    #             return None
    #     except:
    #         return None
