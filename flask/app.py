from urllib import response
from flask import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import datetime
import csv

app = Flask(__name__)  

# id=""
# pwd=""
# 爬蟲抓回的資料
advance = []    # 免修
attendCourse = [] # 所有修過的課(不包含被當的)
system = "" # 系所名
passNum = 0 # 通過幾場通識講座
Epass = False   # 英文畢業門檻
user = ""   # 帳號
password = ""   # 密碼
driver = ""



# 分組們
# 按年分去抓
AllGeneral = dict()
AllGeneral_list = [] # 通識
SchoolCourse = [] # 校必修
CollegeCourse = [] # 院必修
SystemCourse = [] # 系必修
SystemChooseCourse = [] # 系次領域選修
systemProCourse = [] # 系選修
FreeCredit = [] # 自由選修
studyingCourse = [] # 修習中
studyingGeneralGroup = [] # 修習中通識



# -----------------------------


# 缺通識
missGeneral = []
# 需要八堂系次領域課程
needSystemChooseCourse = 8 #
# 需要系選修學分
needProCredit = 12 #
# 需要自由學分
needFreeCredit = 20    #
# 一個領域通識需要幾學分
result = 5
# 特殊領域通識需要幾學分
resultSpecial = 4
# 放解的地方
CombResult = []
# 已經找到最佳解
CombBest = False
# 目前距離最佳解的最接近距離
CombMax = result

General =  ["文學與藝術", "歷史哲學與文化", "法政與教育", "社經與管理", "工程與科技", "生命與科學", "東南亞", "綠概念", "在地實踐"]

SchoolCoursePlusStudy = []
CollegeCoursePlusStudy = []
SystemCoursePlusStudy = []
SystemChooseCoursePlusStudy = []
systemProCoursePlusStudy = []
FreeCreditPlusStudy = []
studyingGeneralGroupPlusStudy = []
studyingCoursePlusStudy = []

# 缺少的課程
missSchoolCourse = [] # 校必修
missCollegeCourse = [] # 院必修
missSystemCourse = [] # 系必修
missChooseCourse = [] # 系領域選修
missSpecialGeneral = []
needGeneralCredit = 0
needGeneralCreditsmall = 0
missGeneralCredit = []


missCourseCredit = 0
missSchoolCourseCredit = 0 # 校必修缺分
missCollegeCourseCredit = 0 # 院必修缺分
missSystemCourseCredit = 0 # 系必修缺分
needGeneralCredit = 0 # 通識缺分
GernalCreditPercent = -1 # 趴數
mustCreditPercent = -1
chooseCreditPercent = -1
FreeCreditPercent = -1



def English() :
    global driver, Epass
    # 英文畢業門檻
    driver.get("https://ccweb6.ncnu.edu.tw/student/aspmaker_student_english_qualifylist.php")
    time.sleep(2)

    try :
        Ep = driver.find_element(by=By.ID, value="el1_aspmaker_student_english_qualify_passed").text
        if (Ep == "Y" ) :
            Epass = True
            print("英文畢業門檻通過")
        else :
            print("英文畢業門檻還沒過")
    except :
        return

def System() :
    global system
    driver.get("https://ccweb6.ncnu.edu.tw/student/aspmaker_student_selected_viewlist.php?cmd=resetall")

    # 系所
    pageSource = driver.page_source
    head = pageSource.find("系所：")
    bottom = pageSource.find("部別：")
    time.sleep(1)
    system = pageSource[head+3 : bottom-1 ]
    print("系所 :", system)

def Course() :
    global attendCourse
    # 修課
    elementHalf1Class = driver.find_elements(by=By.CLASS_NAME, value='ew-table-row')
    elementHalf2Class = driver.find_elements(by=By.CLASS_NAME, value='ew-table-alt-row') 
    classLen = len(elementHalf1Class)+len(elementHalf2Class)
    for i in range(classLen) :
        scoreUrl = "el"+str(i+1)+"_aspmaker_student_selected_view_score"
        score = driver.find_element(by=By.ID, value=scoreUrl).text
        if (score == "") :
            scoreNum = float(-1)
        elif (score == "停修") :
            continue
        else :
            scoreNum = float(score)
        if (scoreNum >= 60 or scoreNum == -1) :
            strUrl = "el"+str(i+1)+"_aspmaker_student_selected_view_cname"
            creditUrl = "el"+str(i+1)+"_aspmaker_student_selected_view_credit"
            cidUrl = "el"+str(i+1)+"_aspmaker_student_selected_view_courseid"
            YearUrl = "el"+str(i+1)+"_aspmaker_student_selected_view_year"
            classname = driver.find_element(by=By.ID, value=strUrl).text
            credit = driver.find_element(by=By.ID, value=creditUrl).text
            cid = driver.find_element(by=By.ID, value=cidUrl).text
            year = driver.find_element(by=By.ID, value=YearUrl).text
            print("Class : ", classname, " credit : ", credit, "score : ", score, "year", year)
            attendCourse.append([cid, year, credit, classname, scoreNum])
    driver.get("https://ccweb6.ncnu.edu.tw/student/aspmaker_student_exempt_list_viewlist.php")
    elementHalf1Class = driver.find_elements(by=By.CLASS_NAME, value='ew-table-alt-row')
    elementHalf2Class = driver.find_elements(by=By.CLASS_NAME, value='ew-table-row')
    classLen = len(elementHalf1Class)+len(elementHalf2Class)
    print("抵免")
    for i in range(classLen) :
        cidUrl = "el"+str(i+1)+"_aspmaker_student_exempt_list_view_exempt_courseid"
        oldCidUrl = "el"+str(i+1)+"_aspmaker_student_exempt_list_view_internal_courseid"
        oldCnameUrl = "el"+str(i+1)+"_aspmaker_student_exempt_list_view_exempt_coursename"
        cnameUrl = "el"+str(i+1)+"_aspmaker_student_exempt_list_view_internal_coursename"
        Ocid = driver.find_element(by=By.ID, value=oldCidUrl).text
        oldCname = driver.find_element(by=By.ID, value=oldCnameUrl).text
        cname = driver.find_element(by=By.ID, value=cnameUrl).text
        cid = driver.find_element(by=By.ID, value=cidUrl).text
        print("oldCid : ", Ocid, "cid", cid, "oldCname : ", oldCname, "cname : ", cname)

