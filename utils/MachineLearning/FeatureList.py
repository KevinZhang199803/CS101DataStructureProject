from utils import io
import numpy as np
import time

degree_const = 111 # 1 degree in longitutde/altitude equals 111 kilometers
dis_thr = 1.5 # distance (in kilometer) looking around
dis_max = 4
cab_nearby = 0.5
ptr = [104.0545, 30.7116]
init_time = time.time()

io.filepath = '/home/kevin/ShanghaiTech/Sophomore/DS/Project/Codes/MachineLearning/data/clusters_start.js'
cabDir = io.readin()
cabList = [[i['lng'],i['lat'],i['count']] for i in cabDir]

io.filepath = '/home/kevin/ShanghaiTech/Sophomore/DS/Project/Codes/MachineLearning/data/clusters_end.js'
cusDir = io.readin()
cusList = [[i['lng'],i['lat'],i['count']] for i in cusDir]

def distance(aLong, aLa, bLong, bLa):
	dis = degree_const * np.sqrt((aLong-bLong)**2 + (aLa-bLa)**2)
	return dis

def cabFeature(cabInfo, CabDir, CusDir):
	# calculate the score of each cab
	# 3 parts:
	# 1. # of cabs around this cab
	# 2. Distance to the customer
	# 3. # of customers around this cab
	# 1 and 3 will form the supply/demand factor of this cab
	cab = cabInfo
	cab_to_cus_dis = cabInfo[1]

	# # of cabs around
	cabAround = 0
	for i in CabDir:
		dis = distance(cab[0], cab[1], i[0], i[1])
		if dis < dis_thr:
			cabAround += i[2]

	# # of customers around
	cusAround = 0
	for i in CusDir:
		dis = distance(cab[0], cab[1], i[0], i[1])
		if dis < dis_thr:
			cusAround += i[2]
	if (cusAround != 0):
		return [cabAround, cusAround, '%.8f'%(cabAround/cusAround)]
	else:
		return [cabAround, cusAround, -1]

cabFeatures = [[i,distance(ptr[0], ptr[1], i[0], i[1]),cabFeature(i, cabList, cusList)] for i in cabList]
result = ''
for i in cabFeatures:
	result += (str(i)+'\n')
print(result)
print('use %.8f seconds'%(time.time()-init_time))