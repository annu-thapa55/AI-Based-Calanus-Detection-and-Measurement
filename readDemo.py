import os
import cv2 as cv
import csv
path = str(input("enter the path here (both folder and jpeg file are supported):"))
extension_input = str("." + input("enter the format of images (jpg or jpeg for example):"))
pwd = str(os.getcwd())
def fileWriter(dir,name,header,rows):
	#check if it's csv or txt file
	name_, extension = os.path.splitext(name)
	filePath = str(os.path.join(dir, name))
	if extension == ".csv":
		with open(filePath, 'w+', encoding='UTF8') as c:
			writer = csv.writer(c)
			# write the header
			writer.writerow(header)
			# write the data
			writer.writerows(rows)
	elif extension == ".txt":
		with open(filePath, 'w', encoding='UTF8') as f:
				f.write(header)
				f.write(rows)
# #method1
# condition = path.rsplit("/",1)[-1]
# list = []
#
# def fileReader(folderPath):
#
#
# if len(condition) <= 4:
#     print("folder")
# elif condition[-len(format):] == format:
#     list.append(path)
#     print("image")
# else:
#     print("folder2")
#method2
name, extension = os.path.splitext(path)
header = ["file name"]
if extension == "":
	# read all files under the folder and save those file names to a csv file
	fileNames = os.listdir(path)
	n = 0
	fileList = []
	for f in fileNames:
		name_, extension_ = os.path.splitext(str(f))
		if extension_ == extension_input:
			fileList.append([f])
			n = n +1
	# write to file
	fileWriter(pwd, "list.csv", header, fileList)
	print("total {} images.".format(n))
elif extension == extension_input:
	fileList = [[path]]
	fileWriter(pwd, "list.csv", header, fileList)
	print("total 1 image.")
else:
    print("wrong format input")
