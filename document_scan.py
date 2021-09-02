import cv2
import numpy as np


widthImg,heightImg = 480, 640

cap = cv2.VideoCapture(0)
cap.set(3,640) # 设置宽度参数代码3，宽度640
cap.set(4,480) #高度
cap.set(10,150) #亮度

def prePro(img):
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
    imgCanny = cv2.Canny(imgBlur,200,200)
    kernel = np.ones((5,5))
    imgDial = cv2.dilate(imgCanny,kernel,iterations=2)
    imgThres = cv2.erode(imgDial,kernel,iterations=1)
    return imgThres


def getContours(img):#获取轮廓
    biggest = np.array([])
    maxArea = 0
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #print(area)
        if area>5000:#防止噪音
            # cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)#周长，True表示封闭
            approx = cv2.approxPolyDP(cnt,0.01*peri,True)
            if len(approx) == 4:
                cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            if area > maxArea and len(approx) == 4:
                biggest = approx#四个端点
                maxArea = area
            # #print(len(approx))
            # objCor = len(approx)
            # x,y,w,h = cv2.boundingRect(approx)
    cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 20)
    return biggest



def reorder(myPoints):
    myPoints = myPoints.reshape((4,2))
    myPointsNew = np.zeros((4,1,2),np.int32)
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints,axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew




def getWarp(img,biggest):
    biggest = reorder(biggest)
    pts1 = np.float32(biggest)  # 原始图像四个端点坐标
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
    #imgOutput = imgOutput[20:imgOutput.shape[0]-20,20:imgOutput.shape[1]-20]#边界处切割20像素，可删除

    return imgOutput


while True:
    success, img = cap.read()
    imgContour = img.copy()
    imgThres = prePro(img)
    biggest = getContours(imgThres)
    cv2.imshow("original",img)
    if biggest.size !=0:
        imgWarped = getWarp(img, biggest)
        cv2.imshow("Result",imgWarped)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break