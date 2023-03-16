"""three steps
1. select object
2. enter scale
3. calculate ratio
"""

start = []
end = []
lengthList = []
import cv2 as cv
def selectObj(action, x, y, flags, *userdata):
	global start, end, lengthList
	if action == cv.EVENT_LBUTTONDOWN:
		start = [(x, y)]
		x1 = start[0][0]
		lengthList.append(x1)
	elif action == cv.EVENT_LBUTTONUP:
		end = [(x, y)]
		cv.rectangle(img_raw, start[0], end[0], (0, 255, 0), 2, 8)
		cv.imshow("img_window", img_raw)
		x2 = end[0][0]
		lengthList.append(x2)

def ratioCalculator(scale):
	width = lengthList[1] - lengthList[0]
	ratio = scale / width
	return ratio

if __name__ == '__main__':
	#how to draw
	print("press and hold left mouse button to start drawing. release it after finish darwing process.")
	#show img
	path = "/Users/jackyan_1/PycharmProjects/plankton/test/res/1008_a1_01_b_less_dense.jpg"
	img_raw = cv.imread(path)
	img_ept = img_raw.copy()
	cv.namedWindow("img_window")
	#draw on img
	cv.setMouseCallback("img_window", selectObj)
	k = 0
	# Close the window when key enter is pressed
	while k != 13:
		# Display the image
		cv.imshow("img_window", img_raw)
		k = cv.waitKey(0)
		# If c is pressed, clear the window, using the dummy image
		if (k == 99):
			img_raw = img_ept.copy()
			cv.imshow("img_window", img_raw)
			lengthList = []
	cv.destroyAllWindows()
	#width value
	print(lengthList)
	print("enter the width of selected object. unit of measurement: mm")
	rScale = int(input(":"))
	ratio = ratioCalculator(rScale)
	print(ratio)
