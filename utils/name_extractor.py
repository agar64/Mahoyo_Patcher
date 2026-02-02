import os

file_path = r"F:\Games\SteamLibrary\steamapps\common\WITCH ON THE HOLY NIGHT"
f01_name = "script_jp"
f02_name = "script_en_original"

f01_path = os.path.join(file_path, f"{f01_name}.txt")
f02_path = os.path.join(file_path, f"{f02_name}.txt")

script_jp = open(f01_path, "r", encoding='utf-8')
script_en = open(f02_path, "r", encoding='utf-8')

en_text = script_en.readlines()

en_name_prefix = ["Mr. ", "Ms. ", "Mister ", "Miss ", "Lady ", ""]
en_proper_name = ["Aozaki", "Aoko", "Kuonji", "Alice", "Shizuki", "Soujuurou", "Touko", "Touko", "Tsukiji",
                  "Tobimaru", "Kinomi", "Housuke", "Kumari", "Kojika", "Lugh", "Beowulf", "Beo", "Fumizuka",
                  "Eiri", "Suse", "Ritsuka", "Yuika", "Sister", "Sister", "Yamashiro", "Kazuki", "Tokitsu",
                  "Yurihiko", "May", "Riddell", "Archelot"]
en_honorific = ["-san", "-sama", "-sama", "-chan", "-kun", "-kun", "-sensei", "-senpai"]

jp_proper_name = ["蒼崎", "青子", "久遠寺", "有珠", "静希", "草十郎", "橙子", "トーコ", "槻司", "鳶丸", "木乃美",
                  "芳助", "久万梨", "金鹿", "ルゥ", "ベオウルフ", "ベオ", "文柄", "詠梨", "周瀬", "律架", "唯架",
                  "唯架", "シスター", "山城", "和樹", "土桔", "由里彦", "メイ", "リデル", "アーシェロット"]
jp_honorific = ["さん", "様", "さま", "ちゃん", "くん", "君", "先生", "先輩"]


#en_name_honorific = "Beo-kun"
en_name = [pre + en_proper_name[0] for pre in en_name_prefix]
en_name_honorific = [en_proper_name[0] + suf for suf in en_honorific]
#en_name = [[x + y for x in en_name_prefix] for y in en_proper_name]
print(en_name)
print(en_name_honorific)
jp_name = [jp_proper_name[0] + hon for hon in jp_honorific]
print(jp_name)


list_line = 0
names_list = []
for hon in jp_honorific:
    line_count = 0
    script_jp.seek(0)
    print("===-",hon, "-===", sep='')
    names_list.append("===-" + hon + "-===" + '\n')
    for line_jp in script_jp:
        if hon in line_jp:
            subtxt = line_jp[:line_jp.index(hon)]
            subtxt2 = line_jp[:line_jp.index(hon)-7]
            newtxt = subtxt.replace(subtxt2, '')
            hits = False
            for name in jp_proper_name:
                if name in newtxt:
                    hits = True
            if not hits:
                print(line_count, " - ", newtxt, hon, sep='')
                names_list.append(str(line_count+1) + " - " + newtxt + hon + '\n')
                list_line = list_line + 1


        line_count = line_count + 1



fout = open(r'F:\Games\SteamLibrary\steamapps\common\WITCH ON THE HOLY NIGHT\extracted files\honorifics\extracted_names.txt', 'w', encoding='utf-8')
fout.writelines(names_list)
fout.close()


script_en.close()
script_jp.close()