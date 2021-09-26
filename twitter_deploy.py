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

def job():

    load_dotenv(verbose=True)

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)


    # ここに取得したキーを書く
    api_key=os.getenv("API_KEY")

    CONSUMER_KEY = os.getenv("TWITTER_API_KEY_JP")
    CONSUMER_TOKEN = os.getenv("TWITTER_API_KEY_SECRET_JP")
    ACCESS_KEY = os.getenv("ACCESS_TOKEN_JP")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN_SECRET_JP")

    print(api_key)
    print(CONSUMER_KEY)


    api_key=os.getenv("API_KEY")

    # ここに取得したキーを書く
    CONSUMER_KEY = os.getenv("TWITTER_API_KEY_JP")
    CONSUMER_TOKEN = os.getenv("TWITTER_API_KEY_SECRET_JP")
    ACCESS_KEY = os.getenv("ACCESS_TOKEN_JP")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN_SECRET_JP")

    # tweepyによるOAuth認証処理
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_TOKEN)
    auth.set_access_token(ACCESS_KEY, ACCESS_TOKEN)
    api = tweepy.API(auth)
    print(api_key)
    print(CONSUMER_KEY)


    #tweet内容のopendataのjsonデータをから取り出し
    key="&acl:consumerKey="
    http="https://api-tokyochallenge.odpt.org/api/v4/odpt:TrainInformation?"
    #conditions="&owl:sameAs=odpt.TrainInformation:JR-East.ChuoRapid"
    conditions=""
    train_url = http+conditions+key+str(api_key)
    url = requests.get(train_url)
    text = url.text
    #print(text)

    context=""
    before_context=""


    #before_before_context=""

    data = json.loads(text)

    for i in range(len(data)):
        
        if (21 < len(data[i]['odpt:trainInformationText']['ja'])):
            context += data[i]['owl:sameAs'] + '  ' + data[i]['odpt:trainInformationText']['ja'] + "\n" 
            
        if (len(context) > 140 ):
            
            #api.update_status(before_context)
            context=""
        before_context=context

    if context=="":
        # print("No changes")
        api.update_status("if",random.random())
        # api.update_status("if分の方",context)

    else:
        #ツイートの実行
        api.update_status("else",random.random())
        # print("Yes changes")
        # api.update_status("else分の方",context)
        #print(context)



def main():
    # schedule.every(5).minutes.do(job)
    schedule.every(1).seconds.do(job)
    # schedule.every(3).hours.do(job)

    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == '__main__':
    main()
