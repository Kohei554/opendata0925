import json
import requests
import opendata_api_key
import config
import tweepy
import schedule
from time import sleep
import re

def job():
    # ここに取得したキーを書く
    CONSUMER_KEY = config.TWITTER_API_KEY_JP
    CONSUMER_TOKEN = config.TWITTER_API_KEY_SECRET_JP
    ACCESS_KEY = config.ACCESS_TOKEN_JP
    ACCESS_TOKEN = config.ACCESS_TOKEN_SECRET_JP

    # tweepyによるOAuth認証処理
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_TOKEN)
    auth.set_access_token(ACCESS_KEY, ACCESS_TOKEN)
    api = tweepy.API(auth)


    #tweet内容のopendataのjsonデータをから取り出し
    api_key=opendata_api_key.API_KEY
    key="&acl:consumerKey="
    http="https://api-tokyochallenge.odpt.org/api/v4/odpt:TrainInformation?"
    #conditions="&owl:sameAs=odpt.TrainInformation:JR-East.ChuoRapid"
    conditions=""
    train_url = http+conditions+key+api_key
    url = requests.get(train_url)
    text = url.text
    #print(text)

    context=""
    before_context=""


    #before_before_context=""

    data = json.loads(text)

    for i in range(len(data)):
        
        if (21 < len(data[i]['odpt:trainInformationText']['ja'])):
            context += data[i]['owl:sameAs'] + '  ' + data[i]['odpt:trainInformationText']['ja'] + "a" +"\n" 
            
        if (len(context) > 140 ):
            
            #api.update_status(before_context)
            context=""
        before_context=context

    if context=="":
        print("No changes")
        # api.update_status("No changes")
    else:
        #ツイートの実行
        api.update_status(context)
        #print(context)



def main():
    schedule.every(5).minutes.do(job)

    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == '__main__':
    main()
