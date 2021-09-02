import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3,640) # 设置宽度参数代码3，宽度640
cap.set(4,480) #高度
cap.set(10,100) #亮度

myColors = [[0,119,147,9,255,255],
            [107,0,88,114,255,184],
            [66,52,77,93,98,181]]#可以增加或减少颜色

myColorValues = [[0,0,255],
                 [255,0,0],
                 [0,255,0]]#BGR

myPoints = []#[x,y,colorID]



def findColor(img,myColors,myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y = getContours(mask)
        #cv2.circle(imgResult,(x,y),20,myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count +=1
    return newPoints
        #cv2.imshow(str(color[0]),mask)


def getContours(img):#获取轮廓
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #print(area)
        if area>500:#防止噪音
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)#显示轮廓
            peri = cv2.arcLength(cnt,True)#周长，True表示封闭
            approx = cv2.approxPolyDP(cnt,0.01*peri,True)
            #print(len(approx))
            #objCor = len(approx)
            x,y,w,h = cv2.boundingRect(approx)
    return x+w//2,y

def drawPaint(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgResult,(point[0],point[1]),10,myColorValues[point[2]],cv2.FILLED)



while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    imgResult = img.copy()
    newPoints = findColor(img,myColors,myColorValues)
    if len(newPoints)!=0:
        for new in newPoints:
            myPoints.append(new)
    if len(myPoints)!=0:
        drawPaint(myPoints,myColorValues)
    cv2.imshow("Video",imgResult)
    if cv2.waitKey(1) & 0xFF == ord('c'):
        myPoints = []
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break