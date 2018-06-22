import json

filepath = "../data/clusters_start.js"

def readin():
	with open(filepath, encoding="utf-8") as f:
		dic = eval(f.read())
		return dic