def advanceCourse() :
    print("免修")
    driver.get("https://ccweb6.ncnu.edu.tw/student/aspmaker_student_waiver_exempt_list_viewlist.php")
    elementHalf1Class = driver.find_elements(by=By.CLASS_NAME, value='ew-table-alt-row')
    elementHalf2Class = driver.find_elements(by=By.CLASS_NAME, value='ew-table-row')

    classLen = len(elementHalf1Class)+len(elementHalf2Class)
    print("classLen", len(elementHalf1Class), len(elementHalf2Class))
    for i in range(classLen) :
        cidUrl = "el"+str(i+1)+"_aspmaker_student_waiver_exempt_list_view_waived_courseid"
        cnameUrl = "el"+str(i+1)+"_aspmaker_student_waiver_exempt_list_view_waived_coursename"
        cid = driver.find_element(by=By.ID, value=cidUrl).text
        classname = driver.find_element(by=By.ID, value=cnameUrl).text
        print("cid", cid, "Class : ", classname)
        advance.append([cid, classname])

def GSpeech() :
    global passNum
    driver.get("https://ccweb.ncnu.edu.tw/UploadLectureReport/login.asp")
    time.sleep(2)
    # 通識講座
    # driver.get("https://ccweb.ncnu.edu.tw/UploadLectureReport/literacy_student_attendlectureViewlist.asp")

    element = driver.find_element(by=By.ID, value="mi_literacy_student_attendlectureView")
    ActionChains(driver).click(element).perform()

    time.sleep(5)

    elementHalf1Pass = driver.find_elements(by=By.CLASS_NAME, value='ewTableRow')
    elementHalf2Pass = driver.find_elements(by=By.CLASS_NAME, value='ewTableAltRow')
    passLen = len(elementHalf1Pass)+len(elementHalf2Pass)

    for i in range(passLen) :
        passOrNotUrl = "el"+str(i+1)+"_literacy_student_attendlectureView_pass"
        passOrNot = driver.find_element(by=By.ID, value=passOrNotUrl).text
        if (passOrNot == "通過審核") :
            passNum = passNum + 1
    print(passNum)

def EasyCheck() :
    # 體育課同一學期修兩堂
    # print("att", attendCourse)
    global needFreeCredit
    Sameyear = 0
    i = 0
    while ( i < len(attendCourse)) :
        if (attendCourse[i][3].find("體育:") != -1) :
            print("attendCourse[i][3]", attendCourse[i][1])
            if (Sameyear == attendCourse[i][1]) :
                print("isSame")
                print(attendCourse[i][2])
                needFreeCredit = needFreeCredit - float(attendCourse[i][2])
                attendCourse.pop(i)
                i = i - 1
            Sameyear = attendCourse[i][1]
        i = i + 1

# 登入教務系統, 抓資料
def Login() :
    global driver
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    # driver = webdriver.Firefox(options=options)
    driver = webdriver.Firefox(executable_path='/usr/bin/geckodriver', options=options)
    driver.get("https://ccweb6.ncnu.edu.tw/student/login.php")   # 前往特定網址

    elementUser = driver.find_element(by=By.ID, value="username")
    elementUser.send_keys(user)

    elementPwd = driver.find_element(by=By.ID, value="password")
    elementPwd.send_keys(password)

    elementSubmit = driver.find_element(by=By.ID, value="btn-submit")
    ActionChains(driver).click(elementSubmit).perform()

    time.sleep(1)

    try:
        pageSelect = driver.find_element(by=By.CLASS_NAME, value="alert-danger")
        driver.close()
        return False
    except:
        English()
        System()
        Course()
        advanceCourse()
        GSpeech()
        EasyCheck()
        driver.close()

        return True

def AllIntoName() :
    GeneralintoName(studyingCourse)
    GeneralintoName(studyingGeneralGroup)
    GeneralintoName(AllGeneral_list)
    intoName(SchoolCourse) # 校必修
    intoName(CollegeCourse) # 院必修
    intoName(SystemCourse) # 系必修
    intoName(SystemChooseCourse) # 系次領域選修
    intoName(systemProCourse) # 系選修
    intoName(FreeCredit) # 自由選修
    intoName(studyingCourse) # 修習中

def intoName(data):
    name = []
    for i in range(len(data)) :
        name.append(data[i][3])
    return name

def GeneralintoName(data) :
    name = []
    for i in range(len(data)) :
        for j in range(len(data[i])) :
           name.append(data[i][j][3])
    return name

# 通識
# 這裡要找最佳解，如果要 5 學分而且有 3 2 的課就先選，或是 2 2 1 ，如果是 4 學分要先選 2 2 或 3 1 
# 但同時又要注意兩個都要各一
def checkGeneralCourse() :
    global AllGeneral, AllGeneral_list
    # 先按照分類分成不同的 list ， 各自的 list 再去找最佳解
    # G 人文-文學與藝術
    G_list = []
    # H 人文-歷史哲學與文化
    H_list = []
    # I 社會-法政與教育
    I_list = []
    # J 社會-社經與管理
    J_list = []
    # K 自然-工程與科技
    K_list = []
    # L 自然-生命與科學
    L_list = []
    # M 特色通識-東南亞
    M_list = []
    # N 特色通識-綠概念
    N_list = []
    # O 特色通識-在地實踐
    O_list = []
    All_list_Word = ["G", "H", "I", "J", "K", "L", "M", "N", "O"]
    AllGeneral_list = [G_list, H_list, I_list, J_list, K_list, L_list, M_list, N_list, O_list] 
    # print("AllGeneral", AllGeneral)
    # print("attendCourse", attendCourse)

    for i in range(len(attendCourse)) :
        if (attendCourse[i] != "0" and attendCourse[i][1] != '') :
            for j in range(len(AllGeneral[attendCourse[i][1]])) :
                if (AllGeneral[attendCourse[i][1]][j][2] == attendCourse[i][0]) :
                    for pos in range(len(All_list_Word)) :
                        if (All_list_Word[pos] == AllGeneral[attendCourse[i][1]][j][1]) :
                            AllGeneral_list[pos].append(attendCourse[i])
                            attendCourse[i] = "0"
                            break
                    break
    # print("AllGeneral_list", AllGeneral_list)

