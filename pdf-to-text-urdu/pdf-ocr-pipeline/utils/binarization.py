import os
import cv2 as cv
from PIL import Image
import PIL.ImageOps
import numpy as np
import math
import doxapy
from collections import Counter

class ColorRenderer():
    def __init__(self, rgb):
        self.rgb = rgb

    def render(self):
        w, h = 512, 512
        data = np.zeros((h, w, 3), dtype=np.uint8)
        r, g, b = self.rgb
        data[0:512, 0:512] = [r, g, b]
        img = Image.fromarray(data, 'RGB')
        img.show()


class BackgroundColorDetector():
    def __init__(self, imageLoc):
        #         self.img = cv2.imread(imageLoc, 1)
        self.img = imageLoc
        self.manual_count = {}
        self.w, self.h, self.channels = self.img.shape
        self.total_pixels = self.w * self.h

    def count(self):
        for y in range(0, self.h):
            for x in range(0, self.w):
                RGB = (self.img[x, y, 2], self.img[x, y, 1], self.img[x, y, 0])
                if RGB in self.manual_count:
                    self.manual_count[RGB] += 1
                else:
                    self.manual_count[RGB] = 1

    def average_colour(self):
        red = 0
        green = 0
        blue = 0
        sample = 10
        for top in range(0, sample):
            red += self.number_counter[top][0][0]
            green += self.number_counter[top][0][1]
            blue += self.number_counter[top][0][2]

        average_red = red / sample
        average_green = green / sample
        average_blue = blue / sample
        #         print("Average RGB for top ten is: (", average_red,
        #               ", ", average_green, ", ", average_blue, ")")
        return (average_red, average_green, average_blue)

    def twenty_most_common(self):
        self.count()
        self.number_counter = Counter(self.manual_count).most_common(20)

    #         for rgb, value in self.number_counter:
    #             print(rgb, value, ((float(value)/self.total_pixels)*100))

    def detect(self):
        self.twenty_most_common()
        self.percentage_of_first = (
                float(self.number_counter[0][1]) / self.total_pixels)
        #         print(self.percentage_of_first)
        if self.percentage_of_first > 0.5:
            #             print("Background color is ", self.number_counter[0][0])
            return self.number_counter[0][0]
        else:
            return self.average_colour()


def isLightOrDark(rgbColor):
    [r, g, b] = rgbColor
    hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
    if (hsp > 150):  # orignal 127.5
        return 'light'
    else:
        return 'dark'


def back(image):
    # cv_img = cv.imread(path)
    BackgroundColor = BackgroundColorDetector(image)
    average_color = BackgroundColor.detect()
    return isLightOrDark(average_color)


def get_gray_image(image):
    background = back(image)
    
    if background == 'dark':
        # print(background)
        # image = Image.open(image_path)
        image = Image.fromarray(image)
        inverted_image = PIL.ImageOps.invert(image)
        cv_img = np.array(inverted_image).astype('uint8')
        gray = cv.cvtColor(cv_img, cv.COLOR_BGR2GRAY)
    else:
        # print(background)
        # cv_img = cv.imread(image_path)
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    return gray


class stack:
    def __init__(self):
        self.array = list()

    def push(self, value):
        self.array.append(value)

    def pop(self):
        return self.array.pop()

    def is_empty(self):
        if len(self.array) == 0:
            return True
        else:
            return False


def connected_components(image):
    X = [0, -1, -1, -1, 0, 1, 1, 1]
    Y = [1, 1, 0, -1, -1, -1, 0, 1]
    pass_flag = True
    obj = stack()
    final_point_array = list()
    i = 0
    j = 0
    count = 0
    limit = image.shape[0] / 1
    while i < image.shape[0]:
        #         print(i)
        while j < image.shape[1]:
            flag = True
            pass_flag = True
            point_array = list()
            m = int()
            n = int()
            if image[i][j] == 1:
                obj.push((i, j))
                while flag:
                    center_pixel = obj.pop()
                    n = center_pixel[0]
                    m = center_pixel[1]
                    if image[n][m] == 1:
                        point_array.append(center_pixel)
                        image[n][m] = 3
                    for k in range(len(X)):
                        row = n + X[k]
                        column = m + Y[k]
                        if row < 0 or column < 0 or row >= image.shape[0] or column >= image.shape[1]:
                            pass
                        else:
                            if image[row][column] == 1:
                                center_pixel = obj.push((row, column))
                            elif obj.is_empty():
                                #                                 print(count)
                                #                                 i=0
                                #                                 j=0
                                pass_flag = False
                                flag = False
                final_point_array.append(point_array)
            else:
                if pass_flag:
                    j += 1
        if pass_flag:
            if i >= limit:
                break
            i += 1
            j = 0
    return len(final_point_array)


def convert_binary(image):
    if len(image.shape) == 3:
        gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    elif len(image.shape) < 3:
        gray_image = image
    (thresh, gray_image) = cv.threshold(gray_image, 195, 255, cv.THRESH_BINARY)
    gray_image[gray_image == 0] = 1  # black pixels set to 1
    gray_image[gray_image == 255] = 0  # white pixels set to 0
    #     gray_image[gray_image == 1] = 255
    return gray_image
