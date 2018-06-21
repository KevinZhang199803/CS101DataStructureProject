import numpy as np

degree_const = 111 # 1 degree in longitutde/altitude equals 111 kilometers
dis_thr = 1.5 # distance (in kilometer) looking around
dis_max = 4
cab_nearby = 0.5

def distance(aLong, aLa, bLong, bLa):
	dis = degree_const * np.sqrt((aLong-bLong)**2 + (aLa-bLa)**2)
	return dis

def cabScore(cabInfo, CabDir, CusDir):
	# calculate the score of each cab
	# 3 parts:
	# 1. # of cabs around this cab
	# 2. Distance to the customer
	# 3. # of customers around this cab
	# 1 and 3 will form the supply/demand factor of this cab
	cab = cabInfo[0]
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

	supply_urgency_factor = 10 ** ((cabAround/cusAround)**2 - 1)# will be developed by machine learning
	distance_factor = 100 ** (dis_thr-cab_to_cus_dis)# will be developed by machine learning

	if (cab_to_cus_dis > dis_max):
		return -1
	elif (cab_to_cus_dis < cab_nearby):
		return -2
	else:
		return (supply_urgency_factor+distance_factor)

def quick_sort(a_list):
	quick_sort_helper(a_list, 0, len(a_list) - 1)

def quick_sort_helper(a_list, first, last):
	if first < last:
		split_point = partition(a_list, first, last)
		quick_sort_helper(a_list, first, split_point - 1)
		quick_sort_helper(a_list, split_point + 1, last)

def partition(a_list, first, last):
	pivot_value = a_list[first]
	left_mark = first + 1
	right_mark = last
	done = False
	while not done:
		while left_mark <= right_mark and a_list[left_mark][2] <= pivot_value[2]:
			left_mark += 1
		while a_list[right_mark][2] >= pivot_value[2] and right_mark >= left_mark:
			right_mark -= 1
		if right_mark < left_mark:
			done = True
		else:
			temp = a_list[left_mark]
			a_list[left_mark] = a_list[right_mark]
			a_list[right_mark] = temp
	
	temp = a_list[first]
	a_list[first] = a_list[right_mark]
	a_list[right_mark] = temp
	return right_mark

def GrabCab(hubLong, hubLa, CabDir, CusDir):
	'''
	hubLong: longtitude of the hub requesting for a cab
	hubLa: altitude of the hub requesting for a cab
	CabDir: a list of Cabhubs around (within dis_thr)
	element follows:
	[longtitude, Altitude, # of cabs]
	CusDir: a list of Customers around
	element follows:
	[longtitude, Altitude, # of cabs]
	'''
	# get neaby valid hubs, sum up all available cabs
	nearbyHubs = []
	availableCabs = 0
	for i in CabDir:
		dis = distance(hubLong, hubLa, i[0], i[1])
		if dis < dis_thr:
			nearbyHubs.append([i, dis, cadScore([i, dis], CabDir, CusDir)])
			availableCabs += i[2]

	# look for a suitable hub for a cab
	# calculate the "score" of the cab
	# we will consider both # of cars and distance to distribute a cab there
	quick_sort(nearbyHubs)
	if nearbyHubs != []:
		if nearbyHubs[0][2] == -2:# at least one cab nearby
			return nearbyHubs[0]
		else:
			return nearbyHubs[-1]
	else:
		return None
		