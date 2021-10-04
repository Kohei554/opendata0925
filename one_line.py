def create_one_line(context):
    oneline_sentence=""
    for i in context:
        if "。" == i:
            break
        oneline_sentence+=i
    oneline_sentence+="。"
    return oneline_sentence 

if __name__ == '__main__':
    print(create_one_line("外房線：外房線は、内房線内での動物と衝突の影響で、\n千葉～勝浦駅間の下り線の一部列車に遅れがでています。\n伊勢崎線：18時10分頃、蒲生駅で発生した人身事故の影響により、一部列車に運休および遅れがでています。")) 