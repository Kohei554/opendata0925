import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

api_key=os.getenv("API_KEY")

    # ここに取得したキーを書く
CONSUMER_KEY = os.getenv("TWITTER_API_KEY_JP")
CONSUMER_TOKEN = os.getenv("TWITTER_API_KEY_SECRET_JP")
ACCESS_KEY = os.getenv("ACCESS_TOKEN_JP")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN_SECRET_JP")

print(api_key)
print(CONSUMER_KEY)
