# ChatBot with GPT-2 Rinna, "main_JP_Rinna.py" by F. Fujita on 2022/06/30

import random
import difflib
from transformers import T5Tokenizer, AutoModelForCausalLM
from chardet.universaldetector import UniversalDetector
from flask import Flask, render_template, request
from janome.tokenizer import Tokenizer
from modules import RSS_Recieve_01


Model_file='rinna/japanese-gpt2-xsmall'
#Model_file='rinna/japanese-gpt2-small'
#Model_file='rinna/japanese-gpt2-medium'
#Model_file='rinna/japanese-gpt-1b'

file_path = './ChatBot_with_GPT-2_Rinna-main/'            # 貴方の環境に合わせてパス設定を変更してください。
CSV_file = file_path + 'data/Talk_List.csv'
news_file = file_path + 'data/News.csv'
tenki_file = file_path + 'data/Tenki_jp.csv'
link_file = file_path + 'data/Link_List.csv'
Unk_data = 'えぇーと、'
app = Flask(__name__, static_url_path='/static')
tokenizer = Tokenizer()
t_wakati = Tokenizer(wakati=True)
area_name = '日本'
answer_data = []
link_data = []
ai_ratio = 0.5
text_length = 64

@app.route("/")
# Display by the HTML
def home():
    return render_template("index_JP_Rinna.html")

@app.route("/get_New")
def csv_New():
    global answer_data
    answer_data = list()
    answer_data = []
    temp_data = request.args.get('new_CSV')
    temp = temp_data.split('%0D%0A')
    for i in range(len(temp)):
        temp_01 = temp[i].split('\r\n')
        for j in range(len(temp_01)):
            temp_02 = temp_01[j].split(',')
            if (temp_02[0] != ""):
                temp_02.append('\r\n')
                answer_data.append(temp_02)
    return ('OFF')

@app.route("/get_Add")
def csv_Add():
    global answer_data
    temp_data = request.args.get('add_CSV')
    temp = temp_data.split('%0D%0A')
    for i in range(len(temp)):
        temp_01 = temp[i].split('\r\n')
        for j in range(len(temp_01)):
            temp_02 = temp_01[j].split(',')
            if (temp_02[0] != ""):
                temp_02.append('\r\n')
                answer_data.append(temp_02)
    return ('OFF')

@app.route("/get_Save")
def csv_Save():
    temp_CSV = ""
    for i in range(len(answer_data)):
        for j in range(len(answer_data[i])):
            if (j==0):
                temp_CSV = temp_CSV + answer_data[i][j]
            elif (answer_data[i][j] != ""):
                temp_CSV = temp_CSV + "," + answer_data[i][j]
    temp_data = request.args.get('save_CSV')
    if (temp_data == "CSV_Save"):
        return temp_CSV
    else:
        return ("OFF")

@app.route("/get_AI_Ratio")
# Get the AI Ratio from HTML
def get_AI_Ratio():
    global ai_ratio
    ai_ratio = float(request.args.get('AI_Ratio'))/100
    return (str('OK'))

@app.route("/get")
# Communicate with HTML
def get_bot_response():
    userText = request.args.get('msg')
    answer = make_answer(userText)
    return answer

