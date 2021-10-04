#以前tweetした内容を集合に格納
def get_before_tweet_en():
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
    return before_tweet

if __name__ == '__main__':
    print(get_before_tweet_en()) 