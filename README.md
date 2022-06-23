# 自動化魷魚

## Concept Development 理念
大學生必須達到最低畢業學分才可以畢業，但本系修課有許多因素要考量，不只新生看得一頭霧水，舊生也需要花上一些時間計算。
在學長姊建議下決定來做一個可以自動幫系上同學算學分的系統，功能計算還需要多少學分達到畢業門檻、視覺化其修課情形，還可以順便省下幫魷魚買蘇滑口口的工資 ｡:.ﾟヽ(*´∀`)ﾉﾟ.:｡ 


## Implementation Resources 設備資源
- 一台 Unbuntu 20.04 server

## Existing Library/Software
- 爬蟲： Selenium
- 架網站：Python Flask
- 網頁前端框架：Bootstrap
- 部屬網站：Docker

## Implementation Process 實作過程
1. 收集歷年資料
2. 寫爬蟲程式爬使用者成績資料
3. 寫學分判斷規則
4. 寫前端網頁
5. 前後端整合
6. 佈署
7. 使用

## Installation 安裝
- 安裝 [Docker Engine](https://docs.docker.com/engine/install/ubuntu/)
    - `sudo apt-get update`
    - `sudo apt-get install \
        ca-certificates \
        curl \
        gnupg \
        lsb-release`
    - `curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg`
    - `echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`
    - `sudo apt-get update`
    - `sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin`
    - `apt-cache madison docker-ce`
    - `sudo apt-get install docker-ce=<VERSION_STRING> docker-ce-cli=<VERSION_STRING> containerd.io docker-compose-plugin`
- 安裝 [Docker CLI](https://docs.docker.com/compose/install/compose-plugin/#installing-compose-on-linux-systems)
	- `sudo apt-get update`
	- `sudo apt-get install docker-compose-plugin`
	- `apt-cache madison docker-compose-plugin`
	- `sudo apt-get install docker-compose-plugin=<VERSION_STRING>`
    - `docker compose version`
- 下載 GitHub Repo
    - `git clone https://github.com/miga-666/automatedSquid`
- 用 docker compose 啟動應用程式
    - `cd automatedSquid/flask`
    - `sudo docker compose build`
    - `sudo docker compose up`
- 結果畫面
      ![image](https://github.com/NCNU-OpenSource/automatedSquid/blob/main/MainPage.jpg)
- [實作影片](https://www.youtube.com/watch?v=CYOCT4PtsxY)

## Job Assignment 工作分配
- 前端 : 采禎
- 後端 : 婷誼
- 整合、文件資料 : 采禎、婷誼


## References 文獻資料
- Selenium 相關
  - [不開啟視窗](https://vimsky.com/zh-tw/examples/detail/python-method-selenium.webdriver.FirefoxOptions.html)
- Docker 相關
    - [安裝 Docker Engine](https://docs.docker.com/engine/install/ubuntu/)
    - [安裝 Docker CLI](https://docs.docker.com/compose/install/compose-plugin/#installing-compose-on-linux-systems)
## 遇到的困難
1. Selenium 無法在 server 版上執行，因為需要跳視窗 
  :point_right: 把 Selenium 改成不開視窗的程式碼 
2. 學校校務系統有時候會掛掉 
  :point_right: 等它恢復
3. 校務系統中的修業規則資料沒有更新，抓系辦上的 PDF 檔，轉換成 csv 檔，內容會跑掉，無法抓到需要的修業規則 
  :point_right: 手寫 list 
4. 將網站部屬到虛擬機時（ubuntu server 版）安裝 WebDriver 時，虛擬機會從文字介面變成奇怪畫面
  :point_right: 架在 docker 中 

## 感謝名單
- 題目發想
  - [漢偉](https://github.com/UncleHanWei)、蔣媽、[柏偉](https://github.com/PengLaiRenOu) 
- 測試小天使
  - [琪樺](https://github.com/ChiHua0918)、亮亮、蔣媽
