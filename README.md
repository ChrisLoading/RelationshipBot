# 感情小助理 RelationshipBot
### 內容列表
- [Bot介紹](##Bot介紹)
- [專案目錄](##專案目錄)
- [環境設置](##環境設置)
- [Loki啟用說明](##Loki啟用說明)
- [Discord Bot建置](##DiscordBot建置)
- [使用者互動說明](##使用者互動說明)
- [參考資料](##參考資料)
- [作者](##作者)
## Bot介紹 


## 專案目錄
```
.
├── Discord_bot.py                     # DISCORD 連接
├── README.md
├── family                             # Context "家庭"
│   ├── intent                         # Context為"家庭"下的意圖
│   │   ├── Loki_family.py
│   │   ├── USER_DEFINED.json          
│   │   └── Updater.py
│   ├── family.py                      # Context"家庭"的主程式
│   └── reply                          # Context為"家庭"下的回覆
│       └── reply_family.json
├── life_style                         # Context "生活習慣"
│   ├── intent                         # Context為"生活習慣"下的意圖
│   │   ├── Loki_future.py
│   │   ├── Loki_habit.py
│   │   ├── Loki_long_distance.py
│   │   ├── Loki_work.py
│   │   ├── USER_DEFINED.json          
│   │   └── Updater.py
│   ├── life_style.py                  # Context"生活習慣"的主程式
│   └── reply                          # Context為"生活習慣"下的回覆 
│       ├── reply_future.json
│       ├── reply_habit.json
│       ├── reply_long_distance.json
│       └── reply_work.json
├── loyalty                             # Context "忠誠"
│   ├── intent                          # Context為"忠誠"下的意圖
│   │   ├── Loki_other.py
│   │   ├── Loki_self.py
│   │   ├── USER_DEFINED.json           
│   │   └── Updater.py
│   ├── loyalty.py                      # Context"忠誠"的主程式
│   └── reply                           # Context為"忠誠"下的回覆
│       ├── reply_other.json
│       └── reply_self.json
├── money                               # Context "經濟"
│   ├── intent                          # Context為"經濟"下的意圖
│   │   ├── Loki_money.py
│   │   ├── USER_DEFINED.json
│   │   └── Updater.py
│   ├── money.py                        # Context"經濟"的主程式
│   └── reply                           # Context為"經濟"下的回覆
│       └── reply_money.json
├── personality                         # Context "個性"
│   ├── intent                          # Context為"個性"下的意圖
│   │   ├── Loki_care.py
│   │   ├── Loki_care_adv.py
│   │   ├── Loki_fight.py
│   │   ├── Loki_trait.py
│   │   ├── Loki_trait_adv.py
│   │   ├── USER_DEFINED.json
│   │   └── Updater.py
│   ├── personality.py                  # Context"個性"的主程式
│   └── reply                           # Context為"個性"下的回覆
│       ├── reply_care.json
│       ├── reply_fight.json
│       └── reply_trait.json
├── sex                                 # Context "性事"
│    ├── intent                         # Context為"性事"下的意圖
│    │   ├── Loki_both.py
│    │   ├── Loki_boyfriend.py
│    │   ├── Loki_girlfriend.py
│    │   ├── USER_DEFINED.json
│    │   └── Updater.py
│    ├── sex.py                         # Context"性事"的主程式
│    └── reply                          # Context為"性事"下的回覆
│        ├── reply_both.json
│        ├── reply_boyfriend.json
│        └── reply_girlfriend.json
├── pingying_preprocessing              #前處理
│   ├── intent
│   │   ├── Loki_dcard.py
│   │   ├── Loki_ig.py
│   │   ├── Loki_line.py
│   │   ├── Loki_pow.py
│   │   ├── Loki_ptt.py
│   │   ├── Loki_sex.py
│   │   ├── USER_DEFINED.json
│   │   └── Updater.py
│   └── pingying_preprocessing.py
└── ref                             # 6個不同Context+前處理的ref檔
   ├── family_ref
   │   └── family.ref
   ├── life_style_ref
   │   ├── future.ref
   │   ├── habit.ref
   │   ├── long_distance.ref
   │   └── work.ref
   ├── loyalty_ref
   │   ├── other.ref
   │   └── self.ref
   ├── money_ref
   │   └── money.ref
   ├── personality_ref
   │   ├── care.ref
   │   ├── care_adv.ref
   │   ├── fight.ref
   │   ├── trait.ref
   │   └── trait_adv.ref
   ├── sex_ref
   │   ├── both.ref
   │   ├── boyfriend.ref
   │   └── girlfriend.ref
   └── pingying_preprocessing_ref
       ├── dcard.ref
       ├── ig.ref
       ├── line.ref
       ├── pow.ref
       ├── ptt.ref
       └── sex.ref
```
## 環境設置
- 套件安裝
    - `pip3 install ArticutAPI`
## Loki啟用說明
1. 註冊並登入[卓騰語言科技AI](https://api.droidtown.co/login/)
2. 點選 `Loki` -> `開始啟用Loki` 進入Loki控制台
3. 輸入專案名稱並點選 `建立專案`，並依序建立**family、life_style ... sex、pingying_preprocessing**，共7個專案
4. 進入設立完成之專案**family**
5. 點擊 `選擇檔案` ->選擇 `.ref` 檔->點選 `讀取意圖` 依序匯入目錄**family_ref** 中所有的`.ref`檔案
6. 點選畫面左上角房子圖示，回到 Loki控制台，點選 `複製` 專案金鑰
7. 在目錄 **family** 底下創建檔案 `account.info` ，並輸入以下內容
```
{
    "username":"--填入Loki註冊信箱--",
    "api_key" :"--填入ArticutAPI金鑰--",
    "loki_key":"--填入專案金鑰--"
}
```
8. 對剩餘6個專案重複步驟4-7

## DiscordBot建置
1. 註冊並登入 Discord 帳號
2. 進入[Discord Developers](https://discord.com/developers/applications)
3. 點擊畫面右上方的 `New Application` ->填上 Bot 名稱-> 點擊 `create` 建立 Discord Bot
4. 點選右方欄位 SETTINGS 中的 `Bot` ->點選 `Add Bot`
5. 點選右方欄位 SETTINGS 中的 `OAuth2` ->點選 `URL Generator`
6. 於 SCOPES 欄位勾選「bot」
7. 於 BOT PERMISSIONS 欄位勾選「Send Messages」、「Embed Links」、「Attach Files」及「Read Message History」
8. 複製 GENERATED URL 到新分頁中貼上，選擇 Bot 欲加入之伺服器，即完成添加
9. 點選 SETTINGS 中的 `Bot` ->點選 `Reset Token`
10. 在最外層的目錄下（與`Discord_bot.py`同一層）創建檔案 `account.info`
11. 將 Token 貼至 `account.info` 中
```
{
    "discord_token":"--填入token--"
}
```
## 使用者互動說明
完成上述程序後，執行 `python3 Discord_bot.py` 即可開始與 Bot 互動<br><br>
<互動示例><br>

## 參考資料

## 作者
+ [Brian Ding](https://github.com/brian098091) 
+ [Chris Chou](https://github.com/ChrisLoading) 
+ [Emily Li](https://github.com/emilyli0521)
