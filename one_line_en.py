#路線と遅延情報をたして、280文字を超える場合の処理を行う関数
def create_one_line(train, context):
    if len(train+' : '+context+'\n') > 280:
        if len(train + " : This train is delayed.\n") > 280:
            return train
        return train + " : This train is delayed.\n"
    return train+' : '+context+'\n'

if __name__ == '__main__':
    print(create_one_line("JR-East.TsurumiOkawaBranch","Service on schedule"))
    print(create_one_line("odpt.TrainInformation:JR-East.TsurumiOkawaBranch","Service on schedule"))