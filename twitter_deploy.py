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
    context=""
    before_context=""

    context_en=""
    before_context_en=""


    data = json.loads(text)

    #以前に投稿した140文字の集合を獲得
    before_tweet=get_before_tweet.get_before_tweet()
    #以前に投稿した280文字のenの集合を獲得
    before_tweet_en=get_before_tweet_en.get_before_tweet_en()
    
    #データの取り出し
    for i in range(len(data)):

        if (len(context) > 140 ):
            #もし、以前tweetした内容と同じ場合はifでかき消されるので、num.txtの利用などで工夫して回数追加を必要がある
            if before_context in before_tweet:
                print("same_content")
                with open('./test.txt', mode='a+') as f:
                    f.write(before_context)

            else:
                try:
                    with open('./test.txt', mode='a+') as f:
                        print("tweet\n")
                        f.write(before_context)
                        api_JA.update_status(before_context)

                except FileNotFoundError:
                    print("test.txtが存在しない、一度コード内の上部で生成しているため、errorはないはず")

            context=""

        if (len(context_en) > 280 ):
            #もし、以前tweetした内容と同じ場合はifでかき消されるので、num.txtの利用などで工夫して回数追加を必要がある
            if before_context_en in before_tweet_en:
                print("same_content")
                with open('./test_en.txt', mode='a+') as f:
                    f.write(before_context_en)

            else:
                try:
                    with open('./test_en.txt', mode='a+') as f:
                        print("tweet\n")
                        f.write(before_context_en)
                        api_EN.update_status(before_context_en)
                    

                except FileNotFoundError:
                    print("test.txtが存在しない、一度コード内の上部で生成しているため、errorはないはず")

            context_en=""

        before_context=context

        before_context_en=context_en

        #print(one_line_en.create_one_line(re.findall('odpt.TrainInformation:(.*)', data[i]['owl:sameAs']).pop(), translate.translate(data[i]['odpt:trainInformationText']['ja'])))

        #25文字以上なら遅延情報あり
        if (25 < len(data[i]['odpt:trainInformationText']['ja'])):
            context_en += one_line_en.create_one_line(re.findall('odpt.TrainInformation:(.*)', data[i]['owl:sameAs']).pop(), translate.translate(data[i]['odpt:trainInformationText']['ja']))
            if data[i]['owl:sameAs'] in dic:
                context += one_line.create_one_line(dic[data[i]['owl:sameAs']], data[i]['odpt:trainInformationText']['ja'])
            else:
                context += one_line.create_one_line(data[i]['owl:sameAs'], data[i]['odpt:trainInformationText']['ja'])


    if context=="":
        print("No changes")

    else:
        #ツイートの実行
        #日本語版の処理
        if before_context in before_tweet:
                print("same_content")
                with open('./test.txt', mode='a+') as f:
                    f.write(context)

        else:
            try:
                with open('./test.txt', mode='a+') as f:
                    print("tweet\n")
                    f.write(context)
                    api_JA.update_status(context)
                    

            except FileNotFoundError:
                print("test.txtが存在しない、一度コード内の上部で生成しているため、errorはないはず")

        #英語版の処理
        if before_context_en in before_tweet_en:
                print("same_content")
                with open('./test_en.txt', mode='a+') as f:
                    f.write(context_en)

        else:
            try:
                with open('./test_en.txt', mode='a+') as f:
                    print("tweet\n")
                    f.write(context_en)
                    api_JA.update_status(context_en)
                    

            except FileNotFoundError:
                print("test.txtが存在しない、一度コード内の上部で生成しているため、errorはないはず")




def main():
    schedule.every(10).minutes.do(job)
    # schedule.every(5).seconds.do(job)
    # schedule.every(3).hours.do(job)

    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == '__main__':
    main()
