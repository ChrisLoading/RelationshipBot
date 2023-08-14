#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from ArticutAPI import Articut
from requests import post
from pprint import pprint
from time import sleep
import json
with open("account.info", encoding="utf-8") as f:
    accountDICT = json.load(f)
articut = Articut(username=accountDICT["username"], apikey=accountDICT["api_key"])

def intentCreate(usernameSTR, lokiKeySTR, projectNameSTR, intentSTR, typeSTR):


    url = "https://api.droidtown.co/Loki/Call/"  #線上版 URL

    payload = {
        "username" : usernameSTR, # 這裡填入您在 https://api.droidtown.co 使用的帳號 email。     Docker 版不需要此參數！
        "loki_key" : lokiKeySTR, # 這裡填入您在 https://api.droidtown.co 登入後取得的 loki_key。 Docker 版不需要此參數！
        "project": projectNameSTR, #專案名稱 (請先在 Loki 的設定網頁裡建立一個 Project 以便取得它的專案金鑰 (loki_key)
        "intent": intentSTR, #意圖名稱
        "func": "create_intent",
        "data": {
            "type": typeSTR #意圖類別
        }
    }

    response = post(url, json=payload).json()
    #pprint(response)
    return response

def utteranceInsert(usernameSTR, lokiKeySTR, projectNameSTR, intentSTR, utteranceList, checkList):


    url = "https://api.droidtown.co/Loki/Call/"  #線上版 URL

    payload = {
        "username" : usernameSTR, # 這裡填入您在 https://api.droidtown.co 使用的帳號 email。     Docker 版不需要此參數！
        "loki_key" : lokiKeySTR, # 這裡填入您在 https://api.droidtown.co 登入後取得的 loki_key。 Docker 版不需要此參數！
        "project": projectNameSTR, #專案名稱 (請先在 Loki 的設定網頁裡建立一個 Project 以便取得它的專案金鑰 (loki_key)
        "intent": intentSTR, #意圖名稱
        "func": "insert_utterance",
        "data": {
            "utterance": utteranceList,
            "checked_list": checkList
        }
    }

    response = post(url, json=payload).json()
    #pprint(response)
    return response


if __name__ == "__main__":


    intentLIST = ["sex","loyalty"]

    usernameSTR=accountDICT["username"]
    lokiKeySTR=accountDICT["loki_key"]
    projectNameSTR="RelationshipBot"
    

    for intentSTR in intentLIST:
        print(intentSTR)
        createResult = intentCreate(usernameSTR,
                                    lokiKeySTR,
                                    projectNameSTR,
                                    intentSTR=intentSTR,
                                    typeSTR="basic")
        sleep(0.3)
        print("Result:", createResult)
        
    with open("utterance.json", encoding="utf-8") as f:
        uList = json.load(f)
        
    for intentSTR in intentLIST:
        print(intentSTR)
        createResult = utteranceInsert(usernameSTR,
                                        lokiKeySTR,
                                        projectNameSTR,
                                        intentSTR=intentSTR,
                                        utteranceList=uList["utterance"][0][intentSTR],
                                        checkList=uList["check"])
        print("\nResult:\n",createResult,"\n")