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
import pingying_preprocessing.pingying_preprocessing

logging.basicConfig(level=logging.DEBUG)


punctuationPat = re.compile("[,\.\?:;，。？、：；\n]+")
def getLokiResult(inputSTR):
    punctuationPat = re.compile("[,\.\?:;，。？、：；\n]+")
    inputLIST = punctuationPat.sub("\n", inputSTR).split("\n")
    filterLIST = []
    splitLIST = ["！", "，", "。", "？", "!", ",", "\n", "；", "\u3000", ";","."]
    resultDICT_family = family.family.execLoki(inputLIST, filterLIST=filterLIST, splitLIST=splitLIST)
    resultDICT_life_style = life_style.life_style.execLoki(inputLIST, filterLIST=filterLIST, splitLIST=splitLIST)
    resultDICT_money = money.money.execLoki(inputLIST, filterLIST=filterLIST, splitLIST=splitLIST)
    resultDICT_personality = personality.personality.execLoki(inputLIST, filterLIST=filterLIST, splitLIST=splitLIST)
    resultDICT_sex = sex.sex.execLoki(inputLIST, filterLIST=filterLIST, splitLIST=splitLIST)
    resultDICT_loyalty = loyalty.loyalty.execLoki(inputLIST, filterLIST=filterLIST, splitLIST=splitLIST)
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
        templateDICT = {    "id": messageAuthorID,
                             "updatetime" : datetime.now(),
                             "latestQuest": "",
                             "false_count" : 0
        }
        return templateDICT

    async def on_ready(self):
        # ################### Multi-Session Conversation :設定多輪對話資訊 ###################
        self.mscDICT = {
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
                    replySTR = "嗨嗨~我是感情小助理~\n可以協助您解決感情世界的疑難雜症~\n您可以試著問我有關男女朋友之間的煩惱\n"

# ##########非初次對話：這裡用 Loki 計算語意
            else: #開始處理正式對話
                #從這裡開始接上 NLU 模型
                count = 1
                if message.author.id not in self.mscDICT.keys():
                   self.mscDICT[message.author.id] = self.resetMSCwith(message.author.id)
                splitLIST = ["！", "，", "。", "？", "!", ",", "\n", "；", "\u3000", ";","."]
                resultDICT_pre = pingying_preprocessing.pingying_preprocessing.execLoki(msgSTR,splitLIST=splitLIST)
                if "correct" in resultDICT_pre:
                    msgSTR = resultDICT_pre["correct"][0]
                    logging.debug("Loki Result preprocessing => {}".format(resultDICT_pre))
                resultDICT_family,resultDICT_life_style,resultDICT_money,resultDICT_personality,resultDICT_sex,resultDICT_loyalty = getLokiResult(msgSTR)
                resultDICT_pre.clear()
                logging.debug("######\nLoki 處理結果如下：")
                replySTR = ""
                reply = False
                if "response" in resultDICT_family:
                    for i in range(len(resultDICT_family["response"])):
                        replySTR = replySTR +str(count)+". "+resultDICT_family["response"][i] + "\n\n"
                        count = count + 1
                    resultDICT_family.clear()
                    reply = True
                if "response" in resultDICT_life_style:
                    for i in range(len(resultDICT_life_style["response"])):
                        replySTR = replySTR +str(count)+". "+resultDICT_life_style["response"][i] + "\n\n"
                        count = count + 1
                    resultDICT_life_style.clear()
                    reply = True
                if "response" in resultDICT_money:
                    for i in range(len(resultDICT_money["response"])):
                        replySTR = replySTR +str(count)+". "+resultDICT_money["response"][i] + "\n\n"
                        count = count + 1
                    resultDICT_money.clear()
                    reply = True
                if "response" in resultDICT_personality:
                    for i in range(len(resultDICT_personality["response"])):
                        replySTR = replySTR +str(count)+". "+resultDICT_personality["response"][i] + "\n\n"
                        count = count + 1
                    resultDICT_personality.clear()
                    reply = True
                if "response" in resultDICT_sex:
                    for i in range(len(resultDICT_sex["response"])):
                        replySTR = replySTR +str(count)+". "+resultDICT_sex["response"][i] + "\n\n"
                        count = count + 1
                    resultDICT_sex.clear()
                    reply = True
                if "response" in resultDICT_loyalty:
                    for i in range(len(resultDICT_loyalty["response"])):
                        replySTR = replySTR +str(count)+". "+resultDICT_loyalty["response"][i] + "\n\n"
                        count = count + 1
                    resultDICT_loyalty.clear()
                    reply = True
                if reply == False:
                    self.mscDICT[message.author.id]["false_count"] += 1
                    if self.mscDICT[message.author.id]["false_count"] == 1:
                        replySTR = "很抱歉，我不太理解您的意思，您可以試著問我有關:\n1.家庭\n2.經濟\n3.個性\n4.生活習慣\n5.性事\n6.忠誠\n 以上6種方面的問題喔~"
                    elif self.mscDICT[message.author.id]["false_count"] >= 5:
                        replySTR = "夠了沒啦，就說聽不懂了"
                    else:
                        replySTR = "很抱歉，我還是不太理解您的意思，可能是您的狀況較為特殊，暫時無法給您回復"
                else:
                    self.mscDICT[message.author.id]["false_count"] = 0
                    replySTR = "我已經了解到你的困擾，以下是我給您的建議:\n\n\n" + replySTR + "\n\n請注意，以上回覆僅供參考，請自行評估問題的嚴重性以尋求專業人士的協助。"
            await message.reply(replySTR)
            
if __name__ == "__main__":
    with open("account.info", encoding="utf-8") as f: #讀取account.info
        accountDICT = json.loads(f.read())
    client = BotClient(intents=discord.Intents.default())
    client.run(accountDICT["discord_token"])
