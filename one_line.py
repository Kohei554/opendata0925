def create_one_line(train, context):
    oneline_sentence=""
    for i in context:
        if "。" == i:
            break
        oneline_sentence+=i
    oneline_sentence+="。"
    if len(train+'：'+oneline_sentence+'\n') > 140:
        return train + "：現在遅延しています。"
    return train+'：'+oneline_sentence+'\n'

if __name__ == '__main__':
    print(create_one_line("外房線","外房線：外房線は、内房線内での動物と衝突の影響で、\n千葉～勝浦駅間の下り線の一部列車に遅れがでています。\n伊勢崎線：18時10分頃、蒲生駅で発生した人身事故の影響により、一部列車に運休および遅れがでています。")) 
    print(create_one_line("外貌線", "新宿線は、19時02分頃、井荻～上井草駅間での線路内人立入りの影響により、新宿線の特急電車は運転を見合わせていましたが、上り：本川越駅21時30分発（小江戸5２号）・所沢駅22時17分発（小江戸54号）・所沢駅22時47分発（小江戸56号）・本川越駅23時00分発（小江戸58号）から、下り：西武新宿駅22時30分発（小江戸47号）から運転を再開いたします。"))