# 修課中
def studying() :
    global studyingCourse
    i = 0
    while (i < len(attendCourse)) :
        if (attendCourse[i][4] == -1) :
            studyingCourse.append(attendCourse)
            attendCourse.pop(i)
        else :
            i = i + 1
    # print("studyingCourse", studyingCourse)
    # FIX 之後要怎麼處理，要放回去的話要按照組別


# 校必修
def checkSchoolCourse() :
    global SchoolCourse
    # 這裡目前兩個體育沒有避免兩個同學期修
    # 學院國文(上)、(下)目前沒有區分
    needSchoolCourse =  ["英文(上)","英文(下)","英文二","大一體育(上)","大一體育(下：","服務學習(上)","服務學習(下)","學院國文","學院國文","體育:","體育:"]
    SchoolCourse = check(needSchoolCourse, 3)
    # print("SchoolCourse :", SchoolCourse)

# 院必修
def checkCollegeCourse() :
    global CollegeCourse
    # 管院系所
    # 資管的課 id 、跟其他院的課 id 不一樣，用課名
    needCollegeCourse = ["經濟學", "會計學及實習(一)", "管理學", "統計學", "程式設計(上)"]
    CollegeCourse = check(needCollegeCourse, 3)
    # print("CollegeCourse :", CollegeCourse)


# 系必修
def checkSystemCourse() :
    global SystemCourse
    needSystemCourseId = ["130065", "130014", "130008", "130021", "130030", "130032", "130027", "130039", "130041", "130044"]
    SystemCourse = check(needSystemCourseId, 0)
    # print("SystemCourse :", SystemCourse)

def check(NeedCourse, IdOrName) :
    data = []
    for i in range(len(NeedCourse)) :
        for j in range(len(attendCourse)) :
            if (IdOrName == 3) :
                if (attendCourse[j] != "0" and attendCourse[j][IdOrName].find(NeedCourse[i]) != -1) :
                    data.append(attendCourse[j])
                    attendCourse[j] = "0"
                    break
            elif (IdOrName == 0) :
                if (attendCourse[j] != "0" and attendCourse[j][IdOrName] == NeedCourse[i]) :
                    data.append(attendCourse[j])
                    attendCourse[j] = "0"
                    break
    return data

# 系次領域選修
def checkChooseCourse() :
    global SystemChooseCourse
    ChooseCourse = ["130024", "130031", "130034", "130040", "130077", "130042", "130028", "130022", "135091", "135120", "130058", "130033", "130050", "130061", "130019", "130073", "130038", "130071", "130070", "135109", "135086", "130089"]
    SystemChooseCourse = checkCredit(ChooseCourse)
    # print("SystemChooseCourse : ", SystemChooseCourse)

# 系選修
def checkProCourse() :
    global systemProCourse
    # 系次領域選修可以當作是系選修的，但一律以算系次領域選修優先
    # 一樣會有最佳化的問題
    global needProCredit
    ProCourse = ["951001","951002","130051","130056","130059","130068","130074","130075","130076","130078","130079","C20012","130082","130083","130087","130088","135114","135115","130053","130090","135001","210048","135029","135037","135042","135052","135055","135056","135067","135071","135075","135079","135086","135092","135094","135095","135098","135102","135103","135104","135105","135107","135108","135109","135111","120027","120081","120157","120165","120167","140020","140096","140102","145018","210128","210056","210060","210131","210115","210135","135117","135121","135118","135119","130085","130086","135125","135129","135130","135123","135131","135083","135132","135133","135135","135134","135136","130091","510001","510002","135137","130092","135099"]
    systemProCourse = checkCredit(ProCourse)
    # print("systemProCourse : ", systemProCourse)

# 系選修學分
def checkCredit(NeedCourse) :
    # 用課號
    data = []
    for i in range(len(NeedCourse)) :
        for j in range(len(attendCourse)) :
            if (attendCourse[j] != "0" and attendCourse[j][0] == NeedCourse[i]) :
                data.append(attendCourse[j])
                attendCourse[j] = "0"
    return data

# 自由選修
def checkFreeCredit() :
    global FreeCredit
    for i in range(len(attendCourse)) :
        if (attendCourse[i] != "0") :
            FreeCredit.append(attendCourse[i])
    # print("FreeCredit : ", FreeCredit)
# 讀入通識
# 用年去找讀入那一個年分的檔案(可以先看使用者是哪一年入學，然後看今年是哪一個學期)
def readAllGeneral(Account, ThisYear) :
    global AllGeneral
    Year = int(Account) // 1000000
    ThisYear = ThisYear - 1911 -1
    for i in range(ThisYear - Year + 1) :
        # 開啟 CSV 檔案
        for v in range(2) :
            data = []
            n = v + 1
            with open('./static/csv/' +  str(Year+i) + str(n) + '_general.csv', newline='',encoding="utf-8") as csvfile:
                # 讀取 CSV 檔案內容
                rows = csv.reader(csvfile)
                # 第一行的內容 : 英文畢業門檻、通識講座數量、系所
                # 抓修課程式碼的那邊，萬一沒有通過畢業門檻會抓不到資料
                for row in rows :
                    data.append(row)
            AllGeneral[str(Year+i) + str(n)] = data


