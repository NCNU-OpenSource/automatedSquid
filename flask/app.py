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

def English() :
    global driver, Epass
    # 英文畢業門檻
    driver.get("https://ccweb6.ncnu.edu.tw/student/aspmaker_student_english_qualifylist.php")
    time.sleep(1)

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
            print("Class : ", classname, " credit : ", credit, "score : ", score)
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
    time.sleep(1)
    # 通識講座
    # driver.get("https://ccweb.ncnu.edu.tw/UploadLectureReport/literacy_student_attendlectureViewlist.asp")

    element = driver.find_element(by=By.ID, value="mi_literacy_student_attendlectureView")
    ActionChains(driver).click(element).perform()

    time.sleep(3)

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
    print("att", attendCourse)
    global FreeCredit
    Sameyear = 0
    i = 0
    while ( i < len(attendCourse)) :
        if (attendCourse[i][3].find("體育:") != -1) :
            if (Sameyear == attendCourse[i][1]) :
                FreeCredit = FreeCredit - float(attendCourse[i][2])
                attendCourse.pop(i)
                i = i - 1
            else :
                Sameyear = attendCourse[i][1]
        i = i + 1

# 登入教務系統, 抓資料
def Login() :
    global driver
    driver = webdriver.Firefox()# options=opts
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
    for i in range(len(attendCourse)) :
        if (attendCourse[i] != "0") :
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
            elif (IdOrName == 0) :
                if (attendCourse[j] != "0" and attendCourse[j][IdOrName] == NeedCourse[i]) :
                    data.append(attendCourse[j])
                    attendCourse[j] = "0"
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
    # AllIntoName()

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
    init()
    user = request.form['id']
    password = request.form['pwd']

    isSuccess = Login()
    
    # 如果帳號密碼正確，切換新頁面
    if isSuccess:
        group()
        return render_template("check.html", AllGeneral_list=GeneralintoName(AllGeneral_list), 
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
    print(request.form.getlist('AllGeneral_list_Select'))
    # print(request.form.getlist('AllGeneral_list_Select'))
    return ("ok")

if __name__ == '__main__':
    app.run(debug = True)