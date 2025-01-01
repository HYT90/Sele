#cli指令 py 檔名.py
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import time as timer

import SaveImage
#os建立資料夾folder
import os

#讀取頁面失敗時重新載入
def Refresh(method):
    while(True):
        try:
            WebDriverWait(driver, 5).until(
                method
            )
            break
        except:
            print('重新載入')
            driver.refresh()

#由於eHentai頁面可能會有閱覽警告 所以若會進入警告頁面選取不要再警告我, 沒有則取消這裡
def WithWarning(w, wnacg, WarningTrigger):
    print("檢查WARNING")
    if wnacg: return
    if(w and WarningTrigger):
        warntext = "Never Warn Me Again"
        Refresh(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, warntext)))
        neverwarn = driver.find_element(By.PARTIAL_LINK_TEXT, warntext)
        neverwarn.click()
    
    #進入圖片頁面 等待圖片載入完成
    Refresh(EC.presence_of_element_located((By.ID, "gdt")))

    #找到第一張圖進入放大
    imgpage = driver.find_element(By.XPATH, "//div[@id='gdt']//div[1]/a")
    imgpage.click()
    Refresh(EC.presence_of_element_located((By.XPATH, "//img[@id='img']")))
    return False


#一頁一頁讀存取放大圖片
def ImagesSaveLoop(driver, NewFolderPath, firstPage=""):
    #取得圖片src requests.get(src) 儲存response的資料(圖片)
    #loop 直到載完最後一頁
    imgNumber = 0
    thispage = ""
    while True:
        if not (wnacg):
            #For E-hentai.org
            imgsrc = driver.find_element(By.ID, "img").get_attribute("src")
            nextpage = driver.find_element(By.XPATH, '//div[@id="i3"]/a')
        else:
            #For wnacg.com
            imgsrc = driver.find_element(By.ID, "picarea").get_attribute("src")
            nextpage = driver.find_element(By.XPATH, '//span[@id="imgarea"]/a')        
        
        imgNumber = SaveImage.Save_Image_To_Dir(imgsrc, NewFolderPath, imgNumber)
        
        
        
        lastonecheck = nextpage.get_attribute("href")
        if not (thispage == lastonecheck or firstPage == lastonecheck):
            thispage = lastonecheck
            #不執行 a標籤 .click() 是因為WebDriverWait會誤判最後一頁 導致最後一頁同頁面資料重複下載
            #所以直接用 driver.get(href) 開啟頁面
            driver.get(lastonecheck)

            if not (wnacg):
                #E-hentai
                print("e-hentai讀取中")
                Refresh(EC.presence_of_element_located((By.XPATH, "//img[@id='img']")))
            else:
                #Wnacg
                print("wnacg讀取中")
                Refresh(EC.presence_of_element_located((By.XPATH, "//img[@id='picarea']")))
        else:
            break


###chrome瀏覽器的版本必須與driver一致 version of explorer and explorerdriver must be identical(consistent)
#最新版本 119.0.6045.160 (正式版本) (64 位元)
#explorerdriver 前往selenium網站下載: https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/
#path = "D:\PyProjects\chromedriver_win32\chromedriver.exe"
###select your explorer diver with the path of driver
#service = Service(executable_path="D:\PyProjects\IEDriverServer.exe")
service = Service(ChromeDriverManager().install()) ### 安裝路徑為 C:\Users\USER\.wdm\drivers\chromedriver\win64\127.0.6533.88
options = Options()
#options.page_load_strategy = 'normal'
#options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(1)
#搜尋關鍵字
keywords = ""
#存放路徑
NewFolderPath = 'E:\\7788\\無作品名\\'
while(input('是否新增資料夾?(y/n)') == 'y'):
    folderName = input('請輸入資料夾名稱')
    if(input('資料夾名稱是否為' + folderName + '?(y/n)') == 'y'):
        NewFolderPath = 'E:\\7788\\' + folderName + '\\'
        break

#檢查資料夾是否存在 如果儲存資料夾不存在 就建立新儲存資料夾
if not os.path.exists(NewFolderPath):
    os.makedirs(NewFolderPath)

#是否是wnacg?
wnacg = True
if(input('是否是wnacg?(y/n)') == 'n'):
    wnacg = False

#e-hentai的閱覽警告
#warning = False
#if(input('是否有警告頁面?(y/n)') == 'y'):
    #warning = True

#是否已開啟警告, 一旦開啟並關閉後改為False, 避免後續作品頁面會等待警告頁面
WarningTrigger = True

Start = True

#待存取的網址 e-hentai為作品頁面 wnacg為第一頁URL
arr = [
    ["", False],
]
#上次的斷點
checkpoint = False

if(Start):
    for n in range(0, len(arr)):
        tmp = 1
        newPath = NewFolderPath+"第"+str(n+tmp)+"本\\"
        while os.path.exists(newPath):
            tmp = tmp+1
            newPath = NewFolderPath+"第"+str(n+tmp)+"本\\"
        if(checkpoint):
            newPath = NewFolderPath+"第"+str(n+tmp-1)+"本\\"
            checkpoint = not checkpoint
        else:
            os.makedirs(newPath)
            
        print("開始載入網頁")
        driver.get(arr[n][0])
        print("載入網頁")
        #e-hentai警告
        warning = WithWarning(arr[n][1], wnacg, WarningTrigger)
        if(arr[n][1]):
            WarningTrigger=False

        print("開始")
        if not (wnacg):
            ImagesSaveLoop(driver, newPath)
        else:
            #Wnacg用, 需要給予第一頁URL
            ImagesSaveLoop(driver, newPath, arr[n][0])
    print("已下載完成")    
    driver.quit()

################################################################################

# #let driver gets the url
# #url = "https://e-hentai.org/"
# driver.get("https://e-hentai.org")
# Refresh(EC.presence_of_element_located((By.CLASS_NAME, "itg")))

# ###以條件(By [name, id, class...])找出搜尋欄位 並清空 輸入關鍵字 確認搜尋
# search = driver.find_element(By.NAME, "f_search")
# search.clear()
# search.send_keys(keywords)
# #search.send_keys(Keys.RETURN)
# search.submit()


# driver.quit()

# #拿取要訪問的頁面url 需要宣告一個container來儲存
# all_need_url = []
# #找出所有進入頁面的a標籤(anchor)
# elements = driver.find_elements(By.CLASS_NAME, "gl3c")
# for n in range(len(elements)):
#     anchor = elements[(len(elements)-1) - n].find_element(By.TAG_NAME, "a").get_attribute("href")
#     #把a標籤href存入container
#     all_need_url.append(anchor)

# #從頁面url container依序訪問
# for n in range(0, len(all_need_url)):
#     # if(n==1):
#     #     continue
#     #driver.get(all_need_url[(len(all_need_url)-1) - n])
#     driver.get(all_need_url[n])

#     warning = WithWarning(warning)
    
#     ImagesSaveLoop(driver, imgNumber, NewFolderPath)

# driver.quit()