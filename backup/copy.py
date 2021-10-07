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
    lack_dic={'odpt.TrainInformation:Keikyu':"京急線", 'odpt.TrainInformation:Keio':"京王線・井の頭線", 'odpt.TrainInformation:Seibu':"西武鉄道各線", 'odpt.TrainInformation:Keisei':"京成線"}
    dic.update(lack_dic)



    #tweet内容のopendataのjsonデータをから取り出し
    http="https://api-tokyochallenge.odpt.org/api/v4/odpt:TrainInformation?acl:consumerKey="
    train_url = http+str(api_key)
    url = requests.get(train_url)
    text = url.text

    data = json.loads(text)

    #以前に投稿した140文字の集合を獲得
    #before_tweetにtest.txtから140字で以前tweetした内容を保存
    before_tweet=set()
    last_line=""
    last_before_line=""
    try:
        f = open('./test_en.txt', mode='r')
        while True:
            line=f.readline()
            if line:
                if len(last_line)>280:
                    before_tweet.add(last_before_line)
                    last_line = ""
                last_before_line=last_line
                last_line+=line

            else:
                if last_line=="" and last_before_line=="":
                    pass
                #多分下のelifはいらない->elifの処理は一切行われないはず
                elif last_line=="":
                    if not last_before_line in before_tweet:
                        before_tweet.add(last_before_line)

                #多分下のelifはいらない->elifの処理は一切行われないはず
                elif len(last_line)>140:
                    before_tweet.add(last_before_line)
                    if not last_line=="" or last_line=="\n":
                        before_tweet.add(last_line)
                else:
                    before_tweet.add(last_line)
                break
        f.close()

    except FileNotFoundError:
        pass

    #test.txtの初期化、リセット
    f = open('./test_en.txt', mode='w+')
    f.write("")
    f.close()
    
    #以前に投稿した280文字のenの集合を獲得
    before_tweet_en=set()
    last_line=""
    last_before_line=""
    try:
        f = open('./test_en.txt', mode='r')
        while True:
            line=f.readline()
            if line:
                if len(last_line)>280:
                    before_tweet_en.add(last_before_line)
                    last_line = ""
                last_before_line=last_line
                last_line+=line

            else:
                if last_line=="" and last_before_line=="":
                    pass
                #多分下のelifはいらない->elifの処理は一切行われないはず
                elif last_line=="":
                    if not last_before_line in before_tweet_en:
                        before_tweet_en.add(last_before_line)

                #多分下のelifはいらない->elifの処理は一切行われないはず
                elif len(last_line)>140:
                    before_tweet_en.add(last_before_line)
                    if not last_line=="" or last_line=="\n":
                        before_tweet_en.add(last_line)
                else:
                    before_tweet_en.add(last_line)
                break
        f.close()

    except FileNotFoundError:
        pass


    #test.txtの初期化、リセット
    f = open('./test_en.txt', mode='w+')
    f.write("")
    f.close()


    #下の140文字生成時に利用
    context=""
    before_context=""
    #下の140文字生成時に利用_English
    context_en=""
    before_context_en=""
    #25文字以上か判別
    over25_train=[]
    over25_content=[]
    #over25_train、over25_contentを合体させ、正規化したリスト
    tweet_uncomplete_JA=[]
    tweet_uncomplete_EN=[]
    #140_280文字以内の正規化した文を返す集合
    tweet_JA=set()
    tweet_EN=set()


    data = json.loads(text)

    #データの取り出し
    for i in range(len(data)):
        #まず、25文字以上の文を取り出す
        if (25 < len(data[i]['odpt:trainInformationText']['ja'])):
            over25_train.append(data[i]['owl:sameAs'])
            over25_content.append(data[i]['odpt:trainInformationText']['ja'])


    #遅延情報のみのリストをforにかける->投稿するきれいな文章のみの作成
    for i in range(len(over25_content)):
        tweet_uncomplete_EN.append(one_line_en.create_one_line( re.findall('odpt.TrainInformation:(.*)', over25_train[i]).pop(), translate.translate(over25_content[i])))
        if over25_train[i] in dic:
            tweet_uncomplete_JA.append(one_line.create_one_line(dic[over25_train[i]], over25_content[i]))
        else:
            tweet_uncomplete_JA.append(one_line.create_one_line(over25_train[i], over25_content[i]))

    #日本語の140文字以内で、連結した文章をリストに格納し、返す
    for i in tweet_uncomplete_JA:
        before_context+=context
        context+=i
        if len(context)>140:
            tweet_JA.add(before_context)
            context=i

    #for文を抜けた後にcontextにまだ残ってる中身確認
    if len(context)>140:
        if not before_context=="":
            tweet_JA.add(before_context)
    else:
        if not context=="":
            tweet_JA.add(context)



    #英語の280文字以内で、連結した文章をリストに格納し、返す
    for i in tweet_uncomplete_EN:
        before_context_en+=context_en
        context_en+=i
        if len(context)>280:
            tweet_EN.add(before_context_en)
            context_en=i

    #for文を抜けた後に英語のcontext_enにまだ残ってる中身確認
    if len(context_en)>280:
        if not before_context_en=="":
            tweet_EN.add(before_context_en)
    else:
        if not context_en=="":
            tweet_EN.add(context_en)

    
    for i in tweet_JA:
        #日本語版の処理
        if i in before_tweet:
            with open('./test.txt', mode='a+') as f:
                try:
                    f.write(i)                        
                except FileNotFoundError:
                    print("test.txtが存在しない、一度コード内の上部で生成しているため、errorはないはず")
        else:
            try:
                with open('./test.txt', mode='a+') as f:
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



    

def main():
    # schedule.every(10).minutes.do(job)
    schedule.every(1).seconds.do(job)
    # schedule.every(3).hours.do(job)

    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == '__main__':
    main()
