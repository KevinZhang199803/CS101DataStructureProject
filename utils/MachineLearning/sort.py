import sys

degree_const = 111 # 1 degree in longitutde/altitude equals 111 kilometers
dis_thr = 1.5 # distance (in kilometer) looking around
dis_max = 4
cab_nearby = 0.5

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
		while left_mark <= right_mark and a_list[left_mark][2][2] <= pivot_value[2][2]:
			left_mark += 1
		while a_list[right_mark][2][2] >= pivot_value[2][2] and right_mark >= left_mark:
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

cabList = []
raw = sys.stdin.read().replace('inf','-1')
lines = raw.split('\n')
del lines[-1]
cabList = [eval(i) for i in lines]
for i in cabList:
	i[2][2] = float(i[2][2])
quick_sort(cabList)
for i in cabList:
	if (i[1] <= dis_max and i[2][2] != -1 and i[2][2] < 1):
		print(i)