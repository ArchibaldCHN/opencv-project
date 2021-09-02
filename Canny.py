import cv2
import numpy as np

path = 'Resource/zhengjianzhao.jpg'
img = cv2.imread(path)
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray,(7,7),2)
imgCanny = cv2.Canny(img,300,300)
hstack = np.hstack((imgGray,imgBlur,imgCanny))
cv2.imshow("window",hstack)
cv2.waitKey(0)