degree_const = 111 # 1 degree in longitutde/altitude equals 111 kilometers
dis_thr = 2 # distance (in kilometer) looking around
elaborateConst = 50
awardRange = [4, 10]
awardBase = 2

def distance(aLong, aLa, bLong, bLa):
	dis = degree_const * np.sqrt((aLong-bLong)**2 + (aLa-bLa)**2)
	return dis

def isNeedAward(hubLong, hubLa, cabDir, cusDir):
	availableCabs = 0
	for i in cabDir:
		dis = distance(hubLong, hubLa, i[0], i[1])
		if dis < dis_thr:
			availableCabs += i[2]

	customers = 0
	for i in cusDir:
		dis = dis = distance(hubLong, hubLa, i[0], i[1])
		if dis < dis_thr:
			customers += i[2]

	elaborateConst = int(0.05 * customers)
	if (availableCabs < customers):#urgently needed
		return [1, availableCabs, customers]
	else if (availableCabs < customers+elaborateConst):
		return [2, availableCabs, customers]
	else:
		return [-1, availableCabs, customers]

def getCabs(hubLong, hubLa, cabDir, cusDir):
	hubList = []
	for i in cabDir:
		isNeeded = isNeedAward(hubLong, hubLa, cabDir, cusDir)
		dis = distance(hubLong, hubLa, i[0], i[1])
		if (isNeeded[0] == -1 and dis > awardRange[0] and dis < awardRange[1]):
			hubList.append([i, isNeeded])

	return hubList


def getAward(hubLong, hubLa, cabDir, cusDir):
	isNeeded = isNeedAward(hubLong, hubLa, cabDir, cusDir)

	if (isNeeded == 1):
		#urgently needed
		awardTargets = getCabs(hubLong, hubLa, cabDir, cusDir)
		if (awardTargets != []):
			totalCabs = 0
			totalCus = 0
			for i in awardTargets:
				totalCabs += i[1]
				totalCus += i[2]
			vacantRate = (totalCabs - totalCus) / totalCabs
			award = awardBase * 10**(1-vacantRate)
			return award
		else:
			return 999