def checkStudying() :
    global studyingCourse, studyingGeneralGroup
    # 把它整理成像是通識那樣
    # 放回去的時候比較方便
    studyingGroup = [SchoolCourse, CollegeCourse, SystemCourse, SystemChooseCourse, systemProCourse, FreeCredit]
    studyingCourse = [[], [], [], [], [], []]
    for i in range(len(studyingGroup)) :
        v = 0
        while ( v < len(studyingGroup[i])) :
            if (studyingGroup[i][v][4] == -1) :
                studyingCourse[i].append(studyingGroup[i][v])
                studyingGroup[i].pop(v)
                v = v - 1
                # 原本的資料裡面要刪掉
            v = v + 1
    # AllGeneral_list 通識要另外處理
    # ["G", "H", "I", "J", "K", "L", "M", "N", "O"]
    studyingGeneralGroup = [[], [], [], [], [], [], [], [], []]
    for i in range(9) :
        j = 0
        while ( j < len(AllGeneral_list[i])) :
            if (AllGeneral_list[i][j][4] == -1) :
                studyingGeneralGroup[i].append(AllGeneral_list[i][j])
                AllGeneral_list[i].pop(j)
                j = j - 1
            j = j + 1
    # print("studyingCourse", studyingCourse)
    # print("studyingGeneralGroup", studyingGeneralGroup)
def minigroup() :
    # 讀取今年年分
    ThisYear = datetime.datetime.now().date().year
    # 1 是技術 、 0 是管理
    # SystemChoose = int(input())
    # studying() # Fix 目前考慮都分組之後，再把資料挑出來，組別資訊留著
    readAllGeneral(user, ThisYear)
    checkSchoolCourse()
    checkGeneralCourse()
    # checkFreeCredit()

def group() :
    # 讀取今年年分
    ThisYear = datetime.datetime.now().date().year
    # 1 是技術 、 0 是管理
    # SystemChoose = int(input())
    # studying() # Fix 目前考慮都分組之後，再把資料挑出來，組別資訊留著
    readAllGeneral(user, ThisYear)
    checkSchoolCourse()
    checkCollegeCourse()
    checkSystemCourse()
    checkChooseCourse()
    checkProCourse()
    checkGeneralCourse()
    checkFreeCredit()
    checkStudying()

def GeneralRule(data) :
    # global CombBest, CombResult
    global missGeneralCredit, needGeneralCreditsmall, missSpecialGeneral, needGeneralCredit
    # CombBest = False
    # CombResult = []
    missGeneralCredit = []
    need3out2 = 0
    needGeneralCreditsmall = resultSpecial
    for i in range(6, 9) :
        if (len(data[i]) > 0) :
            need3out2 = need3out2 + 1
        else : 
            print("General[i]", General[i])
            missSpecialGeneral.append(General[i])
    if (need3out2 >= 2) :
        missSpecialGeneral = []
        ThreeComb(data[6], data[7], data[8], result)
        moveMore(data[6]+data[7]+data[8], resultSpecial)
    elif (need3out2 == 1) :
        print(missSpecialGeneral, "二選一")
        # 組合
        if (len(data[6]) > 0) :
            OnlyOneComb(data[6], resultSpecial, [])
            moveMore(data[6], resultSpecial)
        elif (len(data[7]) > 0) :
            OnlyOneComb(data[7], resultSpecial, [])
            moveMore(data[7], resultSpecial)
        else :
            OnlyOneComb(data[8], resultSpecial, [])
            moveMore(data[8], resultSpecial)
    missGeneralCredit.append(needGeneralCreditsmall)
    for i in range(3) :
        needGeneralCreditsmall = 0
        print(i)
        # 不缺領域
        if (len(data[i*2]) > 0 and len(data[i*2+1]) > 0) :
            # 組合
            twoComb(data[i*2], data[i*2+1], result)
            moveMore(data[i*2]+data[i*2+1], result)
        # 兩個領域都缺
        elif (len(data[i*2]) == 0 and len(data[i*2+1]) == 0) :
            missGeneral.append(General[i*2+1])
            missGeneral.append(General[i*2])
            needGeneralCreditsmall = result
        # 缺一領域
        else : # 二選一
            # 組合
            if (len(data[i*2]) > 0) :
                missGeneral.append(General[i*2])
                OnlyOneComb(data[i*2], result, [])
                #print("CombResult", CombResult)
                moveMore(data[i*2], result)
            else :
                missGeneral.append(General[i*2+1])
                OnlyOneComb(data[i*2+1], result, [])
                #print("CombResult", CombResult)
                moveMore(data[i*2+1], result)
        missGeneralCredit.append(needGeneralCreditsmall)
    print("missSpecialGeneral", missSpecialGeneral)
    print(missGeneral)
    print("missGeneralCredit", missGeneralCredit)
    needGeneralCredit = sum(missGeneralCredit)



def OnlyOneComb(data, result, ans) :
    global CombBest, CombMax, CombResult
    # 如果有最佳解了，終止
    if (CombBest == True) :
        return 
    if (result <= 0 or (len(ans) >= len(data) and len(ans) > 0)) :
        if (result == 0) :
            CombResult = ans
            CombBest = True
            return
        if (result < CombMax) :
            CombResult = ans
            CombMax = result
            return
    for i in range(len(data)) :
        result = result - float(data[i][2])
        OnlyOneComb(data[i+1:], result, ans + [data[i]])
        result = result + float(data[i][2])

def ThreeComb(dataA, dataB, dataC, result) :
    global CombBest, CombMax, CombResult
    CombResult = []
    CombBest = False
    CombMax = result
    if (len(dataA) == 0) :
        twoComb(dataB, dataC, result)
    elif (len(dataB) == 0) :
        twoComb(dataA, dataC, result)
    elif (len(dataC) == 0) :
        twoComb(dataA, dataB, result)
    else :
        for i in range(len(dataA)) :
            dataA[i].append("A")
        for i in range(len(dataB)) :
            dataB[i].append("B")
        for i in range(len(dataC)) :
            dataB[i].append("C")
        data = dataA + dataB + dataC
        CombThree(data, result, [])
        print("CombResult", CombResult)

