import os
import sys
import cv2
from math import log, floor

IMAGE_FORMATS = [".jpg", ".jpeg", ".bmp", ".png"]

class Image:
    def __init__(self, image, name):
        self._image = image
        self._name = name
        self._height = self._image.shape[0]
        self._width = self._image.shape[1]
        self._center_x = self._width // 2
        self._center_y = self._height // 2

    def get_image(self):
        return self._image

    def get_name(self):
        return self._name

    def show_image(self):
        cv2.imshow("Image", self._image)
        cv2.waitKey(0)

    def split(self):
        new_images = []

        top_left = Image(self._image[0:self._center_y, 0:self._center_x], self._name + "_1")
        new_images.append(top_left)

        top_right = Image(self._image[0:self._center_y, self._center_x:self._width], self._name + "_2")
        new_images.append(top_right)

        bottom_left = Image(self._image[self._center_y:self._height, 0:self._center_x], self._name + "_3")
        new_images.append(bottom_left)

        bottom_right = Image(self._image[self._center_y:self._height, self._center_x:self._width], self._name + "_4")
        new_images.append(bottom_right)

        return new_images


class ImageSplitter:
    def __init__(self, input_file, output_number):
        self._file_name, self._file_extension = os.path.splitext(input_file)
        self._output_number = output_number
        self._original_image = Image(cv2.imread(input_file), self._file_name)
        self._output_images = []

    def split_image(self):
        new_images = self._original_image.split()

        while True:
            if len(new_images) >= self._output_number:
                break

            images = []

            for image in new_images:
                images += image.split()

            new_images = images

        self._output_images = new_images

    def save_images(self):
        for image in self._output_images:
            name = image.get_name() 
            
            while True:
                if os.path.isfile(name + self._file_extension): 
                    name += "_I"
                
                else:
                    break

            output_file = name + self._file_extension
            cv2.imwrite(output_file, image.get_image())



def valid_file(file_path):
    if not os.path.isfile(file_path):
        return False

    _, extension = os.path.splitext(file_path)

    if extension not in IMAGE_FORMATS:
        return False

    return True


def isPowerOfFour(number):
    i = log(number) / log(4)
    return i == floor(i)


def valid_output_number(number):
    if number > 256:
        print("Output image number must not exceed 256.")
        return False
    
    if isPowerOfFour(number):
        return True

    print("Output image number must be a 4th power (e.g., 4, 16, 64, 256).")
    return False


def main():
    args = sys.argv
    path = args[1]
    output_number = int(args[2])

    if not valid_output_number(output_number):
        return


    if os.path.isdir(path): 
        content = [os.path.join(path, f) for f in os.listdir(path)]
        to_split = [f for f in content if valid_file(f)]      

        for i, image in enumerate(to_split):
            splitter = ImageSplitter(image, output_number)
            splitter.split_image()
            splitter.save_images()
            print(i+1, "of", len(to_split), "images split.")
            
            

    elif valid_file(path):
        splitter = ImageSplitter(path, output_number)
        splitter.split_image()
        splitter.save_images()
        ("1 image split.")

    else:
        print("Invalid path.")

    
if __name__ == '__main__':
    main()