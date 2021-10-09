import schedule
from dotenv import load_dotenv
from os.path import join, dirname
from time import sleep
import get_before_tweet
import get_before_tweet_en
import post


def job():
    #before_tweetにtest.txtから140字で以前tweetした内容を保存
    before_tweet=get_before_tweet.get_before_tweet()
    
    #before_tweet_enに以前に投稿した280文字のenの集合を獲得
    before_tweet_en=get_before_tweet_en.get_before_tweet_en()

    post.post(before_tweet, before_tweet_en)
    
def main():
    # schedule.every(10).minutes.do(job)
    schedule.every(1).seconds.do(job)
    # schedule.every(3).hours.do(job)

    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == '__main__':
    main()
