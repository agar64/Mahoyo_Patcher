import os

def metric(text):
    indices = [89, 113, 1482, 1602, 1604,
               1874, 1877, 2576, 2991, 3083,
               3101, 3156, 4012, 4059, 4419,
               4476, 4553, 4558, 4655,
               4695, 4837, 4849, 4852, 4858,
               4877, 4940, 4941, 5156, 5214,
               5565, 5613, 5688, 5866,
               5879, 5890, 5892, 5909,
               5957, 5962, 5965, 6012, 6300,
               6364, 6376, 6400, 6407,
               6449, 6478, 6491, 6826, 6838,
               6918, 6921, 7105,
               7227, 7238, 7243, 7308, 5826, 8772,
               10175, 10176, 10192, 10647,
               11009, 11047, 11727, 14791, 14988,
               15286, 15288, 15381, 15895,
               16798, 16827, 16916, 16923, 16974,
               17218, 17487,
               17515, 17549, 17880, 18038, 18070,
               18308,
               18328, 18329, 18340, 18383, 20479,
               20786, 20930, 21087, 22576, 22577, 23065,
               14811, 4486, 1485,
               11505]
    imperial_strings = ["43 degrees Fahrenheit", "thirty-foot", "over three feet", "45 miles", "miles",
                        "yards", "15 feet", "was a good few feet in length", "6 feet", "a few feet",
                        "ten feet", "a few feet", "yards", "thirty feet", "greater than a football field",
                        "fifteen feet", "few feet", "sixty feet", "thirty or so feet",
                        "a couple hundred feet", "thirty-foot", "hundred-pound", "thirty feet", "thirty feet",
                        "thirty feet", "a hundred feet", "fifty feet", "thirty feet", "thirty feet",
                        "thirty feet", "yards", "fifty feet", "one hundred feet",
                        "One hundred and fifty feet", "fifteen feet", "foot", "a hundred and fifty feet",
                        "two hundred feet", "three hundred feet", "half-mile", "650 yards", "miles",
                        "a great height―was", "six hundred feet", "two hundred feet", "two-hundred-foot",
                        "five feet", "a hundred feet", "a few feet", "sixty-foot", "yards...!",
                        "the better part of a mile", "mile", "two hundred and fifty feet",
                        "yards", "ten feet", "three feet", "paces", "three feet", "couple of feet",
                        "sixteen inches", "sixty miles", "six miles", "three hundred feet",
                        "yards", "inches", "112 miles", "twelve feet", "eighty feet",
                        "ten miles", "Four inches", "six miles", "six feet",
                        "two miles", "a hundred feet", "yards", "yards", "a hundred feet",
                        "closed the distance between them.", "thirty feet",
                        "Fifteen feet to go", "Five feet", "twenty pounds", "feet", "twenty-foot",
                        "the beast now towered above him",
                        "thirty feet", "thirty feet", "three feet", "three feet", "seventy-pound",
                        "yards", "yards", "thirty feet", "miles", "50 miles", "eight inches",
                        "twelve hundred square foot", "a foot to his left", "a foot and a half",
                        "myself, but I think my brain had a major malfunction, and my hand just went for it!"]
    metric_strings = ["6 degrees Celsius", "ten-meter", "around one meter", "70 kilometers", "kilometers",
                      "meters", "five meters", "stretched out several meters", "two meters", "one meter",
                      "several meters", "one meter", "meters", "ten meters", "about a hundred meters",
                      "five meters", "two meters", "twenty meters", "ten or so meters",
                      "about sixty meters", "ten-meter", "forty-five-kilo", "ten meters", "ten meters",
                      "ten meters", "thirty meters", "fifteen meters", "ten meters", "ten meters",
                      "ten meters", "meters", "twenty meters", "forty meters",
                      "Forty-eight meters", "five meters", "meter", "fifty meters",
                      "sixty meters", "a hundred meters", "one-kilometer", "600 meters", "kilometers",
                      "sixty meters above ground―was", "two hundred meters", "sixty meters", "sixty-meter",
                      "two meters", "thirty meters", "about a meter", "18-meter", "meters...!",
                      "about a kilometer", "kilometer", "eighty meters",
                      "meters", "three meters", "a meter", "meters", "a meter", "meter",
                      "forty centimeters", "a hundred kilometers", "ten kilometers", "a hundred meters",
                      "meters", "centimeters", "180 kilometers", "six meters", "eight meters",
                      "fifteen kilometers", "Ten centimeters", "ten kilometers", "two meters",
                      "three kilometers", "thirty meters", "meters", "meters", "thirty meters",
                      "closed the distance between them to just ten meters.", "ten meters",
                      "Five meters to go", "Two meters", "ten kilos", "meters", "six-meter",
                      "the boy, who was smaller than him, had grown to a size of nearly two meters",
                      "ten meters", "ten meters", "a meter", "a meter", "thirty-kilo",
                      "meters", "meters", "ten meters", "kilometers", "80 kilometers", "twenty centimeters",
                      "four hundred square meters", "twenty centimeters", "fifty centimeters",
                      "just a centimeter before that, but I misjudged. It turns out that Aozaki's physical size was slightly greater than my visual information."]

    for i in range (len(indices)):
        text[indices[i]-1] = text[indices[i]-1].replace(imperial_strings[i], metric_strings[i])

    return text

def romanization(text):
    localized_name = ["Soujyuro", "Sizuki", "Fumidsuka", "Yamasiro", "Koga"]
    hepburn_name = ["Soujuurou", "Shizuki", "Fumizuka", "Yamashiro", "Kouga"]

    for i in range (len(localized_name)):
        line_count = 0
        for line in text:
            if (localized_name[i] in line) and (hepburn_name[i] not in line):
                text[line_count] = text[line_count].replace(localized_name[i], hepburn_name[i])
            line_count += 1

    return text

