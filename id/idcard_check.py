# coding=UTF-8

import cv2
import imutils
from imutils import contours
from pylab import *
import numpy as np
from scipy import ndimage


def show_resault(imgs, num):
    """
    matplotlib显示图片集
    :param imgs:  图片集
    :param num:
    :return:
    """

    n = 1
    sqr = math.ceil(math.sqrt(num))
    for b, i in imgs:
        i = cv2.cvtColor(i, cv2.COLOR_RGB2BGR)
        subplot(sqr, sqr, n)
        imshow(i)
        title(b)
        axis('off')
        n += 1
        if n > num:
            break

    show()


def sobel_make(image):
    x = cv2.Sobel(image, cv2.CV_16S, 1, 0)
    y = cv2.Sobel(image, cv2.CV_16S, 0, 1)
    # 转回 utf-8
    abs_x = cv2.convertScaleAbs(x)
    abs_y = cv2.convertScaleAbs(y)
    dst = cv2.addWeighted(abs_x, 0.5, abs_y, 0.5)

    return dst


def contour_check(image):
    """
    判断轮廓是否完整
    :param image:
    :return:
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 灰

    binary = cv2.GaussianBlur(gray, (3, 3), 0)  # 高斯

    edged = cv2.Canny(binary, 50, 150)  # canny轮廓

    cnt = cv2.findContours(edged.copy(), cv2.RETR_EXTERNALR, cv2.CHAIN_APPROX_SIMPLE)
    cnt = imutils.grab_contours(cnt)
    (cnt, _) = contours.sort_contours(cnt)

    w, h, _ = image.shape

    for i, c in enumerate(cnt):
        if cv2.contourArea(c) < w * h / 2:
            continue
        cv2.drawContours(image, c, -1, (255, 0, 0), 3)

        return True, image

    return False, image


def light_check(image):
    """
    thershold: 容许高光的最大面积比
    :param image:
    :return:
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = cv2.GaussianBlur(gray, (3, 3), 0)
    medianb = cv2.medianBlur(binary, 5)

    _, th = cv2.threshold(medianb, 240, 255, cv2.THRESH_BINARY)

    cnt = cv2.findContours(th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = imutils.grab_contours(cnt)
    (cnt, _) = contours.sort_contours(cnt)

    w, h, _ = image.shape

    threshold = 1/16

    for i, c in enumerate(cnt):
        if cv2.contourArea(c) > w * h * threshold:
            cv2.drawContours(image, c, -1, (255, 0, 0))
            return False, image
    return True, image


def quality_check(image):
    """
    threshold: 清晰度阀值
    :param image:
    :return:
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_resize = cv2.resize(gray, (640, 480))

    gray_var = cv2.Laplacian(img_resize, cv2.CV_64F).var()

    threshold = 100

    if gray_var > threshold:
        return True, image
    else:
        return False, image


def tilt_check(image):
    """
    angle_threshold 判断是否倾斜的角度
    :param image:
    :return:
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLines(edges, 1.0, np.pi/180, 0)

    angle = 0
    angle_threshold = 15

    for rho, theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * a)
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * a)
        if x1 == x2 or y1 == y2:
            continue
        t = float(y2 - y1) / (x2 - x1)
        angle = math.degrees(math.atan(t))

        if angle > 45:
            angle = -90 + angle
        elif angle < -45:
            angle = 90 + angle

    if angle > angle_threshold:
        return False, image
    elif angle <= angle_threshold:
        return True, image


if __name__ == '__main__':
    path = '../im/idcard/22222222.jpg'
    img = cv2.imread(path)
    bool_check, image = tilt_check(img)