# Create the answer
def make_answer(tempText):
    if (tempText == ""):
        tempText = "　"
    global area_name
    kensaku_Word = 'ウィキペディア'
    for token in tokenizer.tokenize(tempText):
        if token.part_of_speech.split(',')[2] == '地域':
            area_name = token.surface
        if token.part_of_speech.split(',')[0] == '名詞':
            if (kensaku_Word == 'ウィキペディア' or token.surface != '検索'):
                if (token.surface != '何'):
                    kensaku_Word = token.surface
    wakati = list(t_wakati.tokenize(tempText))
    for i in range(0, len(link_data)):
        if (link_data[i][1] in tempText):
            kensaku_Word = tempText[0: tempText.find(link_data[i][1])]

    temp_Answer = PatternResponder(tempText)
    if ('#NEWS#' in temp_Answer):
        temp = RSS_Recieve_01.news(news_file)
        temp_Answer = temp_Answer.replace('#NEWS#', temp)
    if ('#WEATHER#') in temp_Answer:
        temp_Answer = RSS_Recieve_01.tenki(area_name, tenki_file)
    if ('#WIKI#') in temp_Answer:
        if (kensaku_Word == 'ウィキペディア'):
            for i in range(1, len(wakati) - 1):
                if (wakati[i] == 'を' or wakati[i] == 'とは' or wakati[i] == '永遠'):
                    kensaku_Word = wakati[i-1]
                if (wakati[i] == 'について'):
                    kensaku_Word = tempText[0: tempText.find('について')]
        temp = RSS_Recieve_01.kensaku(kensaku_Word)
        temp_Answer = kensaku_Word + 'の検索結果は、' + temp_Answer.replace('#WIKI#', temp) + "https://ja.wikipedia.org/wiki/" + kensaku_Word
    elif ('#') in temp_Answer:
        temp_data = temp_Answer
        for i in range(0, len(link_data)):
            if link_data[i][0] in temp_Answer:
                temp_data = link_data[i][2] + link_data[i][3] + link_data[i][4] + link_data[i][5]
            temp_data = temp_data.replace('$NON$', '')
            temp_data = temp_data.replace('$KEY$', kensaku_Word)
        temp_Answer = temp_data        
    return str(temp_Answer)

# ChatBot
def in_out(temp_text):
    temp_text = temp_text.replace(' ', '')
    tokenizer = T5Tokenizer.from_pretrained(Model_file) 
    model = AutoModelForCausalLM.from_pretrained(Model_file)
    input = tokenizer.encode(temp_text, return_tensors="pt") 
    output = model.generate(input, do_sample=True, max_length=text_length, num_return_sequences=1)
    temp_reply = tokenizer.batch_decode(output)
    temp_text = str(temp_reply[0])
    pos = temp_text.find('>')
    text_reply = temp_text[(pos + 1):]
    pos = text_reply.rfind('。')
    if (pos > 1):
        text_reply = text_reply[:(pos + 1)]
    else:
        pos = text_reply.rfind('、')
        text_reply = text_reply[:(pos + 1)]
    if (text_reply == '' or text_reply == ' ' or text_reply == '　'):
        text_reply = 'ごめんなさい。ちょっと寝てしまいましたわ。'
    return text_reply

def init():
    global answer_data
    global link_data
    answer_data = []
    answer_data = csv_load(CSV_file)
    link_data = []
    link_data = csv_load(link_file)
    return

def csv_load(filename):
    lines = []
    return_data = []
    file_code = detect_character_code(filename)
    with open (filename, encoding=file_code) as csvfile:
        for line in csvfile.readlines():
            lines.append(line)
    for i in range(len(lines)):
        temp = lines[i].split(',')
        if (temp[0] != ""):
            temp_data = []
            for j in range(len(temp)):
                if (temp[j] != "" or temp[j] != "\r\n" or temp[j] != "\n"):
                    temp_data.append(temp[j])
            return_data.append(temp_data)
    return return_data

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

def PatternResponder(tempText):
    temp_count = 0.0
    max_count = 0.0
    array_No = 0
    for i in range(len(answer_data)):
        temp_count = difflib.SequenceMatcher(None, tempText, answer_data[i][0]).ratio()
        if (max_count < temp_count):
            max_count = temp_count
            array_No = i
    #print('質問一致率＝ ', max_count)
    temp_Answer = random.choice(answer_data[array_No])
    if (temp_Answer == answer_data[array_No][0] or temp_Answer == "" or temp_Answer == " " or temp_Answer == "\n"):
        temp_Answer = answer_data[array_No][1]
    if ('#') in temp_Answer:
        return temp_Answer
    elif (array_No > len(answer_data)) or (max_count <= ai_ratio):
        temp_Answer = in_out(str(tempText))
        temp_Answer = temp_Answer.replace(' ', '')
        temp_Answer = temp_Answer.replace('<unk>', Unk_data)
    return temp_Answer

if __name__ == "__main__":
    #random.seed(None)
    init()
    app.run(host='127.0.0.1', port=5000, debug=True)
