# packages
import os
import math
import cv2
import numpy as np
# global var
root = os.getcwd()
weights_path = os.path.join(root,'model','best.onnx')
classes_path = os.path.join(root,'model','coco.txt')
file_name_list_raw = []
file_name_list_split = []
length_list = []
windowSize = 2400
net = cv2.dnn.readNet(weights_path)
with open(classes_path, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')
## constants
INPUT_WIDTH = 640
INPUT_HEIGHT = 640
SCORE_THRESHOLD = 0.75
NMS_THRESHOLD = 0.15
CONFIDENCE_THRESHOLD = 0.7
## Text parameters.
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.7
THICKNESS = 1
## Colors.
BLACK = (0, 0, 0)
BLUE = (255, 178, 50)
YELLOW = (0, 255, 255)

# sub-functions
#L3 functions
def draw_label(im, label, x, y):
    """Draw text onto image at location."""
    # Get text size.
    text_size = cv2.getTextSize(label, FONT_FACE, FONT_SCALE, THICKNESS)
    dim, baseline = text_size[0], text_size[1]
    # Use text size to create a BLACK rectangle.
    cv2.rectangle(im, (x,y), (x + dim[0], y + dim[1] + baseline), (0,0,0), cv2.FILLED);
    # Display text inside the rectangle.
    cv2.putText(im, label, (x, y + dim[1]), FONT_FACE, FONT_SCALE, YELLOW, THICKNESS, cv2.LINE_AA)
#L2 functions
def file_name_reader(folder,para):
    if para == "raw":
        global file_name_list_raw
        #read all files under the specific folder and return names as a list
        #generate the dir
        folder_path = str(os.path.join(root, folder))
        file_name_list_raw = os.listdir(folder_path)
    elif para == "split":
        global file_name_list_split
        # read all files under the specific folder and return names as a list
        # generate the dir
        folder_path = str(os.path.join(root, 'split', folder))
        file_name_list_split = os.listdir(folder_path)

def folder_maker(name_list):
    for i in name_list:
        new_path = os.path.join(root,'split',str(i))
        os.makedirs(new_path, exist_ok=True)

def lappingRegionCalculator(length):
    lappingThres = int(windowSize * 0.4)
    # n is the number of windows and x is the length or width(depends on which dimension are you calculating) of the overlapping region.
    for i in (length[0], length[1]):
        # [0] is row, [1] is column
        if i == length[0]:
            nR = i // windowSize
            while True:
                xR = math.ceil((windowSize * nR - i) / (nR - 1))
                if xR > lappingThres:
                    break
                else:
                    nR = nR + 1
        else:
            nC = i // windowSize
            while True:
                xC = math.ceil((windowSize * nC - i) / (nC - 1))
                if xC > lappingThres:
                    break
                else:
                    nC = nC + 1
    return nR, xR, nC, xC

def slidingWindow(img_name,img, folder, nR, xR, nC, xC):
    for r in range(nR):
        startR = windowSize * r - xR * r
        for c in range(nC):
            startC = windowSize * c - xC * c
            cv2.imwrite(os.path.join(folder, img_name, 'img_{}_{}.jpg'.format(startR,startC)),img[startR: startR + windowSize, startC: startC + windowSize])


def contours(cropImg, x, y):
    box = 0
    boxes_bol = False
    # pre processing
    gImg = cv2.cvtColor(cropImg, cv2.COLOR_BGR2GRAY)
    imgInRange = cv2.inRange(gImg, 40, 90)
    ret1, th1 = cv2.threshold(imgInRange, 45, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    edged = th1
    # find contours
    contour, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contour

def YOLO_pre(input_image):
    # Create a 4D blob from a frame.
    blob = cv2.dnn.blobFromImage(input_image, 1 / 255, (INPUT_WIDTH, INPUT_HEIGHT), [0, 0, 0], 1, crop=False)

    # Sets the input to the network.
    net.setInput(blob)

    # Run the forward pass to get output of the output layers.
    outputs = net.forward(net.getUnconnectedOutLayersNames())
    return outputs

def YOLO_post(detections,r):
    vali = True
    # Lists to hold respective values while unwrapping.
    row = detections[0][0][r]
    confidence = row[4]
    # Discard bad detections and continue.
    if confidence >= CONFIDENCE_THRESHOLD:
        classes_scores = row[5:]
        # Get the index of max class score.
        class_id = np.argmax(classes_scores)
        #  Continue if the class score is above threshold.
        if (classes_scores[class_id] > SCORE_THRESHOLD):
            confidences.append(confidence)
            class_ids.append(class_id)
            # centre point, not the original point
            cx, cy, w, h = row[0], row[1], row[2], row[3] # return these values
        else:
            vali = False
            cx, cy, w, h = 0,0,0,0
    else:
        vali = False
        cx, cy, w, h = 0, 0, 0, 0
    return cx, cy, w, h,vali

def coordinates_calculator(image_name,input_image, cx, cy, w, h):
    image_height, image_width = input_image.shape[:2]
    # Resizing factor. belongs to calculator
    x_factor = image_width / INPUT_WIDTH
    y_factor = image_height / INPUT_HEIGHT
    left = int((cx - w / 2) * x_factor)
    top = int((cy - h / 2) * y_factor)
    width = int(w * x_factor)
    height = int(h * y_factor)
    """I need recalculate coordinates here to satisfy the merge method, merge all images before run the NMS method."""
    #read image file name and get para
    left_para = int(os.path.splitext(image_name)[0].split('_')[2])
    top_para = int(os.path.splitext(image_name)[0].split('_')[1])
    left = left + left_para #column. add second para of image name
    top = top + top_para #row. add first para of image name
    box = np.array([left, top, width, height])
    boxes.append(box)

def crop(i, raw_image):
    box = boxes[i]
    left = box[0]
    top = box[1]
    width = box[2]
    height = box[3]
    """what i need to do is crop the image and return it. no need to draw bounding boxes on raw image"""
    # cv2.rectangle(input_image, (left, top), (left + width, top + height), BLUE, 3 * THICKNESS)
    """need to use raw image here, not 2400*2400"""
    # below is contour part
    cropImg = raw_image[top:top + height, left:left + width]
    return cropImg, left, top

def circle(raw_image, i, left, top, contour):
    # find rotated boxes
    if len(contour) > 0:
        maxAreaContour = max(contour, key=cv2.contourArea)
        cnt = maxAreaContour
        # compute rotated rectangle (minimum area)
        circle = cv2.minEnclosingCircle(cnt)
        (ox, oy), radius = circle
        # get coordinates
        oy = oy + top
        ox = ox + left

        center = (int(ox), int(oy))
        radius = int(radius)
        boxes_bol = True
    else:
        center = 0
        radius = 0
        boxes_bol = False
    if boxes_bol == True:
        # Draw bounding box.
        output_image = cv2.circle(raw_image, center, radius, BLUE, 3 * THICKNESS)
        # Class label.
        label = "{}:{:.2f}, L:{}".format(classes[class_ids[i]], confidences[i], radius * 2)
        # Draw label.
        draw_label(output_image, label, left, top)
        length_list.append(radius*2)
    return output_image

def visualizing(output_image,image_raw_name):
    cv2.imwrite(os.path.join(root,'result',image_raw_name), output_image)

def textfile(length_list,image_raw_name):
    text_file_path = os.path.join(root,'result', os.path.splitext(image_raw_name)[0]+'_result'+'.txt')
    file = open(text_file_path, 'w+', encoding='UTF8')
    for length in length_list:
        file.write(str(length) + os.linesep)
    file.close()

#L1 functions
"""init dir, pre-processing all images, detect, measure, output"""
def dir_init(raw_img_folder = 'raw'):
    file_name_reader(raw_img_folder,"raw")
    folder_maker(file_name_list_raw)
def image_pre():
    #split
    for image_raw_name in file_name_list_raw:
        folder_path_raw = os.path.join(root,'raw')
        folder_path_split = os.path.join(root,'split')
        image_raw = cv2.imread(os.path.join(folder_path_raw,image_raw_name))
        if image_raw.shape[0] and image_raw.shape[1] != 2400:
            nR, xR, nC, xC = lappingRegionCalculator(image_raw.shape)
            slidingWindow(image_raw_name, image_raw, folder_path_split, nR, xR, nC, xC)
        else:
            cv2.imwrite(os.path.join(root, 'split', image_raw_name, 'img_0_0.jpg'), image_raw)
def detect(split_image_name,split_image):#split image is in the solit folder
    detections = YOLO_pre(split_image)
    for r in range(detections[0].shape[1]):
        cx, cy, w, h, vali = YOLO_post(detections,r)
        if vali:
            coordinates_calculator(split_image_name, split_image, cx, cy, w, h)
    indices = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    return indices
def measure(raw_image, indices):# need indices, for one raw image
    global length_list
    length_list = []
    if len(indices) != 0:
        for i in indices:#iterate through all boxes
            cropImg, left, top = crop(i, raw_image)
            contour = contours(cropImg, left, top)
            output_image = circle(raw_image, i, left, top, contour)
    else:
        output_image = raw_image
    return output_image
def file_image_output(output_image):# for one raw image
    # visualise image output
    # cv2.imshow('test', output_image)
    # cv2.waitKey(0)
    visualizing(output_image,image_raw_name)
    # generate text file
    textfile(length_list, image_raw_name)
# main program
"""call L1 functions one by one"""
if __name__ == '__main__':
    dir_init()
    image_pre()
    for image_raw_name in file_name_list_raw:# first loop. raw
        print(image_raw_name)
        raw_image = cv2.imread(os.path.join(root,'raw',image_raw_name))
        boxes = []
        confidences = []
        class_ids = []
        file_name_reader(image_raw_name, "split")
        for split_image_name in file_name_list_split:# second loop. split
            split_image = cv2.imread(os.path.join(root,'split',image_raw_name,split_image_name))
            indices = detect(split_image_name,split_image)# loop ends here, next function runs on raw image
        output_image = measure(raw_image, indices)
        file_image_output(output_image)


