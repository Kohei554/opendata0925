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
    lack_dic={'odpt.TrainInformation:Keikyu':"京急線", 'odpt.TrainInformation:Keio':"京王線・井の頭線", 'odpt.TrainInformation:Seibu':"西武鉄道各線", 'odpt.TrainInformation:Keisei':"京成線"}
    dic.update(lack_dic)



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

#最後にtweetした内容を取得
    last_tweet=""
    last_tweet_num="" #同じtweetの回数を数え、0,1,2...と増やす、また、文字列で登録
    try:
        f = open('./test.txt', mode='r')
        last_tweet = f.read()
        f.close()

    except FileNotFoundError:
        pass
    
    print(last_tweet)
    
    #tweet処理
    for i in range(len(data)):

        if (len(context) > 140 ):
        #以下のif文で最後に投稿した内容の確認
            if last_tweet==before_context:
                try:
                    f = open('./num.txt', mode='r')
                    last_tweet_num = f.read()
                    f.close()
                    last_tweet_num = str(int(last_tweet_num)+1)
                    f = open('./num.txt', mode='w')
                    f.write(last_tweet_num)
                    f.close()
                    api_JA.update_status(last_tweet_num+"回：以前に投稿した最後のtweet内容と同じ状況です")         
                    print(last_tweet_num+"回：以前に投稿した最後のtweet内容と同じ状況です")                      
               

                except FileNotFoundError:
                    f = open('./num.txt', mode='w+')
                    last_tweet = f.write("1")
                    f.close()
                    api_JA.update_status("1回：最後に投稿した内容と同じ状況です")
                    print("1回：最後に投稿した内容と同じ状況です")

            else:
                api_JA.update_status(before_context)
                f = open('./test.txt', mode='w+')
                f.write(before_context)
                f.close()
                context=""
                print(before_context)

        before_context=context
        
        if (25 < len(data[i]['odpt:trainInformationText']['ja'])):
            if data[i]['owl:sameAs'] in dic:
                context += dic[data[i]['owl:sameAs']] + '：' + data[i]['odpt:trainInformationText']['ja'] + "\n" 
                # total_context += dic[data[i]['owl:sameAs']] + '  ' + data[i]['odpt:trainInformationText']['ja'] + "\n" 
            else:
                context += data[i]['owl:sameAs'] + '：' + data[i]['odpt:trainInformationText']['ja'] + "\n" 
                # total_context += data[i]['owl:sameAs'] + '  ' + data[i]['odpt:trainInformationText']['ja'] + "\n" 

        #total_contextに追加しているのは以前と内容が同じか判断するため
        else:
            if data[i]['owl:sameAs'] in dic:
                total_context += dic[data[i]['owl:sameAs']] + '：' + data[i]['odpt:trainInformationText']['ja'] + "\n" 
            else:
                total_context += data[i]['owl:sameAs'] + '：' + data[i]['odpt:trainInformationText']['ja'] + "\n" 


    if context=="":
        print("No changes")
        # print(total_context)
        # api_JA.update_status("if分の方",context)
        # api_JA.update_status("else",random.random())

    #以前の投稿と同じ内容か判断
    # elif total == total_context:
    #     num+=1
    #     api_JA.update_status(str(num)+"以前の遅延状態が継続しています")

    else:
        # print(total_context)
        #ツイートの実行
        # api_JA.update_status("else",random.random())
        if last_tweet==before_context:
            try:
                f = open('./num.txt', mode='r')
                last_tweet_num = f.read()
                f.close()
                last_tweet_num = str(int(last_tweet_num)+1)
                f = open('./num.txt', mode='w')
                f.write(last_tweet_num)
                f.close()
                api_JA.update_status(last_tweet_num+"回：以前に投稿した最後のtweet内容と同じ状況です")  
                print(last_tweet_num+"回：以前に投稿した最後のtweet内容と同じ状況です")                      

            except FileNotFoundError:
                print("except FileNotFoundError:")
                f = open('./num.txt', mode='w+')
                last_tweet = f.write("1")
                f.close()
                api_JA.update_status("1回：最後に投稿した内容と同じ状況です")
                print("1回：最後に投稿した内容と同じ状況です")

        else:
            api_JA.update_status(context)
            print(context)
            f = open('./test.txt', mode='w+')
            f.write(context)
            f.close()


    # total=total_context


def main():
    # schedule.every(10).minutes.do(job)
    schedule.every(10).seconds.do(job)
    # schedule.every(3).hours.do(job)

    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == '__main__':
    main()
