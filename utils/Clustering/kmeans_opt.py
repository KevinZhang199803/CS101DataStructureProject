import numpy as np
from multiprocessing import Pool

eps = 0.0001


kPoint_g = None


def findNearest(point):
    d = np.square(kPoint_g[:, 0] - point[0]) + np.square(kPoint_g[:, 1] - point[1])
    return np.argmin(d)


def kmeans(data, k):
    iter_cnt = 0

    maxx, maxy = np.max(data, axis=0)
    minx, miny = np.min(data, axis=0)

    global kPoint_g

    kPoint = np.array([np.mean(trunk, axis=0) for trunk in np.array_split(data, k)])

    # kPoint = np.stack((np.random.random(k) * (maxx - minx) + minx,
    #                    np.random.random(k) * (maxy - miny) + miny), axis=-1)

    while True:
        iter_cnt += 1

        kPoint_g = kPoint

        center = np.zeros((k, 2), dtype=float)

        with Pool() as p:
            dataId = np.fromiter(p.map(findNearest, data), dtype=np.int)
            # sum(p.map(np.array_split(dataId), np.array_split(data)))

        np.add.at(center, dataId, data)

        count = np.bincount(dataId, minlength=k)

        cond = count != 0
        center[cond, 0] /= count[cond]
        center[cond, 1] /= count[cond]
        cond = count == 0
        center[cond] = kPoint[cond]

        ep = np.sqrt(np.max(np.square(center[:, 0] - kPoint[:, 0]) +
                            np.square(center[:, 1] - kPoint[:, 1])))

        kPoint = center

        print(ep, ' ', iter_cnt)

        if ep <= eps:
            break

    return kPoint, dataId


if __name__ == '__main__':
    print("No")
