import cv2


cap = cv2.VideoCapture(0)
cap.set(3,640) # 设置宽度参数代码3，宽度640
cap.set(4,480) #高度
cap.set(10,100) #亮度
faceCascade = cv2.CascadeClassifier('Resource/haarcascade_frontalface_default.xml')

while True:
    success, img = cap.read()
    cv2.imshow("Video",img)
    faces = faceCascade.detectMultiScale(img, 1.1, 4)  # 可修改参数

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow("Result", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break