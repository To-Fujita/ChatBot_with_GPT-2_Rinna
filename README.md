# ChatBot_with_GPT-2_Rinna

## 1. Description
This is a chat bot for Japanese based on the GPT-2 Rinna. You can talk to this chat bot by keyboard and/or voice.  
If you want to enjoy conversation in English, please check the "[ChatBot_with_ParlAI](https://github.com/To-Fujita/ChatBot_with_ParlAI)".

## 2. Operational Environment
- Windows 10/11 64-bit
- Visual Studio Code (VS Code)
- Python 3.9.4 64-bit
- Browser: Microsoft Edge or Google Chrome

## 3. Demo
![ChatBot_001](https://to-fujita.github.io/Images/Rinna_01.png "Images for ChatBot")
![ChatBot_002](https://to-fujita.github.io/Images/Rinna_02.png "Images for ChatBot")
![ChatBot_003](https://to-fujita.github.io/Images/Rinna_03.png "Images for ChatBot")

## 4. Details
I have confirmed this Python Script on the above conditions only. I will show you below how to execute the Python script.

### 4-1. Preparation
(a) Download & unzip the file.  
Please download following file and put these unzipped folder under the system path passed.
- ChatBot_with_GPT-2_Rinna: Please download from above "Code".

(b) Install some libraries to your Python  
Please install following libraries to your Python system.
- Pytorch: pip install torch
- Transformers: pip install transformers
- SentencePiece: pip install sentencepiece
- Janome: pip install janome
- Flask: pip install Flask

### 4-2. Try to communicate with the chat bot
The  Chat Bot program is as follow.
- main_JP_Rinna.py

Please open the above file by the VS Code, then click the "Run" and the "Start Debugging" or the "Run Without Debugging". Wait a few minutes, it will be displayed "*Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)" at the Terminal.
Then, after open the Browser, please input "http://127.0.0.1:5000". You can talk with the Chat Bot by keybord and/or voice.
  
If this script is not working well, please check your setting for system path and/or check your Python environment.
When you run the Rinna for the first time, it takes a few minutes to download various files. 
  
This Chat Bot is created in following concepts.
- The human interface is given in HTML and JavaScript.
- The answer from the chat bot is created in Python.

In this time, I used the "Dialog Element" in HTML. The Safari and the FireFox are not supported for the Dialog Element, yet. Therefor, it is not working well by the Safari and the FireFox. Please enjoy the talk with the Chat Bot on the Microsoft Edge or the Google Chrome.

## 5. Reference
- [GPT-2 Rinna](https://rinna.co.jp/)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Python](https://www.python.org/)

## 6. License
- Programs: MIT
- All of the images and GPT-2 Rinna: Please confirm to each author.

## 7. Author
[T. Fujita](https://github.com/To-Fujita)
