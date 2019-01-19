import os
import sys
import pyperclip
import requests
from PyQt5 import QtCore, uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

form_class = uic.loadUiType("form.ui")[0]

PAPAGO_USER_ID     = ""
PAPAGO_USER_SECRET = ""
context = ""
result  = ""
flag    = 0

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
            #result = self.get_smt_translte(context)
            result = self.get_nmt_translte(context)
            flag = 0
            self.textEdit.setText(context)
            self.textEdit_2.setText(result)
    
    def get_nmt_translte(self, context):
        try:
            request_url = "https://openapi.naver.com/v1/papago/n2mt"
            headers= {"X-Naver-Client-Id": USER_ID, "X-Naver-Client-Secret":USER_SECRET}
            params = {"source": "en", "target": "ko", "text": context}
            response = requests.post(request_url, headers=headers, data=params)
            res = response.json()
            return res['message']['result']['translatedText']
        except:
            return "번역 실패"
            
    def get_smt_translte(self, context):
        try:
            request_url = "https://openapi.naver.com/v1/language/translate"
            headers= {"X-Naver-Client-Id": USER_ID, "X-Naver-Client-Secret":USER_SECRET}
            params = {"source": "en", "target": "ko", "text": context}
            response = requests.post(request_url, headers=headers, data=params)
            res = response.json()
            return res['message']['result']['translatedText']
        except:
            return "번역 실패"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
