import json
import requests
from dotenv import load_dotenv
import os
from os.path import join, dirname
import re

def get_dict():
    load_dotenv(verbose=True)

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    #Tokyo_Open_Data_APIKEY
    api_key=os.getenv("API_KEY")

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

    return dic

if __name__ == '__main__':
    print(get_dict()) 