import cv2
import time
import matplotlib.pyplot as plt
import requests
import numpy as np

# SAVE IMAGE
def saveImage(img, directory, kind):
    now = (time.strftime(time.ctime())).replace(":", "_")
    file = '%s/%s.png' % (directory, kind)
    cv2.imwrite(file, img)


# CAPTURE IMAGE
def captureImage():
    vcap = cv2.VideoCapture('rtsp://192.168.0.50/PSIA/Streaming/channels/1')
    ret, img = vcap.read()
    return img


# SHOW IMAGE#
def showImage(img):
    plt.imshow(img)
    plt.show()


# TEMPERATURE INFORMATION#
def temperatureInformation(img):
    content = requests.get('http://192.168.0.50/cgi-bin/httpapi/thermal.cgi?svc=tempAdvInfo&action=gets')
    index_temperatura_max = content.text.rindex('max_temp_value') #content vem em texto corrido. Aqui encontra-se o
    index_temperatura_min = content.text.rindex('min_temp_value') #indice para retirar valores de temperatura
    temperatura_max = float(content.text[index_temperatura_max + 15:index_temperatura_max + 19])
    temperatura_min = float(content.text[index_temperatura_min + 15:index_temperatura_min + 19])
    # coord = np.unravel_index(np.real(img).argmax(), np.real(img).shape) antigo metodo para detetar coordenadas
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(imgray)
    return temperatura_max, temperatura_min, minVal, maxVal, minLoc, maxLoc


def saveInformation(image, directory, area, cX, cY, max_T, min_T):
    file = open('%s/Temp_Info.txt' % directory, 'a')
    now = time.ctime()
    area = str(area)
    file.writelines(
        [image,'     ',str([cX, cY]), '       ', str(max_T), '           ', str(min_T), '        ', now, '       ', area, '\n'])
    file.close()


# DETECT CONTOUR #antigo metodo para calcular a area (ainda nao se sabe qual é o melhor)
def detectContour(img):
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 200, 255, cv2.THRESH_BINARY)
    _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detecttedContour = cv2.drawContours(imgray, contours, -1, (0, 255, 0), 2)
    return detecttedContour, contours


# DISTANCE FORMULA BETWEEN TWO POINTS
def distance(x1, x2, y1, y2):
    r = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return r


# CONVERT TO BINARY
def binaryImage(img, interval):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, interval, 255, cv2.THRESH_BINARY)[1]
    return thresh


# CENTER OF MASS #
def centerOfMass(thresh):
    _, contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > x_area:
            x_area = area
            best_cnt = cnt

    if len(cnt) > 0:  # In some cases no coutours are detected so best_cnt is not set.
        M = cv2.moments(best_cnt)
        cX, cY = int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])

    else:
        cX, cY = 0, 0
        print('divisao por zero')

    return cX, cY, best_cnt, x_area

# FIND CLOSE CONTOURS
def find_if_close(cnt1,cnt2):
    row1,row2 = cnt1.shape[0],cnt2.shape[0]
    for i in range(row1):
        for j in range(row2):
            dist = np.linalg.norm(cnt1[i]-cnt2[j])
            if abs(dist) < 50 :
                return True
            elif i==row1-1 and j==row2-1:
                return False