#ccding=UTF-8

from pylab import *
import os
import cv2
import idcard_check


def test_contour(dir):
    """
    轮廓
    :param dir:
    :return:
    """
    file_list = os.listdir(dir)
    imgs = []
    for file_name in file_list:
        img = cv2.imread(dir + '/' + file_name)
        bool_check, image = idcard_check.contour_check(img)
        imgs.append([str(bool_check, image)])

    idcard_check.show_resault(imgs, len(imgs))


def test_quality(dir):
    """
    检测图片质量
    :param dir:
    :return:
    """

    file_list = os.listdir(dir)
    imgs_sharp = []
    imgs_unsharp = []
    for file_name in file_list:
        img = cv2.imread(dir + '/' + file_name)
        bool_check, v, image = idcard_check.quality_check(img)
        if bool_check:
            print(file_name + '(pass):' + str(v))
            imgs_sharp.append([str(bool_check, image)])
        elif not bool_check:
            print(file_name + '(deny):' + str(v))
            imgs_unsharp.append([str(bool_check, image)])

    idcard_check.show_resault(imgs_sharp, len(imgs_sharp))
    idcard_check.show_resault(imgs_unsharp, len(imgs_unsharp))


def test_tilt(path):
    """
    检测倾斜
    :param path:
    :return:
    """

    file_list = os.listdir(path)
    imgs = []
    for file_name in file_list:
        img = cv2.imread(path + '/' + file_name)
        bool_check, image = idcard_check.tilt_check(img)
        imgs.append([str(bool_check, image)])

    idcard_check.show_resault(imgs, len(imgs))


if __name__ == '__main__':
    path = '../img/newid_unsharp'
    test_quality(path)
