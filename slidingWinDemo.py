"""sliding window. Doing segmentation. keep 20% as overlapping region"""
import cv2 as cv
import math
def lappingRegionCalculator(length, windowSize):
    lappingThres = int(windowSize * 0.2)
    # n is the number of windows and x is the length or width(depends on which dimension are you calculating) of the overlapping region.
    n = length // windowSize
    while True:
        x = math.ceil((windowSize * n - length) / (n - 1))
        if x > lappingThres:
            break
        else:
            n = n + 1
            continue
    return n, x
def slidingWindow(img, windowSize, nR, xR, nC, xC):
    for r in range(nR):
        startR = windowSize * r - xR * r
        for c in range(nC):
            startC = windowSize * c - xC * c
            cv.imwrite(f"plankton/img{startR}_{startC}.jpg", img[startR: startR + windowSize, startC: startC + windowSize])



if __name__ == '__main__':
    path = "1008_a1_01_b_less_dense.jpg"
    windowSize = 640
    image = cv.imread(path)
    #calculate overlapping area for column
    n_column, x_column = lappingRegionCalculator(image.shape[1], windowSize)
    print(n_column, x_column)
    #calculate overlapping area for row
    n_row, x_row = lappingRegionCalculator(image.shape[0], windowSize)
    print(n_row, x_row)
    #segmentation
    slidingWindow(image,windowSize,n_row,x_row,n_column,x_column)
