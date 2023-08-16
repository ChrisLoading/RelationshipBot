#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki 4.0 Template For Python3

    [URL] https://api.droidtown.co/Loki/BulkAPI/

    Request:
        {
            "username": "your_username",
            "input_list": ["your_input_1", "your_input_2"],
            "loki_key": "your_loki_key",
            "filter_list": ["intent_filter_list"] # optional
        }

    Response:
        {
            "status": True,
            "msg": "Success!",
            "version": "v223",
            "word_count_balance": 2000,
            "result_list": [
                {
                    "status": True,
                    "msg": "Success!",
                    "results": [
                        {
                            "intent": "intentName",
                            "pattern": "matchPattern",
                            "utterance": "matchUtterance",
                            "argument": ["arg1", "arg2", ... "argN"]
                        },
                        ...
                    ]
                },
                {
                    "status": False,
                    "msg": "No matching Intent."
                }
            ]
        }
"""

from requests import post
from requests import codes
import json
import math
import os
import re
try:
    from intent import Loki_family
    from intent import Loki_money
    from intent import Loki_personality
    from intent import Loki_life_style
    from intent import Loki_sex
    from intent import Loki_loyalty
except:
    from .intent import Loki_family
    from .intent import Loki_money
    from .intent import Loki_personality
    from .intent import Loki_life_style
    from .intent import Loki_sex
    from .intent import Loki_loyalty


LOKI_URL = "https://api.droidtown.co/Loki/BulkAPI/"
try:
    accountInfo = json.load(open(os.path.join(os.path.dirname(__file__), "account.info"), encoding="utf-8"))
    USERNAME = accountInfo["username"]
    LOKI_KEY = accountInfo["loki_key"]
except Exception as e:
    print("[ERROR] AccountInfo => {}".format(str(e)))
    USERNAME = ""
    LOKI_KEY = ""

# 意圖過濾器說明
# INTENT_FILTER = []        => 比對全部的意圖 (預設)
# INTENT_FILTER = [intentN] => 僅比對 INTENT_FILTER 內的意圖
INTENT_FILTER = []
INPUT_LIMIT = 20

class LokiResult():
    status = False
    message = ""
    version = ""
    balance = -1
    lokiResultLIST = []

    def __init__(self, inputLIST, filterLIST):
        self.status = False
        self.message = ""
        self.version = ""
        self.balance = -1
        self.lokiResultLIST = []
        # filterLIST 空的就採用預設的 INTENT_FILTER
        if filterLIST == []:
            filterLIST = INTENT_FILTER

        try:
            result = post(LOKI_URL, json={
                "username": USERNAME,
                "input_list": inputLIST,
                "loki_key": LOKI_KEY,
                "filter_list": filterLIST
            })

            if result.status_code == codes.ok:
                result = result.json()
                self.status = result["status"]
                self.message = result["msg"]
                if result["status"]:
                    self.version = result["version"]
                    if "word_count_balance" in result:
                        self.balance = result["word_count_balance"]
                    self.lokiResultLIST = result["result_list"]
            else:
                self.message = "{} Connection failed.".format(result.status_code)
        except Exception as e:
            self.message = str(e)

    def getStatus(self):
        return self.status

    def getMessage(self):
        return self.message

    def getVersion(self):
        return self.version

    def getBalance(self):
        return self.balance

    def getLokiStatus(self, index):
        rst = False
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["status"]
        return rst

    def getLokiMessage(self, index):
        rst = ""
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["msg"]
        return rst

    def getLokiLen(self, index):
        rst = 0
        if index < len(self.lokiResultLIST):
            if self.lokiResultLIST[index]["status"]:
                rst = len(self.lokiResultLIST[index]["results"])
        return rst

    def getLokiResult(self, index, resultIndex):
        lokiResultDICT = None
        if resultIndex < self.getLokiLen(index):
            lokiResultDICT = self.lokiResultLIST[index]["results"][resultIndex]
        return lokiResultDICT

    def getIntent(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["intent"]
        return rst

    def getPattern(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["pattern"]
        return rst

    def getUtterance(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["utterance"]
        return rst

    def getArgs(self, index, resultIndex):
        rst = []
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["argument"]
        return rst

def runLoki(inputLIST, filterLIST=[], refDICT={}):
    resultDICT = refDICT
    lokiRst = LokiResult(inputLIST, filterLIST)
    if lokiRst.getStatus():
        for index, key in enumerate(inputLIST):
            lokiResultDICT = {}
            for resultIndex in range(0, lokiRst.getLokiLen(index)):
                # family
                if lokiRst.getIntent(index, resultIndex) == "family":
                    lokiResultDICT = Loki_family.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), lokiResultDICT, refDICT)

                # money
                if lokiRst.getIntent(index, resultIndex) == "money":
                    lokiResultDICT = Loki_money.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), lokiResultDICT, refDICT)

                # personality
                if lokiRst.getIntent(index, resultIndex) == "personality":
                    lokiResultDICT = Loki_personality.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), lokiResultDICT, refDICT)

                # life_style
                if lokiRst.getIntent(index, resultIndex) == "life_style":
                    lokiResultDICT = Loki_life_style.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), lokiResultDICT, refDICT)

                # sex
                if lokiRst.getIntent(index, resultIndex) == "sex":
                    lokiResultDICT = Loki_sex.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), lokiResultDICT, refDICT)

                # loyalty
                if lokiRst.getIntent(index, resultIndex) == "loyalty":
                    lokiResultDICT = Loki_loyalty.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), lokiResultDICT, refDICT)

            # save lokiResultDICT to resultDICT
            for k in lokiResultDICT:
                if k not in resultDICT:
                    resultDICT[k] = []
                if type(resultDICT[k]) != list:
                    resultDICT[k] = [resultDICT[k]] if resultDICT[k] else []
                if type(lokiResultDICT[k]) == list:
                    resultDICT[k].extend(lokiResultDICT[k])
                else:
                    resultDICT[k].append(lokiResultDICT[k])
    else:
        resultDICT["msg"] = lokiRst.getMessage()
    return resultDICT

def execLoki(content, filterLIST=[], splitLIST=[], refDICT={}):
    """
    input
        content       STR / STR[]    要執行 loki 分析的內容 (可以是字串或字串列表)
        filterLIST    STR[]          指定要比對的意圖 (空列表代表不指定)
        splitLIST     STR[]          指定要斷句的符號 (空列表代表不指定)
                                     * 如果一句 content 內包含同一意圖的多個 utterance，請使用 splitLIST 切割 content
        refDICT       DICT           參考內容

    output
        resultDICT    DICT           合併 runLoki() 的結果

    e.g.
        splitLIST = ["！", "，", "。", "？", "!", ",", "\n", "；", "\u3000", ";"]
        resultDICT = execLoki("今天天氣如何？後天氣象如何？")                      # output => ["今天天氣"]
        resultDICT = execLoki("今天天氣如何？後天氣象如何？", splitLIST=splitLIST) # output => ["今天天氣", "後天氣象"]
        resultDICT = execLoki(["今天天氣如何？", "後天氣象如何？"])                # output => ["今天天氣", "後天氣象"]
    """
    resultDICT = refDICT
    contentLIST = []
    if type(content) == str:
        contentLIST = [content]
    if type(content) == list:
        contentLIST = content

    resultDICT = {}
    if contentLIST:
        if splitLIST:
            # 依 splitLIST 做分句切割
            splitPAT = re.compile("[{}]".format("".join(splitLIST)))
            inputLIST = []
            for c in contentLIST:
                tmpLIST = splitPAT.split(c)
                inputLIST.extend(tmpLIST)
            # 去除空字串
            while "" in inputLIST:
                inputLIST.remove("")
        else:
            # 不做分句切割處理
            inputLIST = contentLIST

        # 依 INPUT_LIMIT 限制批次處理
        for i in range(0, math.ceil(len(inputLIST) / INPUT_LIMIT)):
            resultDICT = runLoki(inputLIST[i*INPUT_LIMIT:(i+1)*INPUT_LIMIT], filterLIST=filterLIST, refDICT=refDICT)
            if "msg" in resultDICT:
                break

    return resultDICT

def testLoki(inputLIST, filterLIST):
    INPUT_LIMIT = 20
    for i in range(0, math.ceil(len(inputLIST) / INPUT_LIMIT)):
        resultDICT = runLoki(inputLIST[i*INPUT_LIMIT:(i+1)*INPUT_LIMIT], filterLIST)

    if "msg" in resultDICT:
        print(resultDICT["msg"])

def testIntent():
    # family
    print("[TEST] family")
    inputLIST = ['婆婆管太多','被家人逼分手','他們家欠很多債','家庭背景差太多','家庭背景的關係','父母反對就分手','穩聊對象有家庭','要我趕快生孩子','他有他的家人要顧','原生家庭條件不好','婆婆很重視門當戶對','婆媳問題該怎麼處理','我不能接受他的家庭','男友從小被媽媽家暴','對方媽媽的控制欲很強','怎麼跟男友家人好好相處','該因為對方家庭而分手嗎','家庭環境因素改變不了而分手','他的家庭和價值觀與我不太相符','來自一個家裡沒有任何房子的家庭']
    testLoki(inputLIST, ['family'])
    print("")

    # money
    print("[TEST] money")
    inputLIST = ['他哪來的錢','我沒有經費','一起分攤房租','對方沒房沒車','情侶出遊費用','男友說房租要AA','助學貸款的關係','經濟條件很普通','對方月入2萬出頭','他真的都沒在存錢','同居還不用付房租','因為經濟能力自卑','我賺我男友的兩倍','女友什麼都要我付錢','女友出門都不帶錢包','男友常常偷家裡的錢','都是建立在金錢關係上','不想讓他覺得都是他在負擔','不要花費超過自己經濟能力','我跟另一半的經濟非常懸殊','沒辦法回送金額相當的禮物','真的要因為經濟能力分手嗎','怕他覺得我是一直花他錢的女生','有一定的經濟能力才能給對方好的未來']
    testLoki(inputLIST, ['money'])
    print("")

    # personality
    print("[TEST] personality")
    inputLIST = ['女友超黏我','男友超囉嗦','男友超煩人','女友像老媽子','女友管東管西','我男友不夠懂我','我男友個性不好','男友很喜歡抱怨','我男友個性很小氣','跟男友價值觀不合','我們經常為了小事爭吵','我很常覺得自己被忽視','跟男友在一起很不快樂','他似乎對我越來越不在意','常覺得自己什麼都做不好','我不知道他是不是真心愛我','吵架的時候對方老愛講難聽的話','男友什麼事情都要跟我斤斤計較','我覺得我們彼此的興趣愈來愈少交集','我覺得我在這段感情中付出的比對方多','越來越容易看到另一半的缺點更勝於優點']
    testLoki(inputLIST, ['personality'])
    print("")

    # life_style
    print("[TEST] life_style")
    inputLIST = ['作息不一致','男友沒未來','我男友超髒的','女友要我陪她聊天','男友去哪都不報備','我男友生活習慣很差','男友回家衣服都亂丟','男友睡覺打呼超大聲','我們的生活步調不一致','男友一直打電動不陪我','男友很常回家都不陪我','下班回家只想一個人靜靜','男友上廁所都不掀馬桶蓋','一直都遠距離不知道該怎麼辦','女友點很多餐點但每次都吃不完','我男友每天都要加班到很晚才回來','我注重健康飲食，男友愛吃垃圾食物','我習慣早起，男友都要三更半夜才睡','跟男友不同縣市工作生活作息不同步','覺得每天至少一次講電話或視訊很沒有必要']
    testLoki(inputLIST, ['life_style'])
    print("")

    # sex
    print("[TEST] sex")
    inputLIST = ['不做愛有錯嗎','性冷感怎麼辦','男友不愛戴套','女友是死亡海鮮','性事不合怎麼辦','無性生活想分手','男友有包莖問題','男友的性欲太強','性癖很多的另一半','我們性需求不一致','把我當發洩的工具','月事來男友還想做','男友太持久怎麼辦','找各種藉口逃避性事','對床事態度越來越冷淡','感覺自己沒有服務到她','抱怨我怎麼性慾那麼大','伴侶不願意討論床事問題','我需求很大但就是有點快','為什麼一定要婚前性行為','男友喜歡趁我還沒醒弄我','女友在性事方面好像變了個人','沒有心靈上兩人互相滿足的感覺','不小心幫他摸到睡著他就開始不爽了']
    testLoki(inputLIST, ['sex'])
    print("")

    # loyalty
    print("[TEST] loyalty")
    inputLIST = ['我被戴綠帽了','同時跟我在一起','男友腳踏兩條船','一夜情算不算出軌','偷偷下載交友軟體','出軌跟健身教練玩','前陣子被男友劈腿','她因為無聊出軌了','已經原諒過他一次了','已經給過他一次機會了','我對他有一些不信任感','發現女友跟別人劈腿了','男友很愛跟其他女生搞曖昧','男友很愛跟前女友藕斷絲連','對方還留著前任的物品該怎麼辦','我對他的信任可以說是完全破滅','開始懷疑我是不是以工作為名外遇','開始懷疑我是不是變心了才不想被碰','我不在的時候都是另一個女孩在他身邊','他除了劈腿以外其他條件都符合我的擇偶標準']
    testLoki(inputLIST, ['loyalty'])
    print("")


if __name__ == "__main__":
    # 測試所有意圖
    testIntent()

    # 測試其它句子
    filterLIST = []
    splitLIST = ["！", "，", "。", "？", "!", ",", "\n", "；", "\u3000", ";"]
    # 設定參考資料
    refDICT = {
        #"key": []
    }
    resultDICT = execLoki("今天天氣如何？後天氣象如何？", filterLIST=filterLIST, refDICT=refDICT)                      # output => {"key": ["今天天氣"]}
    resultDICT = execLoki("今天天氣如何？後天氣象如何？", filterLIST=filterLIST, splitLIST=splitLIST, refDICT=refDICT) # output => {"key": ["今天天氣", "後天氣象"]}
    resultDICT = execLoki(["今天天氣如何？", "後天氣象如何？"], filterLIST=filterLIST, refDICT=refDICT)                # output => {"key": ["今天天氣", "後天氣象"]}