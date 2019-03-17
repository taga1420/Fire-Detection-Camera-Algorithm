import algorithmFunctions
import time
import numpy as np
import cv2

# MAIN #

print('Camera Initialize')
file = open('Temp_Info.txt', 'w')
file.writelines('Coordinates      Max_T(ºC)      Min_T(ºC)               Time              Area(pixels)\n')
file.close()
while 1:
    print('teste')
    img = algorithmFunctions.captureImage()
    cv2.imwrite('0.png', img)

    temperatura_max, temperatura_min, minVal, maxVal, minLoc, maxLoc = algorithmFunctions.temperatureInformation(img)
    interval = (maxVal * (temperatura_max - 5)) / temperatura_max  # 5graus de diferença
    spot = img.copy()
    spot[np.where((np.all(spot >= [interval, interval, interval], axis=-1)))] = [0, 255, 255]
    cv2.imwrite('1.png', spot)

    # load the image, convert it to grayscale, blur it slightly,
    # and threshold it
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, interval, 255, cv2.THRESH_BINARY)[1]
    #cv2.imwrite('2.png', thresh)

    # find contours in the thresholded image
    im, cnt, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #detecttedContour = cv2.drawContours(im, cnt, -1, (0, 255, 0), 2)
    #ipCamera.showImage(detecttedContour)
    algorithmFunctions.showImage(im)
    cnts = cnt[0]
    M = cv2.moments(cnts)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    area = cv2.contourArea(cnt[-1])
    print(area)




    algorithmFunctions.showImage(img)
    algorithmFunctions.saveImage(img)


    if temperatura_max >= 40.0:
        print('guardou')
        draw, contours = algorithmFunctions.detectContour(img)
        algorithmFunctions.saveImage(draw)
        algorithmFunctions.saveInformation(img, contours)

    time.sleep(5)
    continue





img = algorithmFunctions.captureImage()
cv2.imwrite('0.png', img)

temperatura_max, temperatura_min, minVal, maxVal, minLoc, maxLoc = algorithmFunctions.temperatureInformation(img)
interval = (maxVal * (temperatura_max - 3)) / temperatura_max  # 5graus de diferença
spot = img.copy()
spot[np.where((np.all(spot >= [interval, interval, interval], axis=-1)))] = [0, 255, 255]
cv2.imwrite('1.png', spot)

# load the image, convert it to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, interval, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite('2.png', thresh)

def find_if_close(cnt1,cnt2):
    row1,row2 = cnt1.shape[0],cnt2.shape[0]
    for i in range(row1):
        for j in range(row2):
            dist = np.linalg.norm(cnt1[i]-cnt2[j])
            if abs(dist) < 50 :
                return True
            elif i==row1-1 and j==row2-1:
                return False

_, contours,hier = cv2.findContours(thresh,cv2.RETR_EXTERNAL,2)

LENGTH = len(contours)
status = np.zeros((LENGTH,1))

for i,cnt1 in enumerate(contours):
    x = i
    if i != LENGTH-1:
        for j,cnt2 in enumerate(contours[i+1:]):
            x = x+1
            dist = find_if_close(cnt1,cnt2)
            if dist == True:
                val = min(status[i],status[x])
                status[x] = status[i] = val
            else:
                if status[x]==status[i]:
                    status[x] = i+1

unified = []
maximum = int(status.max())+1
for i in range(maximum):
    pos = np.where(status==i)[0]
    if pos.size != 0:
        cont = np.vstack(contours[i] for i in pos)
        hull = cv2.convexHull(cont)
        unified.append(hull)

cv2.drawContours(img,unified,-1,(0,255,0),2)
cv2.drawContours(thresh,unified,-1,255,-1)

