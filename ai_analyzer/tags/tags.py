
import os
from os import path
from dotenv import load_dotenv

d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir,os.path.pardir,'.env'))
load_dotenv(dotenv_path=dotenv_path)

class AITagFactory:
    def __init__(self, name, description, nftid, category = "AI", provider = "NoSocial", type = "SBT"):
        self.name = name,
        self.description = description
        self.nftid = nftid
        self.category = category
        self.provider = provider
        self.type = type
        self.pic_server = os.getenv('PIC_SERVER')

    def generate_ai_tag_metadata(self, profile, pic_url):
        request_body = {
            "name": self.name,
            "description": self.description,
            "nftId": self.nftid,
            "category": self.category,
            "provider": self.provider,
            "type": self.type,
            "profileId": profile,
            "pic_url": self.pic_server+pic_url,
        }
        return request_body