def twoComb(dataA, dataB, result) :
    global CombBest, CombMax, CombResult
    CombResult = []
    CombBest = False
    CombMax = result
    for i in range(len(dataA)) :
        dataA[i].append("A")
    for i in range(len(dataB)) :
        dataB[i].append("B")
    data = dataA + dataB
    Comb(data, result, [])
    # print("CombResult", CombResult)

def Comb(data, result, ans) :
    # 如何加上flag
    global CombBest, CombMax, CombResult
    # 如果有最佳解了，終止
    if (CombBest == True) :
        return 
    if (result <= 0 or (len(ans) >= len(data) and len(ans) > 0)) :
        # print("ans", ans)
        if (checkGroup(ans, "A") and checkGroup(ans, "B")) :
            if (result == 0 ) :
                CombResult = ans
                CombBest = True
                return
            if (result < CombMax) :
                CombResult = ans
                CombMax = result
                return
    for i in range(len(data)) :
        result = result - float(data[i][2])
        Comb(data[i+1:], result, ans + [data[i]])
        result = result + float(data[i][2])

def CombThree(data, result, ans) :
    # 如何加上flag
    global CombBest, CombMax, CombResult
    # 如果有最佳解了，終止
    if (CombBest == True) :
        return 
    if (result <= 0 or (len(ans) >= len(data) and len(ans) > 0)) :
        if (checkGroup(ans, "A") and checkGroup(ans, "B") and checkGroup(ans, "C")) :
            if (result == 0 ) :
                CombResult = ans
                CombBest = True
                return
            if (result < CombMax) :
                CombResult = ans
                CombMax = result
                return
    for i in range(len(data)) :
        result = result - float(data[i][2])
        Comb(data[i+1:], result, ans + [data[i]])
        result = result + float(data[i][2])


def checkGroup(data, groupName) :
    for i in range(len(data)) :
        if (data[i][5] == groupName) :
            return True
    return False


def turnIntoName(missid, CourseId, CourseName) :
    data = []
    for i in range(len(missid)) :
        for j in range(len(CourseId)) :
            if (CourseId[j] == missid[i]) :
                data.append(CourseName[j])
    return data

def moveMore(data, result) :
    global needFreeCredit, needGeneralCreditsmall
    sum = 0
    needGeneralCreditsmall = 0
    # 學分剛好
    if (CombBest == True) :
        print("不缺學分")
        for i in range(len(data)) :
            needFreeCredit = needFreeCredit - float(data[i][2])
            # print("data", data)
            # print("needFreeCredit", needFreeCredit)
            for j in range(len(CombResult)) :
                if (CombResult[j] == data[i]) :
                    needFreeCredit = needFreeCredit + float(data[i][2])
    else :
        for v in range(len(CombResult)) :
            sum = sum + float(CombResult[v][2])
        # 學分不足
        if (sum < result) :
            print("缺", result - sum, "學分")
            needGeneralCreditsmall = result - sum
        # 學分超過
        else :
            for i in range(len(data)) :
                needFreeCredit = needFreeCredit - float(data[i][2])
                # print("data", data)
                # print("needFreeCredit", needFreeCredit)
                for j in range(len(CombResult)) :
                    if (CombResult[j] == data[i]) :
                        needFreeCredit = needFreeCredit + float(data[i][2])
    print("needFreeCredit_inGeneral", needFreeCredit)


def plus(data, Select, oldData) :
    # print(Select)
    # print("oldData", oldData)
    for pos in Select :
        pos = int(pos)
        data.append(oldData[pos])
    return data

def plusGeneral(data, Select, oldData) :
    print('select', Select)
    print("oldData", oldData)
    for pos in Select :
        selectNum = 0
        pos = int(pos)
        for i in range(len(oldData)) :
            for j in range(len(oldData[i])) :
                if (selectNum == pos) :
                    data[i].append(oldData[i][j])
                selectNum = selectNum + 1
    return data
def count(NeedCourse, attendCourse, IdOrName) :
    global missCourseCredit
    missCourse = []
    missCourseCredit = 0
    for i in range(len(attendCourse)) :
        for j in range(len(NeedCourse)) :
            if (IdOrName == 3) :
                # IdOrName : 課名是 3 、課號是 0
                # print(attendCourse[], NeedCourse[i])
                if (attendCourse[j][IdOrName].find(NeedCourse[i]) != -1) :
                    #print(missCourseCredit, attendCourse[j])
                    NeedCourse[i] = "0"
                    missCourseCredit = missCourseCredit - float(attendCourse[j][2])
                    break
            elif (IdOrName == 0) :
                if (attendCourse[j][IdOrName] == NeedCourse[i]) :
                    #print(attendCourse[j])
                    NeedCourse[i] = "0"
                    missCourseCredit = missCourseCredit - float(attendCourse[j][2])
                    # attendCourse[j] = []
                    break
    print("NeedCourse_INside", NeedCourse)
    for i in range(len(NeedCourse)) :
        if (NeedCourse[i] != "0") :
            missCourse.append(NeedCourse[i])
    print("missinCount", missCourseCredit)
    return missCourse

# 系次領域選修學分
def countSystemCredit(NeedCourse, attendCourse) :
    # 用課號
    global needSystemChooseCourse, needProCredit
    ProNum = 0
    for i in range(len(NeedCourse)) :
        for j in range(len(attendCourse)) :
            if (attendCourse[j][0] == NeedCourse[i]) :
                ProNum = ProNum + 1
                NeedCourse[i] = "0"
                if (needSystemChooseCourse > 0) :
                    needSystemChooseCourse = needSystemChooseCourse - 1
                else :
                    needProCredit = needProCredit - 3
    missProCourse = []
    if (needSystemChooseCourse > 0) :
        for i in range(len(NeedCourse)) :
            if (NeedCourse[i] != "0") :
                missProCourse.append(NeedCourse[i])
    if (len(attendCourse) > ProNum) :
        needProCredit = (needProCredit - 3) * (len(attendCourse) - ProNum)
    return missProCourse

