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

def get_delay_info_140_280():

    load_dotenv(verbose=True)

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    #Tokyo_Open_Data_APIKEY
    api_key=os.getenv("API_KEY")

    #各路線の日本語生成
    dic = create_dict.get_dict()


    #tweet内容のopendataのjsonデータをから取り出し
    http="https://api-tokyochallenge.odpt.org/api/v4/odpt:TrainInformation?acl:consumerKey="
    train_url = http+str(api_key)
    url = requests.get(train_url)
    text = url.text

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
    tweet_uncomplete_EA=[]
    #140_280文字以内の正規化した文を返す集合
    tweet_JA=set()
    tweet_EA=set()


    data = json.loads(text)

    #データの取り出し
    for i in range(len(data)):
        #まず、25文字以上の文を取り出す
        if (25 < len(data[i]['odpt:trainInformationText']['ja'])):
            over25_train.append(data[i]['owl:sameAs'])
            over25_content.append(data[i]['odpt:trainInformationText']['ja'])

    #遅延情報のみのリストをforにかける->投稿するきれいな文章のみの作成
    for i in range(len(over25_content)):
        tweet_uncomplete_EA.append(one_line_en.create_one_line(re.findall('odpt.TrainInformation:(.*)', over25_train[i]).pop(), translate.translate(over25_content[i])))
        if over25_train[i] in dic:
            tweet_uncomplete_JA.append(one_line.create_one_line(dic[over25_train[i]], over25_content[i]))
        else:
            tweet_uncomplete_JA.append(one_line.create_one_line(over25_train[i], over25_content[i]))

    #日本語の140文字に連結した文章をリストに格納し、返す
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

    #英語の280文字に連結した文章をリストに格納し、返す
    for i in tweet_uncomplete_EA:
        before_context_en+=context_en
        context_en+=i
        if len(context)>280:
            tweet_JA.add(before_context_en)
            context_en=i

    #for文を抜けた後にcontextにまだ残ってる中身確認
    if len(context)>280:
        if not before_context=="":
            tweet_JA.add(before_context)
    else:
        if not context=="":
            tweet_JA.add(context)
    
    return tweet_JA,tweet_EA

if __name__ == '__main__':
    print(get_delay_info_140_280()) 
