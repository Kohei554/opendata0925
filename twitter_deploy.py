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
import get_before_tweet
import get_before_tweet_en
import one_line
import one_line_en
import translate
import post


def job():

    load_dotenv(verbose=True)

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    #Tokyo_Open_Data_APIKEY
    api_key=os.getenv("API_KEY")

    # ここに取得した日本のtwitterキーを書く
    CONSUMER_KEY_JA = os.getenv("TWITTER_API_KEY_JP")
    CONSUMER_TOKEN_JA = os.getenv("TWITTER_API_KEY_SECRET_JP")
    ACCESS_KEY_JA = os.getenv("ACCESS_TOKEN_JP")
    ACCESS_TOKEN_JA = os.getenv("ACCESS_TOKEN_SECRET_JP")


    # ここに取得した日本のtwitterキーを書く
    CONSUMER_KEY_EN = os.getenv("TWITTER_API_KEY_EN")
    CONSUMER_TOKEN_EN = os.getenv("TWITTER_API_KEY_SECRET_EN")
    ACCESS_KEY_EN = os.getenv("ACCESS_TOKEN_EN")
    ACCESS_TOKEN_EN = os.getenv("ACCESS_TOKEN_SECRET_EN")


    #日本のアカウントの方tweepyによるOAuth認証処理
    auth_JA = tweepy.OAuthHandler(CONSUMER_KEY_JA, CONSUMER_TOKEN_JA)
    auth_JA.set_access_token(ACCESS_KEY_JA, ACCESS_TOKEN_JA)
    api_JA = tweepy.API(auth_JA)

    #英語のアカウントの方tweepyによるOAuth認証処理
    auth_EN = tweepy.OAuthHandler(CONSUMER_KEY_EN, CONSUMER_TOKEN_EN)
    auth_EN.set_access_token(ACCESS_KEY_EN, ACCESS_TOKEN_EN)
    api_EN = tweepy.API(auth_EN)



    #各路線の日本語生成
    dic = create_dict.get_dict()

    #tweet内容のopendataのjsonデータをから取り出し
    http="https://api-tokyochallenge.odpt.org/api/v4/odpt:TrainInformation?acl:consumerKey="
    train_url = http+str(api_key)
    url = requests.get(train_url)
    text = url.text

    data = json.loads(text)

    #以前に投稿した140文字の集合を獲得
    before_tweet=get_before_tweet.get_before_tweet()
    #以前に投稿した280文字のenの集合を獲得
    before_tweet_en=get_before_tweet_en.get_before_tweet_en()

    post.post(before_tweet,before_tweet_en)
    

def main():
    schedule.every(10).minutes.do(job)
    # schedule.every(5).seconds.do(job)
    # schedule.every(3).hours.do(job)

    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == '__main__':
    main()
