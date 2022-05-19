# ChatBot with GPT-2 Rinna and VoiceVox, "main_JP_Voicevox_Rinna.py" by F. Fujita on 2022/05/19

import random
import difflib
from transformers import T5Tokenizer, AutoModelForCausalLM
from chardet.universaldetector import UniversalDetector
from flask import Flask, render_template, request
from janome.tokenizer import Tokenizer
from modules import RSS_Recieve_01
import json
import requests
import wave


Model_file='rinna/japanese-gpt2-xsmall'
#Model_file='rinna/japanese-gpt2-small'
#Model_file='rinna/japanese-gpt2-medium'
#Model_file='rinna/japanese-gpt-1b'

CSV_file = './ChatBot_with_GPT-2_Rinna-main/data/Talk_List.csv'
Unk_data= 'あのね、'
app = Flask(__name__, static_url_path='/static')
tokenizer = Tokenizer()
t_wakati = Tokenizer(wakati=True)
area_name = '日本'
answer_data = []
ai_ratio = 0.5
text_length = 64
Speaker_No = 0
voice_count = 0
filepath = './ChatBot_with_GPT-2_Rinna-main/static/audio/audio'

@app.route("/")
# Display by the HTML
def home():
    return render_template("index_JP_Voicevox_Rinna.html")

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

@app.route("/get_Voice")
# Get the Voice No from HTML
def get_Voice_No():
    global Speaker_No
    Speaker_No = int(request.args.get('Voice_No'))
    return (str('OK'))

@app.route("/get")
# Communicate with HTML
def get_bot_response():
    userText = request.args.get('msg')
    answer = make_answer(userText)
    return answer

# Create the answer
def make_answer(tempText):
    global voice_count
    voice_count = voice_count + 1
    if (voice_count >= 30000):
        voice_count = 0
    voice_count_text = ('0000' + str(voice_count))[-4:]

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
    if ('について検索' in tempText):
        kensaku_Word = tempText[0: tempText.find('について検索')]
    if ('の写真' in tempText):
        kensaku_Word = tempText[0: tempText.find('の写真')]
    if ('の画像' in tempText):
        kensaku_Word = tempText[0: tempText.find('の画像')]
    if ('の動画' in tempText):
        kensaku_Word = tempText[0: tempText.find('の動画')]
    if ('の映像' in tempText):
        kensaku_Word = tempText[0: tempText.find('の映像')]
    if ('のビデオ' in tempText):
        kensaku_Word = tempText[0: tempText.find('のビデオ')]
    if ('の鳴き声' in tempText):
        kensaku_Word = tempText[0: tempText.find('の鳴き声')]
      
    if (('音声認識' in tempText or '音声入力' in tempText) and '終了' in tempText):
        return str('音声入力を終了しました。')
    else:
        temp_Answer = PatternResponder(tempText)
        if ('#NEWS#' in temp_Answer):
            temp = RSS_Recieve_01.news()
            temp_Answer = temp_Answer.replace('#NEWS#', temp)
        if ('#WEATHER#') in temp_Answer:
            temp_Answer = RSS_Recieve_01.tenki(area_name)
        if ('#WIKI#') in temp_Answer:
            if (kensaku_Word == 'ウィキペディア'):
                for i in range(1, len(wakati) - 1):
                    if (wakati[i] == 'を' or wakati[i] == 'とは' or wakati[i] == '永遠'):
                        kensaku_Word = wakati[i-1]
                    if (wakati[i] == 'について'):
                        kensaku_Word = tempText[0: tempText.find('について')]
            temp = RSS_Recieve_01.kensaku(kensaku_Word)
            temp_Answer = kensaku_Word + 'の検索結果は、' + temp_Answer.replace('#WIKI#', temp)
        if ('#FORTUNE#') in temp_Answer:
            temp_Answer = '占いを表示します。'
        if ('#PHOTO#') in temp_Answer:
            temp_Answer = kensaku_Word + 'の画像を表示します。'
        if ('#VIDEO#') in temp_Answer:
            temp_Answer = kensaku_Word + 'のビデオを表示します。'
        if ('#CALL#') in temp_Answer:
            temp_Answer = kensaku_Word + 'ですね、鳥以外には対応していません。動物の鳴き声は「東京ズーネット」で検索してください。'
        
        generate_wav(temp_Answer, Speaker_No, filepath, voice_count_text)      
        return str(voice_count_text + ':' + temp_Answer)

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
    answer_data = []
    temp_data = csv_load(CSV_file)
    for i in range(len(temp_data)):
        temp = temp_data[i].split(',')
        if (temp[0] != ""):
            temp_temp = []
            for j in range(len(temp)):
                if (temp[j] != "" or temp[j] != "\r\n" or temp[j] != "\n"):
                   temp_temp.append(temp[j])
            answer_data.append(temp_temp)
    return

def csv_load(filename):
    lines = []
    file_code = detect_character_code(filename)
    with open (filename, encoding=file_code) as csvfile:
        for line in csvfile.readlines():
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
        temp_Answer = temp_Answer.replace('__unk__', Unk_data)
    return temp_Answer

def generate_wav(text, speaker, filepath, voice_count_text):
    filepath = filepath + voice_count_text + '.wav'
    host = 'localhost'
    port = 50021
    params = (
        ('text', text),
        ('speaker', speaker),
    )
    response1 = requests.post(
        f'http://{host}:{port}/audio_query',
        params=params
    )
    headers = {'Content-Type': 'application/json',}
    response2 = requests.post(
        f'http://{host}:{port}/synthesis',
        headers=headers,
        params=params,
        data=json.dumps(response1.json())
    )

    wf = wave.open(filepath, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(24000)
    wf.writeframes(response2.content)
    wf.close()

if __name__ == "__main__":
    random.seed(None)
    init()
    app.run(host='127.0.0.1', port=5000, debug=True)
