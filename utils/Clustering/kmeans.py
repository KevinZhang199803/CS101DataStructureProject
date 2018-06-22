import random
import numpy as np

eps = 0.005


def findNearest(kPoint, point, k):
    num = 0
    dn = (kPoint[0][0] - point[0]) * (kPoint[0][0] - point[0]) + \
         (kPoint[0][1] - point[1]) * (kPoint[0][1] - point[1])
    for i in range(1, k):
        d = (kPoint[i][0] - point[0]) * (kPoint[i][0] - point[0]) + \
            (kPoint[i][1] - point[1]) * (kPoint[i][1] - point[1])
        if (d < dn):
            dn = d
            num = i
    return num


def kmeans(data, k):
    tot = 0
    kPoint = np.zeros((k, 2), dtype=float)
    maxx = maxy = 0
    minx = miny = 100000
    print(data.shape)
    cnt = data.shape[0]
    for i in range(cnt):
        maxx = max(maxx, data[i][0])
        minx = min(minx, data[i][0])
        maxy = max(maxy, data[i][1])
        miny = min(miny, data[i][1])
    for i in range(k):
        x = random.random() * (maxx - minx) + minx  # 经度
        y = random.random() * (maxy - miny) + miny  # 纬度
        kPoint[i][0] = x
        kPoint[i][1] = y
    dataId = np.zeros(cnt, dtype=int)
    while True:
        tot += 1
        for i in range(cnt):
            dataId[i] = findNearest(kPoint, data[i], k)
        center = np.zeros((k, 3), dtype=float)
        for i in range(cnt):
            center[dataId[i]][0] += float(data[i][0])
            center[dataId[i]][1] += float(data[i][1])
            center[dataId[i]][2] += 1
        for i in range(k):
            if (center[i][2] != 0):
                center[i][0] /= center[i][2]
                center[i][1] /= center[i][2]
            else:
                center[i][0] = kPoint[i][0]
                center[i][1] = kPoint[i][1]

        b = 0
        ep = 0
        for i in range(k):
            ep = max(ep, abs(center[i][0] - kPoint[i][0]))
            ep = max(ep, abs(center[i][1] - kPoint[i][1]))
            if (abs(center[i][0] - kPoint[i][0]) > eps):
                b = 1
            if (abs(center[i][1] - kPoint[i][1]) > eps):
                b = 1
            kPoint[i][0] = center[i][0]
            kPoint[i][1] = center[i][1]
        print(ep, end='   ')
        print(tot)
        if (not b):
            break
    return kPoint, dataId


if __name__ == '__main__':
    print("No")
