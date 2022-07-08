# RSS_Recieve.py 2022/05/23 by T. Fujita
import requests
import feedparser
from chardet.universaldetector import UniversalDetector
from bs4 import BeautifulSoup
import random

def forming_A(temp_text, target_01, target_02):     # target_01 と target_02 の間を削除する。（後方検索）
    idx_e = temp_text.find(target_02)
    idx_s = temp_text.rfind(target_01, 0, idx_e)
    temp_text_F = temp_text[:idx_s]
    temp_text_B = temp_text[idx_e + len(target_02):]
    temp_text = temp_text_F + temp_text_B
    return temp_text

def forming_B(temp_text, target):                   # target 以降を削除する
    idx = temp_text.find(target)
    temp_text = temp_text[:idx]
    return temp_text

def forming_C(temp_text, target_01, target_02):     # target_01 と target_02 の間を削除する。（前方検索）
    idx_s = temp_text.find(target_01)
    idx_e = temp_text.find(target_02, idx_s, len(temp_text))
    temp_text_F = temp_text[:idx_s]
    temp_text_B = temp_text[idx_e + len(target_02):]
    temp_text = temp_text_F + temp_text_B
    return temp_text

def forming_E(temp_text, target_01, target_02):     # target_01 と target_02 を削除する。（前方検索）
    idx_s = temp_text.find(target_01)
    temp_text_F = temp_text[:idx_s]
    temp_text_B = temp_text[idx_s + len(target_01):]
    temp_text = temp_text_F + temp_text_B.replace(target_02, "")
    return temp_text

def forming_F(temp_text, target):                   # target 以前を削除する
    idx = temp_text.find(target)
    temp_text = temp_text[idx + len(target):]
    return temp_text

def forming(temp_text):
    return_text = ''
    soup = BeautifulSoup(temp_text.content, "html.parser")
    target_01 = 'class="mw-headline"'
    temp = forming_B(str(soup), target_01)
    soup = BeautifulSoup(temp, "html.parser")
    for element in soup.find_all("p"):
        return_text = return_text + element.text
        return_text = return_text.replace('\n\n', '\n')
    return return_text

def Csv_Load(filename):
    lines = []
    file_code = detect_character_code(filename)
    with open (filename, encoding=file_code) as csvfile:
        for line in csvfile.readlines():
            if (line[0] != ','):
                lines.append(line)
    return lines

def detect_character_code(pathname):
    file_code_dic = ''
    detector = UniversalDetector()
    with open (pathname, 'rb') as f:
        detector.reset()
        for line in f.readlines():
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        file_code_dic = detector.result['encoding']
    return file_code_dic

def news(news_file):
    news_data = Csv_Load(news_file)
    total = len(news_data)
    temp = random.randint(0, total)
    temp_data = news_data[temp].split(',')
    text_data = temp_data[0]
    RSS_URL = temp_data[1]
    soup = feedparser.parse(RSS_URL)
    temp_text = text_data + 'からの情報では、\n'
    temp_soup = []
    for entry in soup.entries:
        if text_data == 'gori.me' or text_data == 'Togetterまとめ' or text_data == 'GIGAZINE' or text_data == '朝日新聞':
            temp_soup.append( entry.title )
        else:
            temp_soup.append( entry.title + '：　' + entry.description )
    temp_text = temp_text + random.choice(temp_soup) + '\n以上です。'
    return temp_text

def tenki(text_data, tenki_file):
    Temp_a = 'https://tenki.jp'
    Temp_b = '全国'
    csv_data = Csv_Load(tenki_file)
    for i in range(len(csv_data)):
        temp = csv_data[i].split(',')
        if temp[0] == text_data:
            Temp_a = str(temp[1]).replace('\n', '')
            Temp_b = str(temp[2]).replace('\n', '')
    return Temp_b + 'の天気予報を表示します。' + Temp_a

def kensaku(text_data):
    url = 'https://ja.wikipedia.org/wiki/'
    temp = 'ウィキペディアによりますと、\n'
    res = requests.get(url + text_data)
    soup = res.text
    target_00 = '#REDIRECT [['
    if (target_00 in soup):
        temp = "リダイレクトしました。\nウィキペディアによりますと、\n"
        soup = forming_F(soup, target_00)
        target_01 = ']]'
        text_data = forming_B(soup, target_01)
        res = requests.get(url + text_data)
    target_00 = '#REDIRECT[['
    if (target_00 in soup):
        temp = "リダイレクトしました。\nウィキペディアによりますと、\n"
        soup = forming_F(soup, target_00)
        target_01 = ']]'
        text_data = forming_B(soup, target_01)
        res = requests.get(url + text_data)
    target_00 = '#redirect [['
    if (target_00 in soup):
        temp = "リダイレクトしました。\nウィキペディアによりますと、\n"
        soup = forming_F(soup, target_00)
        target_01 = ']]'
        text_data = forming_B(soup, target_01)
        res = requests.get(url + text_data)        
    target_00 = '#redirect[['
    if (target_00 in soup):
        temp = "リダイレクトしました。\nウィキペディアによりますと、\n"
        soup = forming_F(soup, target_00)
        target_01 = ']]'
        text_data = forming_B(soup, target_01)
        res = requests.get(url + text_data)        
    target_00 = '#転送 [['
    if (target_00 in soup):
        temp = "リダイレクトしました。\nウィキペディアによりますと、\n"
        soup = forming_F(soup, target_00)
        target_01 = ']]'
        text_data = forming_B(soup, target_01)
        res = requests.get(url + text_data)
    target_00 = '#転送[['
    if (target_00 in soup):
        temp = "リダイレクトしました。\nウィキペディアによりますと、\n"
        soup = forming_F(soup, target_00)
        target_01 = ']]'
        text_data = forming_B(soup, target_01)
        res = requests.get(url + text_data)
    soup = temp + forming(res) + '\n以上です。'
    target_00 = '<namespaces>'
    if (target_00 in soup):
        soup = 'あらっ！　検索結果がありませんわ。　変な言葉を使ったんじゃなくって？'
    return soup
