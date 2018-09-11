# -*- coding:utf-8 -*-
# @Time    : 2018/9/11 下午2:57
# @Author  : Ding Xiao Fang
# @File    : show2D.py
# @Software: PyCharm
import vtk
import preprocess as pre
import SimpleITK as sitk
import os


def show_image2(im_data):
    image = sitk.GetImageFromArray(im_data)
    
    castFilter = sitk.CastImageFilter()
    castFilter.SetOutputPixelType(sitk.sitkUInt8)
    image = castFilter.Execute(image)
    # sitk.Show(image)
    [z, y, x] = im_data.shape
    writerpath = '/Users/potato/Pictures/project_image/tmp/'  # 分割出来的图像保存路径
    filenames = []
    for i in range(z):
        tmpstr = writerpath + str(i) + '.jpg'
        filenames.append(tmpstr)
    sitk.WriteImage(image, filenames)
    reader = vtk.vtkJPEGReader()
    reader.SetFileName(filenames[0])
    reader.SetDataExtent(0, x, 0, y, 0, z)
    reader.SetDataScalarTypeToUnsignedInt()
    reader.SetFilePrefix(writerpath)
    reader.SetFilePattern('%s%d.jpg')
    reader.SetFileNameSliceOffset(0)
    reader.SetFileNameSliceSpacing(1)
    reader.SetDataSpacing(1, 1, 1)
    #
    # reader = vtk.vtkDICOMImageReader()
    # reader.SetFileName("/Users/potato/Pictures/project_image/head/ser003img00001.dcm")
    imageViewer = vtk.vtkImageViewer2()
    imageViewer.SetInputConnection(reader.GetOutputPort())
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    imageViewer.SetupInteractor(renderWindowInteractor)
    # imageViewer.SetColorLevel(50)
    # imageViewer.SetColorWindow(90)
    imageViewer.SetSlice(40)
    imageViewer.SetSliceOrientationToXY()
    imageViewer.Render()
    imageViewer.Render()
    imageViewer.GetRenderer().ResetCamera()
    imageViewer.Render()
    renderWindowInteractor.Start()


if __name__=="__main__":
    image_read = pre.read_dcm2array("/Users/potato/Pictures/project_image/head")
    show_image2(image_read)