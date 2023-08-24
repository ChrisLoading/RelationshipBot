#!/user/bin/env python
# -*- coding: utf-8 -*-

import logging
import discord
import json
import re
from datetime import datetime
from pprint import pprint
import sys

sys.path.append('/family')
sys.path.append('/life_style')
sys.path.append('/loyalty')
sys.path.append('/money')
sys.path.append('/personality')
sys.path.append('/sex')

import family.family
import life_style.life_style
import loyalty.loyalty
import money.money
import personality.personality
import sex.sex

logging.basicConfig(level=logging.DEBUG)


punctuationPat = re.compile("[,\.\?:;，。？、：；\n]+")
def getLokiResult(inputSTR):
    punctuationPat = re.compile("[,\.\?:;，。？、：；\n]+")
    inputLIST = punctuationPat.sub("\n", inputSTR).split("\n")
    filterLIST = []
    resultDICT_family = family.family.runLoki(inputLIST, filterLIST)
    resultDICT_life_style = life_style.life_style.runLoki(inputLIST, filterLIST)
    resultDICT_money = money.money.runLoki(inputLIST, filterLIST)
    resultDICT_personality = personality.personality.runLoki(inputLIST, filterLIST)
    resultDICT_sex = sex.sex.runLoki(inputLIST, filterLIST)
    resultDICT_loyalty = loyalty.loyalty.runLoki(inputLIST, filterLIST)
    logging.debug("Loki Result family => {}".format(resultDICT_family))
    logging.debug("Loki Result life_style => {}".format(resultDICT_life_style))
    logging.debug("Loki Result money => {}".format(resultDICT_money))
    logging.debug("Loki Result personality => {}".format(resultDICT_personality))
    logging.debug("Loki Result sex => {}".format(resultDICT_sex))
    logging.debug("Loki Result loyalty => {}".format(resultDICT_loyalty))
    return resultDICT_family,resultDICT_life_style,resultDICT_money,resultDICT_personality,resultDICT_sex,resultDICT_loyalty

class BotClient(discord.Client):

    def resetMSCwith(self, messageAuthorID):
        '''
        清空與 messageAuthorID 之間的對話記錄
        '''
        templateDICT = self.templateDICT
        templateDICT["updatetime"] = datetime.now()
        return templateDICT

    async def on_ready(self):
        # ################### Multi-Session Conversation :設定多輪對話資訊 ###################
        self.templateDICT = {"updatetime" : None,
                             "latestQuest": ""
        }
        self.mscDICT = { #userid:templateDICT
        }
        # ####################################################################################
        print('Logged on as {} with id {}'.format(self.user, self.user.id))

    async def on_message(self, message):
        # Don't respond to bot itself. Or it would create a non-stop loop.
        # 如果訊息來自 bot 自己，就不要處理，直接回覆 None。不然會 Bot 會自問自答個不停。
        if message.author == self.user:
            return None

        logging.debug("收到來自 {} 的訊息".format(message.author))
        logging.debug("訊息內容是 {}。".format(message.content))
        if self.user.mentioned_in(message):
            replySTR = "我是預設的回應字串…你會看到我這串字，肯定是出了什麼錯！"
            logging.debug("本 bot 被叫到了！")
            msgSTR = message.content.replace("<@{}> ".format(self.user.id), "").strip()
            logging.debug("人類說：{}".format(msgSTR))
            
# ##########初次對話：這裡是 keyword trigger 的。
            if msgSTR.lower() in ["哈囉","嗨","你好","您好","hi","hello"]:
                #有講過話(判斷對話時間差)
                if message.author.id in self.mscDICT.keys():
                    timeDIFF = datetime.now() - self.mscDICT[message.author.id]["updatetime"]
                    #有講過話，但與上次差超過 5 分鐘(視為沒有講過話，刷新template)
                    if timeDIFF.total_seconds() >= 300:
                        self.mscDICT[message.author.id] = self.resetMSCwith(message.author.id)
                        replySTR = "嗨嗨，我們好像見過面，但卓騰的隱私政策不允許我記得你的資料，抱歉！"
                    #有講過話，而且還沒超過5分鐘就又跟我 hello (就繼續上次的對話)
                    else:
                        replySTR = self.mscDICT[message.author.id]["latestQuest"]
                #沒有講過話(給他一個新的template)
                else:
                    self.mscDICT[message.author.id] = self.resetMSCwith(message.author.id)
                    replySTR = msgSTR.title()

# ##########非初次對話：這裡用 Loki 計算語意
            else: #開始處理正式對話
                #從這裡開始接上 NLU 模型
                resultDICT_family,resultDICT_life_style,resultDICT_money,resultDICT_personality,resultDICT_sex,resultDICT_loyalty = getLokiResult(msgSTR)
                logging.debug("######\nLoki 處理結果如下：")
                replySTR = ""
                reply = False
                if "response" in resultDICT_family:
                    replySTR = resultDICT_family["response"][0] + "\n"
                    resultDICT_family.clear()
                    reply = True
                if "response" in resultDICT_life_style:
                    replySTR = replySTR + resultDICT_life_style["response"][0] + "\n"
                    resultDICT_life_style.clear()
                    reply = True
                if "response" in resultDICT_money:
                    replySTR = replySTR + resultDICT_money["response"][0]+ "\n"
                    resultDICT_money.clear()
                    reply = True
                if "response" in resultDICT_personality:
                    replySTR = replySTR + resultDICT_personality["response"][0]+ "\n"
                    resultDICT_personality.clear()
                    reply = True
                if "response" in resultDICT_sex:
                    replySTR = replySTR + resultDICT_sex["response"][0]+ "\n"
                    resultDICT_sex.clear()
                    reply = True
                if "response" in resultDICT_loyalty:
                    replySTR = replySTR + resultDICT_loyalty["response"][0]+ "\n"
                    resultDICT_loyalty.clear()
                    reply = True
            if reply == False:
                replySTR = "聽不懂喔~可以再說的詳細一點嗎?"
            await message.reply(replySTR)
            
if __name__ == "__main__":
    with open("account.info", encoding="utf-8") as f: #讀取account.info
        accountDICT = json.loads(f.read())
    client = BotClient(intents=discord.Intents.default())
    client.run(accountDICT["discord_token"])
