import requests
import os

def Save_Image_To_Dir(URL, Path, imgNumber):
    response = requests.get(URL)
    filePath = Path + str(imgNumber) + ".jpg"

    #print("save")
    #先判斷檔案是否已存在 未存在則進行檔案儲存
    if not (os.path.exists(filePath)):
        file = open(filePath, mode = "wb")
        file.write(response.content)
        file.close()

    #編號+-1
    imgNumber+=1
    return imgNumber