# packages
import time
import os
import math
import cv2
import numpy as np
import sys

# global variables
root = os.path.join('static', 'root')
weights_path = os.path.join(root, 'model', 'best.onnx')
classes_path = os.path.join(root, 'model', 'coco.txt')
file_name_list_raw = []
file_name_list_split = []
length_list = []
pixel_mm_ratio = round(float(sys.argv[1]), 4)
window_size = 2400
lap_window_percen = 0.2
net = cv2.dnn.readNet(weights_path)
with open(classes_path, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')
buffer_area = 0
## constants
INPUT_WIDTH = 640
INPUT_HEIGHT = 640
SCORE_THRESHOLD = 0.85
NMS_THRESHOLD = 0.15
CONFIDENCE_THRESHOLD = 0.85
## Text parameters.
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.7
THICKNESS = 1
## Colors.
BLACK = (0, 0, 0)
BLUE = (255, 178, 50)
YELLOW = (0, 255, 255)


# sub-functions
# L3 functions
def draw_label(im, label, x, y):
    # Get text size.
    text_size = cv2.getTextSize(label, FONT_FACE, FONT_SCALE, THICKNESS)
    dim, baseline = text_size[0], text_size[1]
    cv2.putText(im, label, (x + 20, y + 20 + dim[1]), FONT_FACE, FONT_SCALE, YELLOW, THICKNESS, cv2.LINE_AA)


def YOLO_pre(input_image):
    # Create a 4D blob from a frame.
    blob = cv2.dnn.blobFromImage(input_image, 1 / 255, (INPUT_WIDTH, INPUT_HEIGHT), [0, 0, 0], 1, crop=False)

    # Set the input to the network.
    net.setInput(blob)

    # Run the forward pass to get output of the output layers.
    outputs = net.forward(net.getUnconnectedOutLayersNames())
    return outputs


def YOLO_post(detections, r):
    vali = True
    # List to hold respective values while unwrapping.
    row = detections[0][0][r]
    confidence = row[4]
    # Discard bad detections and continues.
    if confidence >= CONFIDENCE_THRESHOLD:
        classes_scores = row[5:]
        # Get the index of max class score.
        class_id = np.argmax(classes_scores)
        #  Continue if the class score is above threshold.
        if (classes_scores[class_id] > SCORE_THRESHOLD):
            # centre point, not the original point
            cx, cy, w, h = row[0], row[1], row[2], row[3]  # return these values
        else:
            vali = False
            cx, cy, w, h, class_id = 0, 0, 0, 0, 0
    else:
        vali = False
        cx, cy, w, h, class_id = 0, 0, 0, 0, 0
    return cx, cy, w, h, vali, confidence, class_id


def coordinates_calculator(top_para, left_para, input_image, cx, cy, w, h, confidence, class_id):
    image_height, image_width = input_image.shape[:2]
    # Resize factor. belongs to calculator
    x_factor = image_width / INPUT_WIDTH
    y_factor = image_height / INPUT_HEIGHT
    left = int((cx - w / 2) * x_factor)
    top = int((cy - h / 2) * y_factor)
    width = int(w * x_factor)
    height = int(h * y_factor)
    if left and top != 0:
        if left + width <= window_size - buffer_area and top + height <= window_size - buffer_area:
            # read image file name and get para
            left = left + left_para  # column. add second para of image name
            top = top + top_para  # row. add first para of image name
            box = np.array([left, top, width, height])
            boxes.append(box)
            confidences.append(confidence)
            class_ids.append(class_id)


# L2 functions
def file_name_reader(folder):
    global file_name_list_raw
    # read all files under the specific folder and return names as a list
    folder_path = str(os.path.join(root, folder))
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.jpg'):
            file_name_list_raw.append(file_name)


def detect(start_row, start_col, split_image):  # split image is in the split folder
    detections = YOLO_pre(split_image)
    for r in range(detections[0].shape[1]):
        cx, cy, w, h, vali, confidence, class_id = YOLO_post(detections, r)
        if vali:
            coordinates_calculator(start_row, start_col, split_image, cx, cy, w, h, confidence, class_id)


def lappingRegionCalculator(image_shape):  # image_shape is a list, [0] is row, [1] is column
    # how many vertical windows
    window_verti = math.ceil((image_shape[0] - window_size * 0.2) / (window_size - window_size * 0.2))
    # how many horizontal windows
    window_hori = math.ceil((image_shape[1] - window_size * 0.2) / (window_size - window_size * 0.2))

    return window_verti, window_hori


def slidingWindow(image_shape, image, window_verti, window_hori):
    overlapping_length_row = math.ceil(((window_size * window_verti) - image_shape[0]) / (window_verti - 1))
    overlapping_length_col = math.ceil(((window_size * window_hori) - image_shape[1]) / (window_hori - 1))
    for row in range(window_verti):
        start_row = (window_size * row) - (row * overlapping_length_row)
        for col in range(window_hori):
            start_col = (window_size * col) - (col * overlapping_length_col)
            split_image = image[start_row: start_row + window_size, start_col: start_col + window_size]
            detect(start_row, start_col, split_image)
    indices = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    return indices


def contours(cropImg):
    # pre processing
    gImg = cv2.cvtColor(cropImg, cv2.COLOR_BGR2GRAY)
    th1 = cv2.inRange(gImg, 30, 90)
    # ret1, th1 = cv2.threshold(imgInRange, 45, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    edged = th1
    # find contours
    contour, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contour


def crop(i, raw_image):
    box = boxes[i]
    left = box[0]
    top = box[1]
    width = box[2]
    height = box[3]
    # below is contour part
    cropImg = raw_image[top:top + height, left:left + width]
    return cropImg, left, top


def circle(raw_image, i, left, top, contour):
    global id
    id = id + 1
    boxes_bol = False
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
    if boxes_bol == True:
        # Draw bounding box.
        output_image = cv2.circle(raw_image, center, radius, BLUE, 1 * THICKNESS)
        label = "{}".format(id)
        # Draw label.
        draw_label(output_image, label, left, top)
        length_list.append([id, (radius * 2) * pixel_mm_ratio, confidences[i]])
    return output_image


def visualizing(output_image, raw_image_name):
    cv2.imwrite(os.path.join(root, 'result', raw_image_name), output_image)


def textfile(length_list, raw_image_name):
    text_file_path = os.path.join(root, 'result', os.path.splitext(raw_image_name)[0] + '_result' + '.txt')
    file = open(text_file_path, 'w+', encoding='UTF8')
    header = 'ID,length_in_mm,confidence'
    file.write(header + '\n')
    for length in length_list:
        length = ",".join(map(str, length))
        file.write(str(length) + '\n')
    file.close()

# L1 functions
def dir_init(raw_img_folder='raw'):
    file_name_reader(raw_img_folder)

def image_pre(raw_image):
    if raw_image.shape[0] and raw_image.shape[1] != 2400:
        window_verti, window_hori = lappingRegionCalculator(raw_image.shape)
        indices = slidingWindow(raw_image.shape, raw_image, window_verti, window_hori)
    return indices

def measure(raw_image, indices):  # need indices, for one raw image
    global length_list
    length_list = []
    if len(indices) != 0:
        for i in indices:  # iterate through all boxes
            cropImg, left, top = crop(i, raw_image)
            contour = contours(cropImg)
            output_image = circle(raw_image, i, left, top, contour)
    else:
        output_image = raw_image
    return output_image

def file_image_output(output_image):  # for one raw image
    visualizing(output_image, raw_image_name)
    # generate text file
    textfile(length_list, raw_image_name)

# main program
# for time calculating
start = time.time()

dir_init()
for raw_image_name in file_name_list_raw:  # first loop. raw
    id = 0
    raw_image = cv2.imread(os.path.join(root, 'raw', raw_image_name))
    boxes = []
    confidences = []
    class_ids = []
    indices = image_pre(raw_image)
    output_image = measure(raw_image, indices)
    file_image_output(output_image)

end = time.time()
print('runing time is :', end - start)

