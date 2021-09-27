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

total=""
num=0

def job():

    load_dotenv(verbose=True)

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

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
    # print(api_key)
    # print(CONSUMER_KEY)



    #日本語に変換する辞書型を入手する
    http_railway="https://api-tokyochallenge.odpt.org/api/v4/odpt:Railway?acl:consumerKey="+str(api_key)
    url_railwai = requests.get(http_railway)
    text_railway = url_railwai.text
    #print(text)
    dic={}
    data_raiilway = json.loads(text_railway)
    for i in range(len(data_raiilway)):
        a=data_raiilway[i]['owl:sameAs']
        #print(a)
        l=re.findall('odpt.Railway:(.*)', a).pop()
        moji='odpt.TrainInformation:'+l
        dic[moji]=data_raiilway[i]['dc:title']
    # print(dic)



    #tweet内容のopendataのjsonデータをから取り出し
    http="https://api-tokyochallenge.odpt.org/api/v4/odpt:TrainInformation?acl:consumerKey="
    train_url = http+str(api_key)
    url = requests.get(train_url)
    text = url.text
    #print(text)
    #global total
    #global num
    total_context=""
    context=""
    before_context=""

    #before_before_context=""

    data = json.loads(text)

    for i in range(len(data)):

        if (len(context) > 140 ):
            api.update_status(before_context)
            context=""

        before_context=context
        
        if (21 < len(data[i]['odpt:trainInformationText']['ja'])):
            if data[i]['owl:sameAs'] in dic:
                context += dic[data[i]['owl:sameAs']] + '  ' + data[i]['odpt:trainInformationText']['ja'] + "\n" 
                # total_context += dic[data[i]['owl:sameAs']] + '  ' + data[i]['odpt:trainInformationText']['ja'] + "\n" 
            else:
                context += data[i]['owl:sameAs'] + '  ' + data[i]['odpt:trainInformationText']['ja'] + "\n" 
                # total_context += data[i]['owl:sameAs'] + '  ' + data[i]['odpt:trainInformationText']['ja'] + "\n" 

        #total_contextに追加しているのは以前と内容が同じか判断するため
        else:
            if data[i]['owl:sameAs'] in dic:
                total_context += dic[data[i]['owl:sameAs']] + '  ' + data[i]['odpt:trainInformationText']['ja'] + "\n" 
            else:
                total_context += data[i]['owl:sameAs'] + '  ' + data[i]['odpt:trainInformationText']['ja'] + "\n" 


    if context=="":
        print("No changes")
        # print(total_context)
        # api.update_status("if分の方",context)

    #以前の投稿と同じ内容か判断
    # elif total == total_context:
    #     num+=1
    #     api.update_status(str(num)+"以前の遅延状態が継続しています")

    else:
        # print(total_context)
        #ツイートの実行
        # api.update_status("else",random.random())
        api.update_status(context)

    # total=total_context


def main():
    # schedule.every(5).minutes.do(job)
    # schedule.every(1).seconds.do(job)
    schedule.every(5).hours.do(job)

    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == '__main__':
    main()
