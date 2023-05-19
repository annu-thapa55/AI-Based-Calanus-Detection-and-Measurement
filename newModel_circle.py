"""using model to detect objects"""
import cv2
import os
import numpy as np
import csv
# constants
INPUT_WIDTH = 640
INPUT_HEIGHT = 640
SCORE_THRESHOLD = 0.85
NMS_THRESHOLD = 0.8
CONFIDENCE_THRESHOLD = 0.8

# Text parameters.
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
#change to 1 for easy testing
FONT_SCALE = 1.5
THICKNESS = 1

# Colors.
BLACK = (0, 0, 0)
BLUE = (255, 178, 50)
YELLOW = (0, 255, 255)
#kernel
kernel1 = np.ones((6, 6), np.uint8)
kernel2 = np.ones((9, 9), np.uint8)
def draw_label(im, label, x, y):
    """Draw text onto image at location."""
    # Get text size.
    text_size = cv2.getTextSize(label, FONT_FACE, FONT_SCALE, THICKNESS)
    dim, baseline = text_size[0], text_size[1]
    # Use text size to create a BLACK rectangle.*** delete it for test purpose
    #cv2.rectangle(im, (x,y), (x + dim[0], y + dim[1] + baseline), (0,0,0), cv2.FILLED);
    # Display text inside the rectangle.
    #cv2.putText(im, label, (x, y + dim[1]), FONT_FACE, FONT_SCALE, YELLOW, THICKNESS, cv2.LINE_AA)
    cv2.putText(im, label, (x+20, y+20 + dim[1]), FONT_FACE, FONT_SCALE, YELLOW, THICKNESS, cv2.LINE_AA)


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
      imgInRange = cv2.inRange(gImg, 40, 90)
      ret1, th1 = cv2.threshold(imgInRange,45,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
      edged = th1
      # edged = cv2.morphologyEx(th1, cv2.MORPH_OPEN, kernel1, iterations=3)
      # edged = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel2, iterations=1)
      # # edged = cv2.dilate(edged, kernel1, iterations=2)
      # edged = cv2.erode(edged, kernel1, iterations=1)
      # cv2.imshow("edged",edged)
      # cv2.waitKey(0)


      #find contours
      contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

      #find rotated boxes
      if len(contours) > 0:
            maxAreaContour = max(contours, key=cv2.contourArea)
            cnt = maxAreaContour
            # compute rotated rectangle (minimum area)
            circle = cv2.minEnclosingCircle(cnt)
            (ox, oy), radius = circle
            #get coordinates
            oy = oy + y
            ox = ox + x

            center = (int(ox), int(oy))
            radius = int(radius)
            boxes_bol = True
      else:
            center = 0
            radius = 0
            boxes_bol = False
      return center, radius, boxes_bol

def post_process(input_image, outputs,filename):
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
      #set label for measure how accurate manually
      c_label=1

      data=[]

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
            center, radius, boxes_bol = contours(cropImg, left, top)
            if boxes_bol == True:
                  # Draw bounding box.
                  input_image = cv2.circle(input_image, center, radius, BLUE, 3*THICKNESS)
                  # Class label.   *** a c_label added in here
                  #label = "{}:{}:{:.2f}, L:{}".format(c_label,classes[class_ids[i]], confidences[i],radius*2)

                  #label for easier testing
                  label = "{}".format(c_label)

                  #placeholder for convert pixel length to actural length
                  #actual_len=radius*2*ratio

                  #each calanus label and length
                  calanus_len=[c_label,radius*2]
                  #print(calanus_len)
                  #for the next one
                  c_label+=1

                  # Draw label.
                  draw_label(input_image, label, left, top)
            data.append(calanus_len)
      #print(data)

      #set the name of csv file as same as the name of image
      csv_filename = filename.replace(".jpg", ".csv")

      #if need to convert text file
      # csv_filename = filename.replace(".jpg", ".txt")
      #print(csv_filename)

      #set path of file
      csv_path = str(
            os.path.join("/Users/meiyundeng/PycharmProjects/computerVision/measurement/csvResult", csv_filename))


      # write the data to the CSV file

      with open(csv_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)

            header = ['cLabel', 'length']
            writer.writerow(header)
            for row in data:
                  writer.writerow(row)
      csv_file_path='/Users/meiyundeng/PycharmProjects/computerVision/measurement/csvResult'
      print(f"CSV file saved to: {csv_file_path}")

      #if need text file
      # with open(text_path, 'w', newline='') as file:
      #       writer = file.write
      #       for row in data:
      #             writer.writerow(row)
      #
      # print(f"CSV file saved to: {csv_file_path}")


      return input_image

if __name__ == '__main__':
      # Load class names.
      classesFile = "/Users/meiyundeng/PycharmProjects/computerVision/measurement/cocoTest.txt"
      classes = None
      with open(classesFile, 'rt') as f:
            classes = f.read().rstrip('\n').split('\n')
      modelWeights = "/Users/meiyundeng/PycharmProjects/computerVision/measurement/best.onnx"
      # Load image.
      directory = "/Users/meiyundeng/PycharmProjects/computerVision/measurement/A1_random"
      for file in os.listdir(directory):

            filename = os.fsdecode(file)
            print(filename)
            if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                  path = str(os.path.join(directory, filename))
                  frame = cv2.imread(path)
                  # Give the weight files to the model and load the network using       them.
                  net = cv2.dnn.readNet(modelWeights)
                  # Process image.
                  detections = pre_process(frame, net)
                  img = post_process(frame.copy(), detections, filename)
                  """now we have cropped image"""
                  t, _ = net.getPerfProfile()
                  label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
                  cv2.putText(img, label, (20, 40), FONT_FACE, FONT_SCALE, (0, 0, 255), THICKNESS, cv2.LINE_AA)
                  cv2.imwrite(os.path.join("/Users/meiyundeng/PycharmProjects/computerVision/measurement/result", filename), img)



                  # cv2.imshow('Output', img)
                  # cv2.waitKey(0)
      print("done")
      print(input(":"))
