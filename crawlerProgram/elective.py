from dbm.ndbm import library
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import csv

driver = webdriver.Firefox()

# 前往課程查詢網址
driver.get("https://ccweb6.ncnu.edu.tw/student/ncnu_coremin_schoolrequire_opened_detail_viewlist.php?cmd=resetall")


# 填入學年度 (最新一年)
yearSelect = driver.find_element(by=By.ID, value="x__51655B785E74")
Select(yearSelect).select_by_index(1)
year = int(yearSelect.text.split('\n')[1]) # 最新資料的年份
time.sleep(0.5)

categorySelect = driver.find_element(by=By.ID, value="x__68385FC3985E5225")
Select(categorySelect).select_by_value("0 共同選修(89始)")

# 開課學期
# 總共最近 5 學年, 上下 2 學期
semesters = []
for i in range(4, -1, -1):
    for j in range(2):
        # print(str(year-i) + str(j+1))
        semesters.append(str(year-i) + str(j+1))


# 依序填入開課學期
for seme in semesters:
    print(seme)
    library = dict()    # library: 儲存通識課程資料, 每年重置

    semesterInput = driver.find_element(by=By.ID, value="x__958B8AB25B78671F")
    semesterInput.clear()
    semesterInput.send_keys(seme)

    # 搜尋
    submitButton = driver.find_element(by=By.ID, value="btn-submit")
    submitButton.click()
    time.sleep(0.5)

    # 如果有多頁, 先選 "全部顯示"
    try:
        pageSelect = driver.find_element(by=By.NAME, value="recperpage")
        Select(pageSelect).select_by_value("ALL")
        print("", end='')
    except:
        print("", end='')

    # 抓下所有搜尋結果
    # 計算總共有幾列資料
    data = driver.find_elements(by=By.CLASS_NAME, value='ew-table-row')
    dataTmp = driver.find_elements(by=By.CLASS_NAME, value='ew-table-alt-row')
    # 將 data 和 dataTmp 合成 data
    for i in range(len(dataTmp)):
        data.append(dataTmp[i])

    # 將 data 中的資訊重新編排, 寫入 library
    for i in range(len(data)):
        # ['檢視\n110', 'G', '人文-文學與藝術(105始)', '1061', '460024', '0', 
        # '設計基礎', '李', '2bcd', '人204-1', '3.00', '0.00', '21', '999.00']
        tmp = data[i].text.split(' ')
        semeInfo = tmp[3]
        cateInfo = tmp[1]
        numInfo = tmp[4]
        nameInfo = tmp[6]
        credInfo = tmp[10]
        library[nameInfo] = [semeInfo, cateInfo, numInfo, credInfo]

    # 儲存成 csv
    with open("./electiveFiles/" + seme + "_elective.csv", "w", newline='') as file:
        # 以 ',' 分隔欄位，建立 CSV 檔寫入器
        writer = csv.writer(file, delimiter=',')
        writer.writerow(["semester", "category", "number", "name", "credit"])
        for name in library.keys():
            writer.writerow([library[name][0], library[name][1], library[name][2], name, library[name][3]])
    print("total: ", len(library))
    # 繼續抓下學期資料 ...


time.sleep(2)
# 關閉瀏覽器視窗
driver.close()


