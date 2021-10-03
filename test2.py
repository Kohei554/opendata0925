before_tweet=set()
last_line=""
last_before_line=""
last_tweet_num="" #同じtweetの回数を数え、0,1,2...と増やす、また、文字列で登録
try:
    f = open('./test.txt', mode='r')
    while True:
        line=f.readline()
        if line:
            if len(last_line)>140:
                before_tweet.add(last_before_line)
                last_line = ""
            last_before_line=last_line
            last_line+=line

        else:
            if last_line=="" and last_before_line=="":
                pass

            elif last_line=="":
                if not last_before_line in before_tweet:
                    before_tweet.add(last_before_line)

            elif len(last_line)>140:
                before_tweet.add(last_before_line)
                if not last_line=="" or last_line=="\n":
                    before_tweet.add(last_line)
            else:
                before_tweet.add(last_line)
            break
    f.close()
    print(before_tweet)
    for i in range(len(before_tweet)):
        print(len(before_tweet.pop()))

except FileNotFoundError:
    pass