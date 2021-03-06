#140文字_280文字に生成した内容を集合に格納し、集合を送信し、test.txtに記入(更新)
import json
import requests
import tweepy
import schedule
from dotenv import load_dotenv
import os
from os.path import join, dirname
from time import sleep
import get_tweet_content_list

def post(before_tweet,before_tweet_en):

    load_dotenv(verbose=True)

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

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
    
    tweet_JA, tweet_EN = get_tweet_content_list.get_delay_info_140_280()

    #日本語版の処理
    for i in tweet_JA:
        if i in before_tweet:
            print(i)
            with open('./test.txt', mode='a+', encoding="shift-jis") as f:
                try:
                    f.write(i)                        
                except FileNotFoundError:
                    print("test.txtが存在しない、一度コード内の上部で生成しているため、errorはないはず")
        else:
            try:
                with open('./test.txt', mode='a+', encoding="shift-jis") as f:
                    print("tweet_JA\n")
                    f.write(i)
                    api_JA.update_status(i)

            except FileNotFoundError:
                print("test.txtが存在しない、一度コード内の上部で生成しているため、errorはないはず")

        #英語版の処理
    for i in tweet_EN:
        if i in before_tweet_en:
            print(i)
            with open('./test_en.txt', mode='a+') as f:
                try:
                    f.write(i)                        
                except FileNotFoundError:
                    print("test_en.txtが存在しない、一度コード内の上部で生成しているため、errorはないはず")
        else:
            try:
                with open('./test_en.txt', mode='a+') as f:
                    print("tweet_EN\n")
                    f.write(i)
                    api_EN.update_status(i)

            except FileNotFoundError:
                print("test_en.txtが存在しない、一度コード内の上部で生成しているため、errorはないはず")