# 系選修
def countProCourse(systemProCoursePlusStudy, systemProCourse_Select) :
    global needProCredit
    # 系次領域選修可以當作是系選修的，但一律以算系次領域選修優先
    systemProCoursePlusStudy = plus(systemProCoursePlusStudy, systemProCourse_Select, systemProCourse)
    countCredit(systemProCoursePlusStudy)
    print("needProCredit : " , needProCredit)
    print("needFreeCredit : ", needFreeCredit)

# 系選修學分
def countCredit(attendCourse) :
    # 用課號
    global needProCredit, needFreeCredit
    print("attendCourse", attendCourse)
    newlist = sorted(attendCourse, key=lambda d: d[2])
    print("newlist", newlist)
    while (needProCredit > 0 and len(newlist) > 0) :
        print(newlist)
        num = float(newlist.pop()[2])
        if (needProCredit >= num) :
            needProCredit = needProCredit - num
        else :
            needFreeCredit = needFreeCredit - num
    while (len(newlist) > 0) :
        needFreeCredit = needFreeCredit - float(newlist.pop()[2])

# 自由選修
def countFreeCredit(FreeCreditPlusStudy, FreeCredit_Select) :
    global needFreeCredit
    FreeCreditPlusStudy = plus(FreeCreditPlusStudy, FreeCredit_Select, FreeCredit)
    for i in range(len(FreeCreditPlusStudy)) :
        needFreeCredit = needFreeCredit - float(FreeCreditPlusStudy[i][2])
    print("final free credit : ", needFreeCredit)

# 系次領域選修
def countChooseCourse(SystemChooseCoursePlusStudy, SystemChooseCourse_Select, fieldSelect) :
    global missChooseCourse
    SystemChooseCoursePlusStudy = plus(SystemChooseCoursePlusStudy, SystemChooseCourse_Select, SystemChooseCourse)
    # 技術組課
    ChooseCourseTech = ["130024", "130031", "130034", "130040", "130077", "130042", "130028", "130022", "135091", "135120", "130073", "130070", "130089"]
    ChooseCourseTechName = ["資料結構與演算法(下)","軟體工程","系統程式 ","作業系統","網頁程式設計","離散數學","線性代數","計算機組織","資訊安全管理與技術","Linux 系統管理實務(一)","人因與人機介面","微積分及實習(下)","Android App 程式設計"]
    # 管理組課
    ChooseCourseManage = ["130058", "130033", "130050", "130061", "130019", "130028", "130073", "130038", "130071", "130070", "135109", "135086", "130089"]
    ChooseCourseManageName = ["財務管理","作業研究","生產與作業管理","行銷管理","組織行為","線性代數","人因與人機介面","決策支援系統","統計學及實習(下)","微積分及實習(下)","系統思考與系統動態學","創新事業導論","Android App 程式設計"]
    # 如果是技術組的 (選 8)
    if (fieldSelect == "1") :
        missid = countSystemCredit(ChooseCourseTech, SystemChooseCoursePlusStudy)
        missChooseCourse = turnIntoName(missid, ChooseCourseTech, ChooseCourseTechName)
    # 是管理組的
    else :
        missid = countSystemCredit(ChooseCourseManage, SystemChooseCoursePlusStudy)
        missChooseCourse = turnIntoName(missid, ChooseCourseManage, ChooseCourseManageName)
    print("needSystemChooseCourse : " , needSystemChooseCourse)
    print("SystemChooseCourseAdvice", missChooseCourse)


# 校必修
def countSchoolCourse(SchoolCoursePlusStudy, SchoolCourse_Select) :
    global missSchoolCourseCredit, missSchoolCourse
    needCredit = 12
    SchoolCoursePlusStudy = plus(SchoolCoursePlusStudy, SchoolCourse_Select, SchoolCourse)
    needSchoolCourse =  ["英文(上)","英文(下)","英文二","大一體育(上)","大一體育(下：","服務學習(上)","服務學習(下)","學院國文","學院國文","體育:","體育:"]
    missSchoolCourse = count(needSchoolCourse, SchoolCoursePlusStudy, 3)
    missSchoolCourseCredit = needCredit + missCourseCredit
    print("missSchoolCourseCredit", missSchoolCourseCredit)
    print("missSchoolCourse", missSchoolCourse)

# 院必修
def countCollegeCourse(CollegeCoursePlusStudy, CollegeCourse_Select) :
    global missCollegeCourseCredit, missCollegeCourse
    needCredit = 15
    CollegeCoursePlusStudy = plus(CollegeCoursePlusStudy, CollegeCourse_Select, CollegeCourse)
    # 如果是管院
    # 管院系所
    # 資管的課 id 、跟其他院的課 id 不一樣，但是如果用課名，有些需要兩段式檢查
    needCollegeCourse = ["經濟學", "會計學及實習(一)", "管理學", "統計學", "程式設計(上)"]
    missCollegeCourse = count(needCollegeCourse, CollegeCoursePlusStudy, 3)
    print("missCollegeCourse", missCollegeCourse)
    missCollegeCourseCredit = needCredit + missCourseCredit
    print("missCollegeCourseCredit", missCollegeCourseCredit)

# 系必修
def countSystemCourse(SystemCoursePlusStudy, SystemCourse_Select) :
    global missSystemCourseCredit, missSystemCourse
    needCredit = 30
    data = []
    SystemCoursePlusStudy = plus(SystemCoursePlusStudy, SystemCourse_Select, SystemCourse)
    needSystemCourseId = ["130065", "130014", "130008", "130021", "130030", "130032", "130027", "130039", "130041", "130044"]
    needSystemCourseName = ["微積分及實習(上)","程式設計(下)","計算機概論","資料結構與演算法(上)","管理資訊系統","資料庫管理系統","系統分析與設計","企業資訊通訊與網路","資訊管理專題與個案(上)","資訊管理專題與個案(下)"]
    missid = count(needSystemCourseId, SystemCoursePlusStudy, 0)
    missSystemCourse = turnIntoName(missid, needSystemCourseId, needSystemCourseName)
    missSystemCourseCredit = needCredit + missCourseCredit
    print("missSystemCourseCredit", missSystemCourseCredit)
    print("missSystemCourse", missSystemCourse)
    # return data

