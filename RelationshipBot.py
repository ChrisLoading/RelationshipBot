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
    from intent import Loki_life_style
    from intent import Loki_loyalty
    from intent import Loki_money
    from intent import Loki_personality
    from intent import Loki_sex
    from intent import Loki_personality_adv
except:
    from .intent import Loki_family
    from .intent import Loki_life_style
    from .intent import Loki_loyalty
    from .intent import Loki_money
    from .intent import Loki_personality
    from .intent import Loki_sex
    from .intent import Loki_personality_adv


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

                # life_style
                if lokiRst.getIntent(index, resultIndex) == "life_style":
                    lokiResultDICT = Loki_life_style.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), lokiResultDICT, refDICT)

                # loyalty
                if lokiRst.getIntent(index, resultIndex) == "loyalty":
                    lokiResultDICT = Loki_loyalty.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), lokiResultDICT, refDICT)

                # money
                if lokiRst.getIntent(index, resultIndex) == "money":
                    lokiResultDICT = Loki_money.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), lokiResultDICT, refDICT)

                # personality
                if lokiRst.getIntent(index, resultIndex) == "personality":
                    lokiResultDICT = Loki_personality.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), lokiResultDICT, refDICT)

                # sex
                if lokiRst.getIntent(index, resultIndex) == "sex":
                    lokiResultDICT = Loki_sex.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), lokiResultDICT, refDICT)

                # personality_adv
                if lokiRst.getIntent(index, resultIndex) == "personality_adv":
                    lokiResultDICT = Loki_personality_adv.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), lokiResultDICT, refDICT)

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
    inputLIST = ['婆婆管太多怎麼辦','婆媳問題該怎麼處理','被家人逼分手怎麼辦','男友家欠很多債怎麼辦','穩聊對象有家庭怎麼辦','怎麼跟男友家人好好相處','該因為對方家庭而分手嗎','該因為父母反對就分手嗎','婆婆很重視門當戶對怎麼辦','對方要我趕快生孩子怎麼辦','我不能接受他的家庭怎麼辦','男友從小被媽媽家暴怎麼辦','男友有他的家人要顧怎麼辦','雙方家庭背景差太多怎麼辦','家庭背景的關係想分手怎麼辦','對方原生家庭條件不好怎麼辦','對方媽媽的控制欲很強怎麼辦','家庭環境因素改變不了想分手怎麼辦','他的家庭和價值觀與我不太相符怎麼辦','對方來自一個家裡沒有任何房子的家庭怎麼辦']
    testLoki(inputLIST, ['family'])
    print("")

    # life_style
    print("[TEST] life_style")
    inputLIST = ['女友嘴臭','作息不一致','她亂丟垃圾','她習慣很糟','男友沒未來','我男友超髒的','男友不愛回家','男友亂丟垃圾','男友前途渺茫','女友回家都不講','男友都不做家事','女友要我陪她聊天','男友去哪都不報備','男友毫無前途可言','她堅持睡覺不開冷氣','我男友生活習慣很差','男友回家衣服都亂丟','男友睡覺打呼超大聲','女友堅持睡覺不開冷氣','我們的生活步調不一致','男友一直加班都不陪我','男友一直打電動不陪我','男友很常回家都不陪我','下班回家只想一個人靜靜','女友一直跟我說八卦好吵','男友上廁所都不掀馬桶蓋','男友無法對未來做出計劃','男友無論去哪都不告訴我','他常常點一堆東西都不吃完','我男友特別不愛整理房間。','我男朋友特別不注重衛生。','每天起床睡覺的時間不一致','男友不管到哪都不與我溝通','男友囉哩八唆的，我想分手','男友睡覺時打呼聲音超響。','一直都遠距離不知道該怎麼辦','我男友睡眠打呼聲音非常吵。','每日的休息時間無法保持一致','男友出門從來不報備任何行蹤','遠距離生活好多年了該怎麼辦','女友點很多餐點但每次都吃不完','我男友總是工作到很晚才回家。','我的男友特別懶散，不愛乾淨。','男友去任何地方都不事先告訴我','男友回家時衣服總是隨處亂放。','我男友每天都要加班到很晚才回來','我男友總是會工作到很晚才回家。','我的另一半完全不重視個人衛生。','放工回家後喜歡享受獨處的寂靜。','我注重健康飲食，男友愛吃垃圾食物','我男友對保持整潔的概念毫不在意。','我男友通常辛勤工作到很晚才回家。','我習慣早起，男友都要三更半夜才睡','跟男友不同縣市工作生活作息不同步','我對於處理遠距離問題一直感到無助。','我男友每次上廁所都不會掀起馬桶蓋。','我的男友總是在打電動，不願意陪我。','每次女友都點很多餐點，但都吃不完。','每次女友點這麼多餐點，但都吃不完。','每次我男友上廁所都沒有掀開馬桶蓋。','男友回到家總愛把衣服丟得滿地都是。','女友常常點很多餐點，但每次都吃不完。','女友每次都點那麼多餐點，但都吃不完。','希望在下班後能夠享受獨自一人的寂靜。','我始終無法找到解決遠距離問題的方法。','我男友從來不會把馬桶蓋掀起來上廁所。','我男友每天都要辛苦工作到很晚才回來。','我的男友整天只顧著玩電動，從不陪我。','下班回家後希望獨自一人享受平靜的時光。','我男友不管上廁所多少次都不願掀馬桶蓋。','我的男友整天都在打電動，從不抽空陪我。','我總是習慣早起，而男友總是在深夜才睡。','每天晚上我男友都要加班到很晚才能回來。','覺得每天至少一次講電話或視訊很沒有必要','長期以來一直都苦惱於解決遠距離的問題。','對於長期的遠距離關係，我一直都束手無策。','男友回到家時，衣服總是亂亂丟得滿地都是。','我一直不知道該如何應對長時間的遠距離關係。','我習慣清晨起床，可男友卻經常在深夜才躺下。','我重視健康的飲食習慣，男友卻偏好吃垃圾食品。','我習慣在早上起床，而男友則偏向晚上才進入夢鄉。','跟男友不同地點工作導致我們的生活作息各自獨立。','我的男友一直沉迷在電動遊戲中，從不顧及我的存在。','我的男友非常放任自己的環境，經常讓房間變得髒亂。','男友和我分隔兩地工作，導致我們的生活作息不同頻率。','我和男友在不同縣市工作，導致我們的生活作息無法統一。','我非常重視健康飲食，可是我的男友卻總是愛吃垃圾食物。','男友和我在不同縣市工作，所以我們的生活作息毫無交集。','長時間以來一直都面臨遠距離的困擾，不知道要怎麼解決。','我注重健康的飲食習慣，但我男友喜歡吃不健康的垃圾食物。','跟男友互不干擾的工作於不同縣市，導致我們的生活作息不協調。']
    testLoki(inputLIST, ['life_style'])
    print("")

    # loyalty
    print("[TEST] loyalty")
    inputLIST = ['被戴綠帽','被女友戴綠帽','男友腳踏兩條船','一夜情算不算出軌','已經原諒過他一次','變心了才不想被碰','女友和陌生人一夜情','已經給過他一次機會','女友出軌跟健身教練玩','女友同時跟別人在一起','對方還留著前任的物品','對男友有一些不信任感','對男友的信任完全破滅','我無法克制自己不出軌','有另一個女生在他身邊','男友偷偷下載交友軟體','男友跟前女友藕斷絲連','男友會跟其他女生搞曖昧','男友很愛跟其他女生搞曖昧','除了劈腿以外其他條件都符合我的擇偶標準']
    testLoki(inputLIST, ['loyalty'])
    print("")

    # money
    print("[TEST] money")
    inputLIST = ['男友說房租要AA','男友沒房沒車怎麼辦','同居還不付房租怎麼辦','他真的都沒在存錢怎麼辦','因為經濟能力自卑怎麼辦','女友什麼都要我付錢怎麼辦','女友出門都不帶錢包怎麼辦','我賺的是我男友兩倍怎麼辦','男友常常偷家裡的錢怎麼辦','男友經濟條件很普通怎麼辦','真的要因為經濟能力分手嗎','男友月入只有2萬出頭怎麼辦','因為經濟問題想提分手會很壞嗎','怎麼不要讓對方覺得都是他在負擔','感情都是建立在金錢關係上怎麼辦','我跟另一半的經濟非常懸殊怎麼辦','沒辦法回送金額相當的禮物怎麼辦','怎麼勸對方不要花費超過自己經濟能力','怕他覺得我是一直花他錢的女生怎麼辦','有一定的經濟能力才能給對方好的未來嗎']
    testLoki(inputLIST, ['money'])
    print("")

    # personality
    print("[TEST] personality")
    inputLIST = ['他超黏我','她很囉唆','女友超黏我','她很愛抱怨','男友超囉嗦','男友超煩人','女友像老媽子','女友管東管西','男友嘴巴很臭','對方很愛講髒話','我男友不夠懂我','我男友個性不好','男友很喜歡抱怨','真受不了另一半','對方很愛侮辱我 ','女友像老媽子一般','女友和老媽子類似','我男友個性很小氣','我男友相當小氣。','我男友非常小氣。','我男友非常節儉。','跟男友價值觀不合','女友對我超級依賴。','女友對我超級黏人。','女友有老媽子的味道','女友有老媽子的特質','女朋友跟老媽子一樣','我的男友超級麻煩。','男友動不動就爆粗口','女友具備老媽子的特性','我們經常為了小事爭吵','我常感到自己被忽略了','我很常覺得自己被忽視','我時常覺得自己被輕忽','我男友很吝嗇的性格。','我的另一半話真的多。','我的男友不太理解我。','我的男友有點愛說話。','我的男友特別愛說話。','我的男朋友說話超多。','我經常感到自己被忘記','我經常感到自己被忽視','男友實在是超級囉嗦。','男朋友經常愛發牢騷。','與男友的價值觀相反。','與男友的價值觀相左。','與男友的價值觀相悖。','跟男友在一起很不快樂','這位男友真的好煩人。','他似乎對我越來越不在意','受不了管東管西的另一半','和男友交往時心情很差。','常覺得自己什麼都做不好','我們常常因小事而爭吵。','我常常感到自己不被重視','我常常感到自己被無視了','我的伴侶對我不夠瞭解。','我的伴侶特別喜歡抱怨。','我的伴侶總是善於抱怨。','我的男友常常嘮叨不已。','我的男友真的很煩人啊！','我的男友總是說個不停。','我的男友超愛絮絮叨叨。','我經常覺得自己被冷落了','每每因小事而發生矛盾。','男友從來不在乎我的感受','男友簡直讓人頭痛不已。','真是個讓人頭痛的男友。','與男友的價值觀不相符。','與男友的價值觀有分歧。','與男友的價值觀有衝突。','他似乎對我越來越不重視。','他好像對我漸漸失去關心。','他好像對我越來越不關注。','他看起來對我越來越冷淡。','他顯然對我漸漸不在意了。','我不知道他是不是真心愛我','我的伴侶喜歡不斷發牢騷。','我的另一半對我欠缺共鳴。','我的另一半總是嘮叨不停。','我的男友實在太過囉唆了。','我的男友經常抱怨一切事。','總是認為自己做事不夠好。','跟男友的價值觀背道而馳。','跟男友相處真的太辛苦了。','他似乎對我越來越不關心了。','他看起來對我漸漸失去興趣。','常常覺得自己的表現不優秀。','我們經常為一些小事而爭吵。','我們總是因小事而產生爭議。','我男友對我的想法不夠重視。','我的伴侶總是喜歡抱怨事情。','男友對什麼事情都非常計較。','經常覺得自己做事不太出色。','總是覺得自己做事不夠出眾。','交往到後期都看不到對方的好了','他像是越來越不把我放在心上。','他像是越來越不把我放在眼裡。','吵架的時候對方老愛講難聽的話','和男友共處時我感到非常不滿。','在男友身邊讓我覺得非常煩躁。','小事常常引起我們之間的爭吵。','小事往往成為我們爭吵的原因。','我不知道他是否對我真正投入。','我們常因些微問題而爭吵不休。','我無法肯定他是否真心地愛我。','我男友對任何事情都患得患失。','我男友對於我的情感不夠體諒。','我的伴侶對我缺乏深刻的理解。','每天面對男友真的讓人受不了。','男友什麼事情都要跟我斤斤計較','與男友在一起時心情無比沮喪。','常為一些微不足道的事情而爭吵。','我的伴侶對我心境的理解度不夠。','我的男友對每件事情都非常挑剔。','與男友交往讓我感到非常不舒適。','與男友共度時光讓我覺得很痛苦。','與男友相處讓我感到非常不開心。','就算是小事，我們也常常為之爭執。','我的伴侶對於每個細節都特別在意。','我的另一半不甚瞭解我的內心需求。','我的男朋友好像無時無刻都在抱怨。','我覺得我們彼此的興趣愈來愈少交集','我認為我們的興趣越來越不相投了。','經常覺得自己在各方面做得不夠好。','跟男友在一起沒有任何快樂的感覺。','跟男友在一起的時候心情格外沉重。','吵架的時候，對方總是喜歡口出惡言。','我無法確定他是否真心地對我有感情。','我的伴侶總是對每件小事都極為挑剔。','我覺得我們的興趣愈來愈少共同之處。','我覺得我在這段感情中付出的比對方多','不管什麼事情，我的男友總是喜歡計較。','吵架的時候，對方總是口出狂言傷害人。','我的另一半總是對每件事情都斤斤計較。','我的男朋友似乎對很多事情都抱怨不已。','我的男朋友對任何事情都十分斤斤計較。','我認為我們之間的興趣愈來愈不一致了。','我認為我在這段感情中貢獻的比對方多。','越來越容易看到另一半的缺點更勝於優點','不時會覺得自己在各個方面都做得不太好。','吵架的時候，對方常常使用冷嘲熱諷的語言。','在我看來，我們之間的興趣越來越少交集了。','在我看來，我們之間的興趣越來越少重疊了。','在這段感情中，我認為我所付出的勝過對方。','我覺得我在這段感情中所付出的超過了對方。','吵架的時候，對方常常用刻薄的言辭攻擊對方。','我有感受到我在這段感情中所承擔的比對方大。','吵架的時候，對方總是用傷人的話語來挑釁對方。','吵架的時候，對方老愛質疑人和使用傷人的語言。','比起對方，我覺得我在這段感情中貢獻的多一點。','吵架的時候，對方常常使用激烈的詞句來侮辱對方。','我們越來越容易注意到另一半的不足之處，而不是優點。','隨著相處時間增加，我們越來越容易看到另一半的不足。','隨著相處時間的增長，我們越來越容易看到另一半的缺陷超過優點。']
    testLoki(inputLIST, ['personality'])
    print("")

    # sex
    print("[TEST] sex")
    inputLIST = ['性事不合','男友太持久','不做愛有錯嗎','男友不愛戴套','男友硬不起來','女友是死亡海鮮','女友的鮑魚很臭','無性生活想分手','用的我很不舒服','男友有包莖問題','男友的包皮過長','男友的性慾太強','另一半的性癖很多','女友幫我摸到睡著','把我用的很不舒服','把我當發洩的工具','月事來男友還想做','男友不愛用保險套','找各種藉口逃避性事','沒有互相滿足的感覺','對床事態度越來越冷淡','感覺自己沒有服務到她','抱怨我怎麼性慾那麼大','伴侶不願意討論床事問題','為什麼一定要婚前性行為','男友喜歡趁我還沒醒弄我','我需求很大但就是有一點快','女友在性事方面好像變了個人']
    testLoki(inputLIST, ['sex'])
    print("")

    # personality_adv
    print("[TEST] personality_adv")
    inputLIST = ['男友不愛回家','女友都不接電話','男友電話都不接']
    testLoki(inputLIST, ['personality_adv'])
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