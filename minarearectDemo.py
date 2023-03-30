import cv2
import numpy as np
path1 = '/Users/jackyan_1/PycharmProjects/plankton/test/res/1008_a2_04_b_1_3_2.jpg'
path2 = '/Users/jackyan_1/PycharmProjects/plankton/test/res/img13689_10647.jpg'
kernel = np.ones((9, 9), np.uint8)
img = cv2.imread(path2)
img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgInRange = cv2.inRange(img1,20,41)
ret,thresh = cv2.threshold(imgInRange,35,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
cv2.imshow("thresh", thresh)
edged = cv2.Canny(thresh, 50, 100, L2gradient = True)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)
edged = cv2.morphologyEx(edged, cv2.MORPH_TOPHAT, kernel)

cv2.imshow("edged", edged)
contours,_ = cv2.findContours(edged, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

# print("Number of contours detected:", len(contours))

# compute straight bounding rectangle
# x,y,w,h = cv2.boundingRect(cnt)
# img = cv2.drawContours(img,contours,-1,(255,255,0),2)
# img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

# compute rotated rectangle (minimum area)
for i in range(len(contours)):
	cnt = contours[i]
	rect = cv2.minAreaRect(cnt)
	(x, y), (width, height), angle = rect
	if width and height >= 80:
		box = cv2.boxPoints(rect)
		box = np.int0(box)
		print(width,height)
		# draw minimum area rectangle (rotated rectangle)
		img = cv2.drawContours(img,[box],0,(0,255,255),2)
cv2.imshow("Bounding Rectangles", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