def countGeneralCourse(studyingGeneralGroupPlusStudy, AllGeneral_list_Select) :
    studyingGeneralGroupPlusStudy = plusGeneral(studyingGeneralGroupPlusStudy, AllGeneral_list_Select, AllGeneral_list)
    GeneralRule(studyingGeneralGroupPlusStudy)

def countStudying(studyingCourse_Select) :
    studyingCourseName = GeneralintoName(studyingCourse)
    print("studyingCourseName", studyingCourseName)
    studyingGroupPlusStudy = [SchoolCoursePlusStudy, CollegeCoursePlusStudy, SystemCoursePlusStudy, SystemChooseCoursePlusStudy, systemProCoursePlusStudy, FreeCreditPlusStudy]
    for i in studyingCourse_Select :
        i = int(i)
        for g in range(len(studyingCourse)) :
            for v in range(len(studyingCourse[g])) :
                if (studyingCourseName[i] == studyingCourse[g][v][3]) :
                    studyingGroupPlusStudy[g].append(studyingCourse[g][v])
    print("studyingGroupPlusStudy", studyingGroupPlusStudy)

def countStudyingGeneral(studyingGeneralGroup_Select) :
    global studyingGeneralGroupPlusStudy
    studyingGeneralCourseName = GeneralintoName(studyingGeneralGroup)
    studyingGeneralGroupPlusStudy = [[], [], [], [], [], [], [], [], []]
    print("here")
    for i in range(len(studyingGeneralGroup_Select)) :
        for g in range(len(studyingGeneralGroup)) :
            for v in range(len(studyingGeneralGroup[g])) :
                if (studyingGeneralCourseName[i] == studyingGeneralGroup[g][v][3]) :
                    studyingGeneralGroupPlusStudy[g].append(studyingGeneralGroup[g][v])
    # countGeneralCourse(studyingGeneralGroupPlusStudy, AllGeneral_list_Select)

def init():
    global FreeCredit, advance, attendCourse, system, passNum, Epass, user, password, driver
    global AllGeneral, AllGeneral_list, SchoolCourse, CollegeCourse, SystemCourse, SystemChooseCourse, systemProCourse, FreeCredit, studyingCourse
    # 爬蟲抓回的資料
    FreeCredit = 20 # 自由學分
    advance = []    # 免修
    attendCourse = [] # 所有修過的課(不包含被當的)
    system = "" # 系所名
    passNum = 0 # 通過幾場通識講座
    Epass = False   # 英文畢業門檻
    user = ""   # 帳號
    password = ""   # 密碼
    driver = ""


    # 分組們
    # 按年分去抓
    AllGeneral = dict()
    AllGeneral_list = [] # 通識
    SchoolCourse = [] # 校必修
    CollegeCourse = [] # 院必修
    SystemCourse = [] # 系必修
    SystemChooseCourse = [] # 系次領域選修
    systemProCourse = [] # 系選修
    FreeCredit = [] # 自由選修
    studyingCourse = [] # 修習中

def intoPicture() :
    # 通識
    global needProCredit, GernalCreditPercent, mustCreditPercent, chooseCreditPercent, FreeCreditPercent
    print("needGeneralCredit", needGeneralCredit)
    GernalCreditPercent = int(((19 - needGeneralCredit) / 19)*100)
    print("GernalCreditPercent", GernalCreditPercent)
    # 必修
    print(missSchoolCourseCredit, missCollegeCourseCredit, missSystemCourseCredit)
    mustCredit = missSchoolCourseCredit + missCollegeCourseCredit + missSystemCourseCredit
    print("mustCredit", mustCredit)
    mustCreditPercent = int(((12+15+30 - mustCredit) / (12+15+30))*100)
    # 系選跟專業選
    if needProCredit < 0 :
        needProCredit = 0
    print(needProCredit, needSystemChooseCourse)
    chooseCredit = needProCredit + (needSystemChooseCourse*3)
    print("chooseCredit", chooseCredit)
    chooseCreditPercent = int((( 24 + 12 - chooseCredit) / (24 + 12))*100)
    print("chooseCreditPercent", chooseCreditPercent)
    # 自由選
    print(needFreeCredit)
    FreeCreditPercent = int(((20 - needFreeCredit) / 20) * 100)
    print("FreeCreditPercent", FreeCreditPercent)

def init2():
    global missGeneral, needSystemChooseCourse, needProCredit, needFreeCredit, result, resultSpecial, CombResult, CombBest, CombMax
    global SchoolCoursePlusStudy, CollegeCoursePlusStudy, SystemCoursePlusStudy, SystemChooseCoursePlusStudy, systemProCoursePlusStudy, FreeCreditPlusStudy, studyingGeneralGroupPlusStudy, studyingCoursePlusStudy
    global missSchoolCourse, missCollegeCourse, missSystemCourse, missChooseCourse, missSpecialGeneral
    global needGeneralCredit, needGeneralCreditsmall, missGeneralCredit
    global missCourseCredit, missSchoolCourseCredit, missCollegeCourseCredit, missSystemCourseCredit, needGeneralCredit, GernalCreditPercent, mustCreditPercent, chooseCreditPercent, FreeCreditPercent


    missGeneral = []
    needSystemChooseCourse = 8
    needProCredit = 12
    needFreeCredit = 20

    # result = 5
    # print("user", user)
    if(int(user[0:3]) > 109) :
        result = 4
    else:
        result = 5

    resultSpecial = 4
    CombResult = []
    CombBest = False
    CombMax = result

    SchoolCoursePlusStudy = []
    CollegeCoursePlusStudy = []
    SystemCoursePlusStudy = []
    SystemChooseCoursePlusStudy = []
    systemProCoursePlusStudy = []
    FreeCreditPlusStudy = []
    studyingGeneralGroupPlusStudy = []
    studyingCoursePlusStudy = []

    # 缺少的課程
    missSchoolCourse = [] # 校必修
    missCollegeCourse = [] # 院必修
    missSystemCourse = [] # 系必修
    missChooseCourse = [] # 系領域選修
    missSpecialGeneral = [] # 特色通識(3選2)
    needGeneralCredit = 0
    needGeneralCreditsmall = 0
    missGeneralCredit = []

    missCourseCredit = 0
    missSchoolCourseCredit = 0 # 校必修缺分
    missCollegeCourseCredit = 0 # 院必修缺分
    missSystemCourseCredit = 0 # 系必修缺分
    needGeneralCredit = 0 # 通識缺分
    GernalCreditPercent = -1 # 趴數
    mustCreditPercent = -1
    chooseCreditPercent = -1
    FreeCreditPercent = -1


