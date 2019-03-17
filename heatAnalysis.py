import time
import datetime
import algorithmFunctions
import numpy as np
import cv2
import os

global percentage  # intervalo de temperatura a detetar



def heatAnalysis():
    print('Analysis Initialize')

    # criação de pasta para guardar analise de 60s

    go = datetime.datetime.now()
    now = (time.strftime(time.ctime())).replace(":", "_")
    file_path = ("%s/%s/%s/%s/" % (go.year, go.month, go.day, now))
    directory = os.path.dirname(file_path)

    if not os.path.isdir(directory):
        os.makedirs(directory)

    # criação de ficheiro txt
    file = open('%s/Temp_Info.txt' % directory, 'w')
    file.writelines(
        'Image     Coordinates      Max_T(ºC)      Min_T(ºC)               Time              Area(pixels)\n')
    file.close()

    dtt = 0
    coord_list = []
    r_list = []
    temp_list = []
    area_list = []
    i = 1

    # img = algorithmFunctions.captureImage()
    # temperatura_max, temperatura_min, minVal, maxVal, minLoc, maxLoc = algorithmFunctions.temperatureInformation(img)
    while dtt < 30:
        t0 = time.time()

        # imagem original
        kind_O = 'O%d' % i
        img = algorithmFunctions.captureImage()
        algorithmFunctions.saveImage(img, directory, kind_O)

        # imagem analisada
        percentage = 0.9
        temperatura_max, temperatura_min, minVal, maxVal, minLoc, maxLoc = algorithmFunctions.temperatureInformation(
            img)
        # interval = (maxVal * (temperatura_max - dT)) / temperatura_max
        interval = percentage * maxVal
        spot = img.copy()
        spot[np.where((np.all(spot >= [interval, interval, interval], axis=-1)))] = [0, 255, 255]
        kind_A = 'A%d' % i
        algorithmFunctions.saveImage(spot, directory, kind_A)

        # imagem binaria
        thresh = algorithmFunctions.binaryImage(img.copy(), interval)
        kind_B = 'B%d' % i
        algorithmFunctions.saveImage(thresh, directory, kind_B)

        '''
        ##########TESTE#########

        new = thresh.copy()
        maxArea=0
        _,contours,_ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        mask = np.ones(thresh.shape[:2], dtype="uint8") * 255

        test_list = []
        for cheese in range(len(contours)):
            area = cv2.contourArea(contours[cheese])
            test_list.append(area)

        test_list.sort()
        for c in contours:
             cv2.drawContours(mask, [c], -1, 0, -1)
             
        # teste teste teste
        '''

        # união das manchas
        _, contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL, 2)

        LENGTH = len(contours)
        status = np.zeros((LENGTH, 1))

        for k, cnt1 in enumerate(contours):
            x = k
            if k != LENGTH - 1:
                for l, cnt2 in enumerate(contours[k + 1:]):
                    x = x + 1
                    dist = algorithmFunctions.find_if_close(cnt1, cnt2)
                    if dist == True:
                        val = min(status[k], status[x])
                        status[x] = status[k] = val
                    else:
                        if status[x] == status[k]:
                            status[x] = k + 1

        unified = []
        maximum = int(status.max()) + 1
        for j in range(maximum):
            pos = np.where(status == j)[0]
            if pos.size != 0:
                cont = np.vstack(contours[j] for j in pos)
                hull = cv2.convexHull(cont)
                unified.append(hull)

        cv2.drawContours(img.copy(), unified, -1, (0, 255, 0), 2)
        cv2.drawContours(thresh, unified, -1, 255, -1)

        kind_C = 'C%d' % i
        algorithmFunctions.saveImage(thresh, directory, kind_C)

        # calculo de area e centro da area
        cX, cY, cnt, areaaaa = algorithmFunctions.centerOfMass(thresh)
        #area = cv2.contourArea(cnt[-1])

        algorithmFunctions.saveInformation(('%s.png' % kind_O), directory, areaaaa, cX, cY, temperatura_max,
                                           temperatura_min)

        coord_list.append([cX, cY])
        temp_list.append(temperatura_max)
        area_list.append(areaaaa)

        time.sleep(4.25)
        t1 = time.time()
        dt = t1 - t0
        dtt = dtt + dt
        i = i + 1
        print('check')
        continue

    print('Heat Analysis Over')
    print('Begin data analysis')

    # distancia entre medidas consecutivas

    for i in range(len(coord_list)):
        if i == 0:
            x2 = (coord_list[i])[0]
            x1 = (coord_list[i])[0]
            y2 = (coord_list[i])[1]
            y1 = (coord_list[i])[1]

        else:
            x2 = (coord_list[i])[0]
            x1 = (coord_list[i - 1])[0]
            y2 = (coord_list[i])[1]
            y1 = (coord_list[i - 1])[1]

        r_list.append(algorithmFunctions.distance(x1, x2, y1, y2))

    index_list = np.arange(1, len(temp_list) + 1, 1)

    r_eq = np.polyfit(index_list, r_list, 1)
    area_eq = np.polyfit(index_list, area_list, 1)
    temp_eq = np.polyfit(index_list, temp_list, 1)

    file = open('%s/Temp_Info.txt' % directory, 'a')
    file.writelines('\n          Centre Distance(pixels)\n')
    for i in range(len(coord_list) - 1):
        file.writelines('%d -> %d        %.4f \n' % (i, i + 1, r_list[i]))

    file.writelines('\n\n ################################################################################ \n')
    file.writelines('\nLinear Regression Equations (ax+b) \n')
    file.writelines('\nCentre Distance - %.4fx + %.4f \n' % (r_eq[0], r_eq[1]))
    file.writelines('Area - %.4fx + %.4f \n' % (area_eq[0], area_eq[1]))
    file.writelines('Temperature - %.4fx + %.4f \n' % (temp_eq[0], temp_eq[1]))
    file.close()

    print('Data Exported')
    print('distance')
    print(r_eq)
    print('area')
    print(area_eq)
    print('temperature')
    print(temp_eq)

    return index_list, r_list, area_list, temp_list, r_eq, area_eq, temp_eq, directory, go, now