def name_order(text):
    localized_name = ["Aoko Aozaki", "Alice Kuonji", "Soujuurou Shizuki", "Touko Aozaki", "Tobimaru Tsukiji",
                      "Housuke Kinomi", "Kojika Kumari", "Eiri Fumizuka", "Ritsuka Suse", "Yuika Suse",
                      "Kazuki Yamashiro", "Yurihiko Tokitsu"]
    correct_name = ["Aozaki Aoko", "Kuonji Alice", "Shizuki Soujuurou", "Aozaki Touko", "Tsukiji Tobimaru",
                    "Kinomi Housuke", "Kumari Kojika", "Fumizuka Eiri", "Suse Ritsuka", "Suse Yuika",
                    "Yamashiro Kazuki", "Tokitsu Yurihiko"]

    for i in range (len(localized_name)):
        line_count = 0
        for line in text:
            if (localized_name[i] in line) and (correct_name[i] not in line):
                text[line_count] = text[line_count].replace(localized_name[i], correct_name[i])
            line_count += 1

    return text

def honorifics(text_en, text_jp):
    en_name_prefix = ["Mr. ", "Ms. ", "Mister ", "Miss ", "Lady ", ""]
    en_proper_name = ["Aozaki", "Aoko", "Kuonji", "Alice", "Shizuki", "Soujuurou", "Touko", "Touko",
                      "Tsukiji", "Tobimaru", "Kinomi", "Housuke", "Kumari", "Kojika", "Lugh", "Beowulf",
                      "Beo", "Fumizuka", "Eiri", "Suse", "Ritsuka", "Yuika", "Sister", "Sister",
                      "Yamashiro", "Kazuki", "Tokitsu", "Yurihiko", "May", "Riddell", "Archelot",
                      "Yoshida", "Yoshida", "Kouga", "Kouga", "Uotatsu", "Uotatsu", "Hanazawa", "Eiri",
                      "Zaki", "Alice", "Yui", "Toko", "Ako", "Yui", "Aozaki", "Soujuurou", "Arisato",
                      "Yamashiro", "Satonaka", "Satonaka", "Mino", "Mino"]
    en_honorific = ["-san", "-sama", "-sama", "-chan", "-kun", "-kun", "-sensei", "-senpai", "-shi"]

    jp_proper_name = ["蒼崎", "青子", "久遠寺", "有珠", "静希", "草十郎", "橙子", "トーコ", "槻司", "鳶丸",
                      "木乃美", "芳助", "久万梨", "金鹿", "ルゥ", "ベオウルフ", "ベオ", "文柄", "詠梨", "周瀬",
                      "律架", "唯架", "唯架", "シスター", "山城", "和樹", "土桔", "由里彦", "メイ", "リデル",
                      "アーシェロット", "吉田", "<吉田|よしだ>", "恒河", "<恒河|こうが>", "<魚達|うおたつ>",
                      "魚達", "花澤", "エイリ", "ザキ", "アリス", "ユイ", "トコ", "アコ", "唯",
                      "<蒼崎|あおざき>", "うじゅうろう>", "有里", "城|やましろ>",
                      "中|さとなか>", "里中", "<美濃|みの>", "み><濃|の>"]
    jp_honorific = ["さん", "様", "さま", "ちゃん", "くん", "君", "先生", "先輩", "氏"]

    line_count = 0
    for line_jp in text_jp:
        for index in range(0, len(en_proper_name) - 1):
            en_name = [pre + en_proper_name[index] for pre in en_name_prefix]
            en_name_honorific = [en_proper_name[index] + suf for suf in en_honorific]
            jp_name = [jp_proper_name[index] + hon for hon in jp_honorific]
            for index2 in range(0, len(jp_honorific) - 1):
                if jp_name[index2] in line_jp:
                    for name in en_name:
                        if (name in text_en[line_count]) and (en_name_honorific[index2] not in text_en[line_count]):
                            text_en[line_count] = text_en[line_count].replace(name, en_name_honorific[index2])
                            break

        line_count = line_count + 1
    text_en = honorifics_special(text_en, text_jp)
    return text_en

def honorifics_special(text_en, text_jp):
    # Special Cases:
    # アッちゃん - Allie
    # アコちゃん - Aoko
    # ペン太くん - Flippy

    jp_name = ["アッちゃん", "アコちゃん", "ペン太くん"]
    en_name_honorific = ["Acchan", "Ako-chan", "Penta-kun"]
    en_name = ["Allie", "Aoko", "Flippy"]

    for i in range(0, len(en_name) - 1):
        line_count = 0
        for line_jp in text_jp:
            if jp_name[i] in line_jp:
                if (en_name[i] in text_en[line_count]) and (en_name_honorific[i] not in text_en[line_count]):
                    text_en[line_count] = text_en[line_count].replace(en_name[i], en_name_honorific[i])
            line_count = line_count + 1
    return text_en


class Replacer:
    def __init__(self, game_dir, input_path, output_path):
        self.in_path = os.path.join(game_dir, input_path)
        self.out_path = os.path.join(game_dir, output_path)

    def get_script(self):
        script = open(self.in_path, "r", encoding='utf-8')
        text = script.readlines()
        script.close()
        return text

    def set_script(self, text):
        fout = open(self.out_path, 'w', encoding='utf-8')
        fout.writelines(text)
        fout.close()