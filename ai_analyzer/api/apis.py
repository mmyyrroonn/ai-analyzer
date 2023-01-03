import requests

class API:
    def __init__(self):
        self.endpoint = "http://43.132.164.207:22223"
    def get_all_posts(self, profile_id):
        api_url = self.endpoint + "/api/v0/publication/post?profile=" + str(profile_id)
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_all_ai_results(self, profile_id):
        api_url = self.endpoint + "/api/v0/ai/fetchResults?profile=" + str(profile_id)
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def update_ai_results(self, profile_id, raw_results, refined_results):
        api_url = self.endpoint + "/api/v0/ai/updateResults"
        request_body = {
            'post_ids': list(refined_results.keys()),
            'profile': profile_id,
            'raw': raw_results,
            'refined': refined_results
        }
        print("AI results are {}".format(request_body))
        response = requests.post(api_url, json=request_body)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def fetch_next_waiting_profile(self):
        api_url = self.endpoint + "/api/v0/ai/fetchProfile"
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def update_profile_status(self, id):
        api_url = self.endpoint + "/api/v0/ai/updateProfile?id=" + str(id)
        response = requests.post(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None