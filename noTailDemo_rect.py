"""using model to detect objects"""
import cv2
import os
import numpy as np
# constants
INPUT_WIDTH = 640
INPUT_HEIGHT = 640
SCORE_THRESHOLD = 0.85
NMS_THRESHOLD = 0.8
CONFIDENCE_THRESHOLD = 0.8

# Text parameters.
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.7
THICKNESS = 1

# Colors.
BLACK = (0, 0, 0)
BLUE = (255, 178, 50)
YELLOW = (0, 255, 255)
#kernel
kernel = np.ones((9, 9), np.uint8)

def draw_label(im, label, x, y):
    """Draw text onto image at location."""
    # Get text size.
    text_size = cv2.getTextSize(label, FONT_FACE, FONT_SCALE, THICKNESS)
    dim, baseline = text_size[0], text_size[1]
    # Use text size to create a BLACK rectangle.
    cv2.rectangle(im, (x,y), (x + dim[0], y + dim[1] + baseline), (0,0,0), cv2.FILLED);
    # Display text inside the rectangle.
    cv2.putText(im, label, (x, y + dim[1]), FONT_FACE, FONT_SCALE, YELLOW, THICKNESS, cv2.LINE_AA)


def pre_process(input_image, net):
	# Create a 4D blob from a frame.
	blob = cv2.dnn.blobFromImage(input_image, 1 / 255, (INPUT_WIDTH, INPUT_HEIGHT), [0, 0, 0], 1, crop=False)

	# Sets the input to the network.
	net.setInput(blob)

	# Run the forward pass to get output of the output layers.
	outputs = net.forward(net.getUnconnectedOutLayersNames())
	return outputs


def contours(cropImg,x,y):
      box = 0
      boxes_bol = False
      #pre processing
      gImg = cv2.cvtColor(cropImg, cv2.COLOR_BGR2GRAY)
      imgInRange = cv2.inRange(gImg, 22, 43)
      ret1, th1 = cv2.threshold(imgInRange,43,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
      # edged = cv2.Canny(th1, 50, 100, L2gradient=True)
      # edged = cv2.dilate(th1, None, iterations=1)
      edged = cv2.morphologyEx(th1, cv2.MORPH_OPEN, kernel, iterations=2)
      edged = cv2.erode(edged, None, iterations=1)

      #find contours
      contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
      #find rotated boxes
      for i in range(len(contours)):
            cnt = contours[i]
            # draw contours
            img = cv2.drawContours(th1, contours, -1, (255, 255, 0), 2)
            # compute rotated rectangle (minimum area)
            rect = cv2.minAreaRect(cnt)
            (ox, oy), (width, height), angle = rect
            #get coordinates
            if width and height >= 40:
                  if width >= height:
                        if width/height >= 1.4:
                              box = cv2.boxPoints(rect)
                              box = np.int0(box)
                              boxes_bol = True
                              box[:, 1] = box[:, 1] + y
                              box[:, 0] = box[:, 0] + x
                  elif width < height:
                        if height/width >= 1.4:
                              box = cv2.boxPoints(rect)
                              box = np.int0(box)
                              boxes_bol = True
                              box[:, 1] = box[:, 1] + y
                              box[:, 0] = box[:, 0] + x
            else:
                  boxes_bol = False
                  # img = cv2.drawContours(img, [box], 0, (0, 255, 255), 2)
      print(box)
      return box, boxes_bol

def post_process(input_image, outputs):
      # Lists to hold respective values while unwrapping.
      class_ids = []
      confidences = []
      boxes = []
      # Rows.
      rows = outputs[0].shape[1]
      image_height, image_width = input_image.shape[:2]
      # Resizing factor.
      x_factor = image_width / INPUT_WIDTH
      y_factor =  image_height / INPUT_HEIGHT
      # Iterate through detections.
      for r in range(rows):
            row = outputs[0][0][r]
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
                        cx, cy, w, h = row[0], row[1], row[2], row[3]
                        left = int((cx - w/2) * x_factor)
                        top = int((cy - h/2) * y_factor)
                        width = int(w * x_factor)
                        height = int(h * y_factor)
                        box = np.array([left, top, width, height])
                        boxes.append(box)
# Perform non maximum suppression to eliminate redundant, overlapping boxes with lower confidences.
      indices = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
      for i in indices:
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            if left < 0:
                  left = 0
            if top < 0:
                  top = 0
            """what i need to do is crop the image and return it. no need to draw bounding boxes on raw image"""
            # cv2.rectangle(input_image, (left, top), (left + width, top + height), BLUE, 3 * THICKNESS)
            cropImg = input_image[top:top+height, left:left+width]
            contoursbox, boxes_bol = contours(cropImg, left, top)
            if boxes_bol == True:
                  # Draw bounding box.
                  input_image = cv2.drawContours(input_image, [contoursbox], -1, BLUE, 3*THICKNESS)
                  # Class label.
                  label = "{}:{:.2f}".format(classes[class_ids[i]], confidences[i])
                  # Draw label.
                  draw_label(input_image, label, left, top)
      return input_image

if __name__ == '__main__':
      # Load class names.
      classesFile = "/Users/jackyan_1/PycharmProjects/plankton/test/model/cocoTest.txt"
      classes = None
      with open(classesFile, 'rt') as f:
            classes = f.read().rstrip('\n').split('\n')
      modelWeights = "/Users/jackyan_1/PycharmProjects/plankton/test/model/best.onnx"
      # Load image.
      directory = "/Users/jackyan_1/PycharmProjects/plankton/test/res/images"
      for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                  path = str(os.path.join(directory, filename))
                  frame = cv2.imread(path)
                  # Give the weight files to the model and load the network using       them.
                  net = cv2.dnn.readNet(modelWeights)
                  # Process image.
                  detections = pre_process(frame, net)
                  img = post_process(frame.copy(), detections)
                  """now we have cropped image"""
                  t, _ = net.getPerfProfile()
                  label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
                  print(label)
                  print(img.shape)
                  cv2.putText(img, label, (20, 40), FONT_FACE, FONT_SCALE, (0, 0, 255), THICKNESS, cv2.LINE_AA)
                  cv2.imshow('Output', img)
                  cv2.waitKey(0)
      print("done")
      print(input(":"))


