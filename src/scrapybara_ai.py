import os
from scrapybara import Scrapybara

def get_scrapybara_client():
    api_key = os.environ.get("SCRAPYBARA_API_KEY")
    return Scrapybara(api_key=api_key)
