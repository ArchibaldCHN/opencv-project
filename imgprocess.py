import cv2
import numpy as np

def empty(a):
    pass


path = 'Resource/zhengjianzhao.jpg'
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars",640,240)
cv2.createTrackbar("H_min","TrackBars",1,179,empty)
cv2.createTrackbar("H_max","TrackBars",179,179,empty)
cv2.createTrackbar("S_min","TrackBars",0,255,empty)
cv2.createTrackbar("S_max","TrackBars",255,255,empty)
cv2.createTrackbar("V_min","TrackBars",0,255,empty)
cv2.createTrackbar("V_max","TrackBars",255,255,empty)

while True:
    img = cv2.imread(path)
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("H_min","TrackBars")
    h_max = cv2.getTrackbarPos("H_max","TrackBars")
    s_min = cv2.getTrackbarPos("S_min","TrackBars")
    s_max = cv2.getTrackbarPos("S_max","TrackBars")
    v_min = cv2.getTrackbarPos("V_min","TrackBars")
    v_max = cv2.getTrackbarPos("V_max","TrackBars")
    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imgHSV,lower,upper)
    imgResult = cv2.bitwise_and(img,img,mask=mask)
    cv2.imshow("Original",img)
    cv2.imshow("HSV",imgHSV)
    cv2.imshow("Mask",mask)
    cv2.imshow("imgResult",imgResult)
    cv2.waitKey(1)