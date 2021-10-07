#140文字_280文字に生成した内容を集合に格納し、集合を返す
import json
import requests
import tweepy
import schedule
from dotenv import load_dotenv
import os
from os.path import join, dirname
from time import sleep
import re
import random
import create_dict
import one_line
import one_line_en
import translate

def confirm():

    load_dotenv(verbose=True)

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    #Tokyo_Open_Data_APIKEY
    api_key=os.getenv("API_KEY")

    #tweet内容のopendataのjsonデータをから取り出し
    http="https://api-tokyochallenge.odpt.org/api/v4/odpt:TrainInformation?acl:consumerKey="
    train_url = http+str(api_key)
    url = requests.get(train_url)
    text = url.text

    data = json.loads(text)
    o=0

    for i in data:
        print(i['odpt:trainInformationText']['ja'])
        o=o+1

    print(o)
    print(len(data))

if __name__ == '__main__':
    print(confirm()) 