@app.route('/')  
def home():
    return render_template("home.html");  

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/checkLogin', methods = ["POST"])  
def validate():
    # global id, pwd
    # id = request.form['id']
    # pwd = request.form['pwd']
    # AllGeneral_list = ['戲劇欣賞', '與哲學家對話', '性別、教育、人文與社會', '政治哲學概論', '不動產投資與交易實務', '影像處理與設計-Photoshop', '圖解生命原理', '東南亞觀光與發展', '綠色能源']
    global user, password
    global AllGeneral_list, SchoolCourse, CollegeCourse, SystemCourse, SystemChooseCourse, systemProCourse, FreeCredit, studyingCourse, studyingGeneralGroup

    init()
    user = request.form['id']
    password = request.form['pwd']

    isSuccess = Login()
    # 如果帳號密碼正確，切換新頁面
    if isSuccess:
        print("system", system)
        if ( system == "資訊管理學系"):
            group()
        else :
            # group()
            print("minigroupFunc")

        # print("AllGeneral_list", AllGeneral_list)
        return render_template("check.html", studyingCourse = GeneralintoName(studyingCourse),
                                             studyingGeneralGroup = GeneralintoName(studyingGeneralGroup),
                                             AllGeneral_list = GeneralintoName(AllGeneral_list), 
                                             SchoolCourse = intoName(SchoolCourse), 
                                             CollegeCourse = intoName(CollegeCourse),
                                             SystemCourse = intoName(SystemCourse),
                                             SystemChooseCourse = intoName(SystemChooseCourse), 
                                             systemProCourse = intoName(systemProCourse), 
                                             FreeCredit = intoName(FreeCredit))
    else:
        error = "invalid password"
        return render_template("login.html", error=error)

@app.route('/check', methods = ["POST"])
def checkSelect():
    global AllGeneral_list, SchoolCourse, CollegeCourse, SystemCourse, SystemChooseCourse, systemProCourse, FreeCredit, studyingCourse, studyingGeneralGroup
    global missGeneral, needSystemChooseCourse, needProCredit, needFreeCredit, result, resultSpecial, CombResult, CombBest, CombMax
    global missSchoolCourse, missCollegeCourse, missSystemCourse


    init2()

    AllGeneral_list_Select = request.form.getlist('AllGeneral_list_Select')
    SchoolCourse_Select = request.form.getlist('SchoolCourse_Select')
    CollegeCourse_Select = request.form.getlist('CollegeCourse_Select')
    SystemCourse_Select = request.form.getlist('SystemCourse_Select')
    SystemChooseCourse_Select = request.form.getlist('SystemChooseCourse_Select')
    systemProCourse_Select = request.form.getlist('systemProCourse_Select')
    FreeCredit_Select = request.form.getlist('FreeCredit_Select')
    studyingGeneralGroup_Select = request.form.getlist('studyingGeneralGroup_Select')
    studyingCourse_Select = request.form.getlist('studyingCourse_Select')
    fieldSelect = request.form['fieldSelect']

    print("missSystemCourseAAAAAAA: ", missSystemCourse)


    countStudying(studyingCourse_Select)
    countSchoolCourse(SchoolCoursePlusStudy, SchoolCourse_Select)
    countCollegeCourse(CollegeCoursePlusStudy, CollegeCourse_Select)
    countSystemCourse(SystemCoursePlusStudy, SystemCourse_Select)
    countChooseCourse(SystemChooseCoursePlusStudy, SystemChooseCourse_Select, fieldSelect)
    countProCourse(systemProCoursePlusStudy, systemProCourse_Select)
    countFreeCredit(FreeCreditPlusStudy, FreeCredit_Select)
    countStudyingGeneral(studyingGeneralGroup_Select)
    countGeneralCourse(studyingGeneralGroupPlusStudy, AllGeneral_list_Select) #通識
    intoPicture()


    # percentage = [50, 41, 100, 12]
    percentage = [GernalCreditPercent, mustCreditPercent, chooseCreditPercent, FreeCreditPercent]
    return render_template("result.html", percentage = percentage, 
                                          missGeneral  = missGeneral, #
                                          missSpecialGeneral = missSpecialGeneral, #
                                          missGeneralCredit = missGeneralCredit,
                                          missSchoolCourse = missSchoolCourse,
                                          missCollegeCourse = missCollegeCourse,
                                          missSystemCourse = missSystemCourse,
                                          needSystemChooseCourse = needSystemChooseCourse,
                                          missChooseCourse = missChooseCourse,
                                          needProCredit = needProCredit,
                                          needFreeCredit = needFreeCredit,
                                          missGspeech = (6-passNum),
                                          Epass = Epass)


if __name__ == '__main__':
    # app.run(debug = True)
    # 啟動 server
    app.run(host='0.0.0.0', port=8000, threaded=True, debug=True)

