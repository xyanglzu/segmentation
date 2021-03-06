# -*- coding: utf-8 -*-

import numpy as np
from scipy.signal import argrelextrema
import random
import preprocess
import point_and_seed as ps
import seg_entropy as seg
import volumerendering
from matplotlib import pyplot as plt
import pandas as pd
from scipy.interpolate import griddata
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import main_gui

def surface_fiting(image_data):

    [lenZ, lenY, lenX] = image_data.shape
    x = list()
    y = list()
    z = list()
    for k in range(lenZ):
        for j in range(lenY):
            for i in range(lenX):
                if image_data[k, j, i] != 0:
                    x.append(i)
                    y.append(j)
                    z.append(k)
    xyz = {'x': x, 'y': y, 'z': z}
    # put the data into a pandas DataFrame (this is what my data looks like)
    df = pd.DataFrame(xyz, index=range(len(xyz['x'])))

    # re-create the 2D-arrays
    x1 = np.linspace(df['x'].min(), df['x'].max(), len(df['x'].unique()))
    y1 = np.linspace(df['y'].min(), df['y'].max(), len(df['y'].unique()))
    x2, y2 = np.meshgrid(x1, y1)
    z2 = griddata((df['x'], df['y']), df['z'], (x2, y2), method='cubic')
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(x2, y2, z2, cmap=cm.coolwarm)
    ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


def hist(image_data):
    [z, y, x] = image_data.shape
    # 创建直方图统计字典
    d = dict()
    for d_i in range(256):
        d[d_i] = list()
    for k in range(z):
        for j in range(y):
            for i in range(x):
                if image_data[k, j, i] != 0:
                    tmp = np.floor(image_data[k, j, i] + 0.5)
                    d[tmp].append([k, j, i])
    return d


def wavelet_hist(image_data):
    [z, y, x] = image_data.shape
    # 创建直方图统计字典
    d = dict()
    for d_i in range(256):
        d[d_i] = list()
    for k in range(z):
        for j in range(y):
            for i in range(x):
                if image_data[k, j, i] != 0:
                # if 100 < image_data[k, j, i] < 256:
                    tmp = np.floor(image_data[k, j, i] + 0.5)
                    d[tmp].append([k, j, i])
    return d


def ployfit(x, y):
    """ 2. 根据样本值拟合多项式系数
    np.polyfit(x_data, y_data, p) 根据 x, y数据和阶数p返回拟合的多项式系数列表
    """
    a10 = np.polyfit(x, y, 30)  # 10阶拟合，即x最高次方系数是10
    p10 = np.poly1d(a10)
    # 画图验证
    xp = np.linspace(0,256,256)
    plt.plot(x, y, ".")  # 点是原数据
    plt.plot(xp, p10(xp), "r--")  # 红线是10阶拟合
    plt.show()



def seed_extract(dic):
    seed_list = list()
    count_array = np.zeros(256)

    for i in range(256):
        count_array[i] = len(dic[i])

    # 直方图局部最小值所处的像素值
    less_extrema = np.array([])
    less_extrema = np.append(less_extrema, np.array(argrelextrema(count_array[0:140], np.less, order=6)))
    less_extrema = np.append(less_extrema, np.array(argrelextrema(count_array[140:180], np.less, order=4)) + 140)
    less_extrema = np.append(less_extrema, np.array(argrelextrema(count_array[180:], np.less, order=6)) + 180)
    # 直方图局部最大值所处的像素值
    greater_extrema = np.array([])
    greater_extrema = np.append(greater_extrema, np.array(argrelextrema(count_array[0:140], np.greater, order=5)))
    # greater_extrema = np.append(greater_extrema, np.array(argrelextrema(count_array[70:140], np.greater, order=3)) + 70)
    greater_extrema = np.append(greater_extrema, np.array(argrelextrema(count_array[140:], np.greater, order=3)) + 140)
    ##################################

    # plt.figure("hist")
    # for i in range(256):
    #     plt.bar(i, len(d[i]), fc='b')
    # # print less_extrema
    # for i in range(len(less_extrema)):
    #     plt.plot(less_extrema[i], len(dic[less_extrema[i]]), 'r.')
    # for i in range(len(greater_extrema)):
    #     plt.plot(greater_extrema[i], len(dic[greater_extrema[i]]), 'g.')
    # # plt.plot(greater_extrema, greater_result, 'g.')
    # plt.show()

    ##################################
    index = 0
    last_seed_lower = 0
    for j in range(greater_extrema.size):
        for i in range(less_extrema.size-1):
            if greater_extrema[j] < less_extrema[i]:
                break
            if less_extrema[i] < greater_extrema[j] < less_extrema[i+1]:
                index += 1
                seed_total = np.array(dic[greater_extrema[j]])
                seed_zyx = np.array(random.sample(seed_total, 3))
                if len(seed_list) == 0:
                    seed_list.append(ps.Seed(seed_zyx, less_extrema[i], less_extrema[i+1], index))
                    last_seed_lower = less_extrema[i]
                elif last_seed_lower != less_extrema[i]:
                    seed_list.append(ps.Seed(seed_zyx, less_extrema[i], less_extrema[i+1], index))
                    last_seed_lower = less_extrema[i]
                continue
    return seed_list



def threshold():
    pass


def program_start(file_dir):
    read = preprocess.read_dcm2array(file_dir)
    image_cw = preprocess.cw(read)
    coeffs = preprocess.wavelet3(image_cw)

    # image_edge = edge.edge_detection(coeffs)

    # preprocess.write_txt(image_edge)
    # volumerendering.show(image_edge)
    # image_show = sitk.GetImageFromArray(image_edge)
    # sitk.Show(image_show)

    image_reduce = preprocess.wavelet_cw(coeffs[0])
    d = wavelet_hist(image_reduce)
    # # d = hist(image_cw)
    volume = []
    seed_tmp = seed_extract(d)
    grow_mark_all = np.zeros(image_reduce.shape)
    for i in range(len(seed_tmp)):
        seed_list_tmp = seed_tmp[i]
        # print seed_list_tmp.seed_zyx, seed_list_tmp.lower, seed_list_tmp.upper
        image_grow = seg.growing(image_reduce, seed_list_tmp,grow_mark_all)
        volume .append(volumerendering.show(image_grow,i))
    return volume
    # main_gui.show_gui(volume)


if __name__ == '__main__':
    program_start("/Users/potato/Pictures/project_image/head/")

