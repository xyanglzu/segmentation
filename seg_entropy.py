# -*- coding: utf-8 -*-

import numpy as np
import point_and_seed as ps


def growing(image_data, seed, grow_mark_all):
    seed_extract = np.array(seed.seed_zyx)
    lower_extract = seed.lower
    upper_extract = seed.upper
    seed_index = seed.index
    seed_growing = list()
    for i in range(seed_extract.shape[0]):            # 添加需要分割区域的种子点，可以添加多个
        seed_growing.append(ps.Point(seed_extract[i, 0], seed_extract[i, 1], seed_extract[i, 2]))
    grow_dir = [ps.Point(0, -1, 0), ps.Point(0, 1, 0),
                ps.Point(-1, 0, 0), ps.Point(1, 0, 0),
                ps.Point(0, 0, -1), ps.Point(0, 0, 1)]
    [lenZ, lenY, lenX] = image_data.shape
    image_mark = np.zeros([lenZ, lenY, lenX])         # 标记种子是否已经生长
    image_return = np.zeros([lenZ, lenY, lenX])       # 创建返回图像数组
    # 生长一个区域
    while len(seed_growing) > 0:
        seed_tmp = seed_growing[0]
        # 将以生长的点从一个类的种子点列表中删除
        seed_growing.pop(0)
        image_mark[seed_tmp.z, seed_tmp.y, seed_tmp.x] = seed_index
        # 遍历6邻域
        for i in range(6):
            tmpZ = seed_tmp.z + grow_dir[i].z
            tmpY = seed_tmp.y + grow_dir[i].y
            tmpX = seed_tmp.x + grow_dir[i].x
            if tmpZ < 0 or tmpX < 0 or tmpY < 0 or tmpZ >= lenZ or tmpX >= lenX or tmpY >= lenY:
                continue
            # 在种子集合中满足条件的点进行生长
            # 取3*3*3的超体素平均值进行生长计算
            else:
                avg = cal_avg(image_data, tmpZ, tmpY, tmpX)
            if upper_extract >= avg >= lower_extract and image_mark[tmpZ, tmpY, tmpX] == 0 and grow_mark_all[tmpZ, tmpY, tmpX]== 0:
                image_return[tmpZ, tmpY, tmpX] = image_data[tmpZ, tmpY, tmpX]
                image_mark[tmpZ, tmpY, tmpX] = seed_index
                grow_mark_all[tmpZ, tmpY, tmpX] = seed_index
                seed_growing.append(ps.Point(tmpZ, tmpY, tmpX))
    return image_mark


def cal_avg(image_data, z, y, x):  # 计算超体素像素值
    [lenZ, lenY, lenX] = image_data.shape
    if z == 0 or y == 0 or x == 0 or z == lenZ - 1 or y == lenY - 1 or x == lenX - 1:
        avg = image_data[z, y, x]
    else:
        avg = (image_data[z-1, y-1, x-1] + image_data[z-1, y-1, x] + image_data[z-1, y-1, x+1] +
               image_data[z-1, y, x-1] + image_data[z-1, y, x] + image_data[z-1, y, x+1] +
               image_data[z-1, y+1, x-1] + image_data[z-1, y+1, x] + image_data[z-1, y+1, x+1] +
               image_data[z, y-1, x-1] + image_data[z, y-1, x] + image_data[z, y-1, x+1] +
               image_data[z, y, x-1] + image_data[z, y, x] + image_data[z, y, x+1] +
               image_data[z, y+1, x-1] + image_data[z, y+1, x] + image_data[z, y+1, x+1] +
               image_data[z+1, y-1, x-1] + image_data[z+1, y-1, x] + image_data[z+1, y-1, x+1] +
               image_data[z+1, y, x-1] + image_data[z+1, y, x] + image_data[z+1, y, x+1] +
               image_data[z+1, y+1, x-1] + image_data[z+1, y+1, x] + image_data[z+1, y+1, x+1]
               )/27.0
    return avg


def cal_entropy(sum, dic, point):
    return True


