import os
import sys
import pyperclip
import requests
from PyQt5 import QtCore, uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

form_class = uic.loadUiType("form.ui")[0]

PAPAGO_USER_ID     = ""  # client ID
PAPAGO_USER_SECRET = ""  # client secret
context = ""             # english request text
result  = ""             # korean response text
flag    = 0              # change flag

# 클립보드에 복사된 내용을 실시간으로 받아오는 스레드
# 클립보드의 내용과 context의 값과 다르면 flag를 0으로 만들고, 새로운 값을 저장한다.
class Thread(QThread):
    threadEvent = QtCore.pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__()
        pass

    def run(self):
        global context, flag
        while True:
            tmp = " ".join(pyperclip.paste().split())
            flag = int(context!=tmp)
            context = tmp
            self.threadEvent.emit(context)
            self.msleep(500) 


# GUI를 담당하는 class
# textEdit이 클립보드 출력 textedit widget이고, textEdit2가 번역 결과 출력 textedit widget이다.
# flag가 1이면(변경사항이 있으면) 번역 결과를 가져와 result에 넣어준다.
class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.th = Thread()
        self.th.threadEvent.connect(self.refresh)
        self.th.start()

    def refresh(self):
        global context, flag, result
        if flag:
            #result = self.get_smt_translate(context)
            result = self.get_nmt_translate(context)
            flag = 0
            self.textEdit.setText(context)
            self.textEdit_2.setText(result)
    
    # nmt 번역 api
    def get_nmt_translate(self, context):
        global PAPAGO_USER_ID, PAPAGO_USER_SECRET
        try:
            url = "https://openapi.naver.com/v1/papago/n2mt"
            headers= {"X-Naver-Client-Id": PAPAGO_USER_ID, "X-Naver-Client-Secret":PAPAGO_USER_SECRET}
            params = {"source": "en", "target": "ko", "text": context}
            response = requests.post(url, headers=headers, data=params)
            res = response.json()
            return res['message']['result']['translatedText']
        except:
            return "번역 실패"
            
    # smt 번역 api
    def get_smt_translate(self, context):
        global PAPAGO_USER_ID, PAPAGO_USER_SECRET
        try:
            url = "https://openapi.naver.com/v1/language/translate"
            headers= {"X-Naver-Client-Id": PAPAGO_USER_ID, "X-Naver-Client-Secret":PAPAGO_USER_SECRET}
            params = {"source": "en", "target": "ko", "text": context}
            response = requests.post(url, headers=headers, data=params)
            res = response.json()
            return res['message']['result']['translatedText']
        except:
            return "번역 실패"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
