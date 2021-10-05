from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
import requests
import tweepy
import schedule
from dotenv import load_dotenv
import os
from os.path import join, dirname
from time import sleep


def translate(text):
    load_dotenv(verbose=True)

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    IBM_ENDPOINT = "https://api.jp-tok.language-translator.watson.cloud.ibm.com/instances/1f098ad2-36bc-4be2-9233-279c270a3e89"
    IBM_API_KEY = os.getenv("IBM_API_KEY")

    if ("平常" in text) or (text == "現在、１５分以上の遅延はありません。"):
        return "Service on schedule"
    model_id = 'ja-en'

    # Prepare the Authenticator
    authenticator = IAMAuthenticator(IBM_API_KEY)
    language_translator = LanguageTranslatorV3(
        version='2018-05-01',
        authenticator=authenticator
    )
    language_translator.set_service_url(IBM_ENDPOINT)

    # Translate
    translation = language_translator.translate(
        text=text,
        model_id=model_id).get_result()

    return json.loads(json.dumps(translation))["translations"][0]["translation"]

if __name__ == '__main__':
    print(translate("write a mail")) 