# -*- coding: utf-8 -*-

import numpy as np
import SimpleITK as sitk
import pywt
import vtk
import edge_detection
import time


def read_dcm2array(path_dcm):
    if path_dcm is None:
        path_dcm = '/Users/potato/Pictures/project_image/head'
    reader = sitk.ImageSeriesReader()
    filenames = reader.GetGDCMSeriesFileNames(path_dcm)
    reader.SetFileNames(filenames)
    img_original = reader.Execute()
    image = sitk.GetArrayFromImage(img_original)  # Z,Y,X
    image_array = np.array(image)
    return image_array


def cw(image_data):
    # CT图像数据重新调整，转换为HU值
    fRescaleSlope = 1.0
    fRescaleIntercept = -1024
    imageU = image_data * fRescaleSlope + fRescaleIntercept

    # 图像调窗
    width = 985.0  # 窗宽
    level = -679.0  # 窗位
    imageCW = imageU
    im_shape = imageU.shape
    lenZ = im_shape[0]
    lenY = im_shape[1]
    lenX = im_shape[2]
    for k in range(lenZ):
        for i in range(lenY):
            for j in range(lenX):
                if imageCW[k, i, j] < level - width / 2.0:
                    imageCW[k, i, j] = 0.0
                else:
                    if imageCW[k, i, j] > level + width / 2.0:
                        imageCW[k, i, j] = 255.0
                    else:
                        imageCW[k, i, j] = (imageU[k, i, j] + width / 2.0 - level) * 255.0 / width
    return imageCW


def wavelet2(image_data):
    db1 = pywt.Wavelet('db1')
    # 多尺度小波变化，返回值分别为[低频分量，(水平高频，垂直高频，对角线高频)]
    [cA2, (cH2, cV2, cD2), (cH1, cV1, cD1)] = pywt.wavedec2(image_data, db1, mode='symmetric', level=2)
    return cA2


def wavelet3(image_data):
    # coeffs = [aaa, (aad, ada, daa, add, dad, dda, ddd), (aad2, ada2, daa2, add2, dad2, dda2, ddd2)]
    coeffs = pywt.wavedecn(image_data, 'db1', level=2)
    return coeffs


def wavelet_cw(image_data):
    [z, y, x] = image_data.shape
    for k in range(z):
        min = np.amin(image_data[k, :, :])
        max = np.amax(image_data[k, :, :])
        for i in range(y):
            for j in range(x):
                image_data[k, i, j] = (image_data[k, i, j] - min) * 255.0 / (max - min)
    return image_data


def image_reduce_dim(image_data):
    [z, y, x] = image_data.shape
    img_reduce = np.zeros([z, y/4, x/4])
    for h in range(y/4):
        for w in range(x/4):
            j = h * 4
            i = w * 4
            tmp = (image_data[:, j, i] + image_data[:, j + 1, i] + image_data[:, j, i + 1] + image_data[:, j + 1, i + 1]) / 4.0
            img_reduce[:, h, w] = tmp
    return img_reduce


def write_txt(image_data):
    [lenZ, lenY, lenX] = image_data.shape
    write_data = list()
    for k in range(lenZ):
        for j in range(lenY):
            for i in range(lenX):
                if image_data[k, j, i] != 0:
                    write_data.append('%-5d%-5d%-5d  %-3d\n' % (i, j, k, 1))
    filepath = '/Users/xiaofang/Desktop/image_data_new.txt'
    with open(filepath, 'w') as f:
        f.write('[(x, y, z), class_index]: 体素三维坐标和所属类别\n')
        f.writelines(write_data)


if __name__ == '__main__':
    # read = read_dcm2array()
    # image_cw = cw(read)
    # coeffs = wavelet3(image_cw)
    # imagedata = coeffs[0]
    # image = sitk.GetImageFromArray(imagedata)
    #
    # # castFilter = sitk.CastImageFilter()
    # # castFilter.SetOutputPixelType(sitk.sitkUInt16)
    # # image = castFilter.Execute(image)
    #
    # test_edge = sitk.CannyEdgeDetection(image)
    # # sitk.Show(image[:, :, 0])
    # sitk.Show(test_edge)

    # path = '/Users/xiaofang/Desktop/Dataset/3D-segmentation/part/p1/'
    # filenames = [path+str(i)+'.jpg' for i in range(206)]
    # reader = sitk.ImageSeriesReader()
    # # filenames = reader.GetGDCMSeriesFileNames(path_dcm)
    # reader.SetFileNames(filenames)
    # img_original = reader.Execute()
    # image = sitk.GetArrayFromImage(img_original)  # Z,Y,X
    # image_array = np.array(image)
    # write_txt(image_array)

    a = time.clock()
    read = read_dcm2array()
    image_cw_bones = cw(read)
    image_edge = edge_detection.edge_detection(image_cw_bones)
    sitk.Show(sitk.GetImageFromArray(image_edge))
    print time.clock() - a



