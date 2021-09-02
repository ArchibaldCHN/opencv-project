import cv2
import numpy as np


def to_multiple(arr, row, col):
    result = []
    for y in range(0, col):
        for x in range(0, row):
            if x == 0:
                result.append([])
            result[y].append(arr[x + y * row])
    return result



def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = 1
    for row in imgArray:
        if isinstance(row, list):
            cols = max(cols, len(row))
    print(rows, cols)
    if isinstance(imgArray[0], list):
        width = int(imgArray[0][0].shape[1] * scale)
        height = int(imgArray[0][0].shape[0] * scale)
    else:
        width = int(imgArray[0].shape[1] * scale)
        height = int(imgArray[0].shape[0] * scale)
    dim = (width, height)
    dim3 = (width, height, 3)
    max_col = int(1920 / width)
    new_array = []
    if cols == 1:
        if rows > max_col:
            new_rows = int(rows / max_col) + 1
            for i in range(0, new_rows * max_col):
                new_array.append(np.zeros(dim3, dtype=np.uint8))
            for i in range(rows):
                if len(imgArray[i].shape) == 2:
                    new_array[i] = cv2.resize(cv2.cvtColor(imgArray[i], cv2.COLOR_GRAY2BGR), dim)
                else:
                    new_array[i] = cv2.resize(imgArray[i], dim)
            new_array = to_multiple(new_array, max_col, new_rows)
            hor = []
            for r in new_array:
                hor.append(np.hstack(r))
            return np.vstack(hor)
        else:
            for img in imgArray:
                if len(img.shape) == 2:
                    new_array.append(cv2.resize(cv2.cvtColor(img, cv2.COLOR_GRAY2BGR), dim))
                else:
                    new_array.append(cv2.resize(img, dim))
            return np.hstack(new_array)
    else:
        for row in imgArray:
            if isinstance(row, list):
                for i in row:
                    if len(i.shape) == 2:
                        new_array.append(cv2.resize(cv2.cvtColor(i, cv2.COLOR_GRAY2BGR), dim))
                    else:
                        new_array.append(cv2.resize(i, dim))
                for i in range(len(row), cols):
                    new_array.append(np.zeros(dim3, dtype=np.uint8))
            else:
                new_array.append(cv2.resize(row, dim))
        new_array = to_multiple(new_array, cols, rows)
        hor = []
        for r in new_array:
            hor.append(np.hstack(r))
        return np.vstack(hor)


def getContours(img):#获取轮廓
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #print(area)
        if area>500:#防止噪音
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)#周长，True表示封闭
            approx = cv2.approxPolyDP(cnt,0.01*peri,True)
            #print(len(approx))
            objCor = len(approx)
            x,y,w,h = cv2.boundingRect(approx)

            if objCor ==3: objectType ="Tri"
            elif objCor ==4:
                aspRatio = w/float(h)
                if aspRatio >0.95 and aspRatio <1.05 :objectType = "Square"
                else:objectType ="Rect"
            elif objCor > 4:objectType = "Circle"
            else:objectType = "None"

            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(imgContour,objectType,
                        (x+(w//2)-20,y+(h//2)-2),cv2.FONT_HERSHEY_SIMPLEX,0.5,
                        (255,255,255),2)

img = cv2.imread('Resource/shapes.jpg')
imgContour = img.copy()
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
imgCanny = cv2.Canny(imgBlur,60,60)
getContours(imgCanny)

imgBlank = np.zeros_like(img)
imgStack = stackImages(0.8,([img,imgGray,imgBlur],
                            [imgCanny,imgContour,imgBlank]))

cv2.imshow("Stack",imgStack)
cv2.waitKey(0)