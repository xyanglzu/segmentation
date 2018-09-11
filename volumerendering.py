# -*- coding: utf-8 -*-
import vtk
import SimpleITK as sitk
import os
import main_gui

def show(image_data,index):
    image = sitk.GetImageFromArray(image_data)
    castFilter = sitk.CastImageFilter()
    castFilter.SetOutputPixelType(sitk.sitkUInt8)
    image = castFilter.Execute(image)
    # sitk.Show(image)
    [z, y, x] = image_data.shape
    writerpath = "/Users/potato/Pictures/project_image/seg_image/"+str(index)+"/"  # 分割出来的图像保存路径
    if not os.path.exists(writerpath):
        os.makedirs(writerpath)
    filenames = []
    for i in range(z):
        tmpstr = writerpath + str(i) + '.jpg'
        filenames.append(tmpstr)
    sitk.WriteImage(image, filenames)

    reader = vtk.vtkJPEGReader()
    reader.SetDataExtent(0, x, 0, y, 0, z)
    reader.SetDataScalarTypeToUnsignedShort()
    reader.SetFilePrefix(writerpath)
    reader.SetFilePattern('%s%d.jpg')
    reader.SetFileNameSliceOffset(0)
    reader.SetFileNameSliceSpacing(1)
    reader.SetDataSpacing(1, 1, 1)

    # Create the standard renderer, render window and interactor
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Create transfer mapping scalar value to opacity
    opacityTransferFunction = vtk.vtkPiecewiseFunction()
    opacityTransferFunction.AddSegment(0, 0, 10, 1)

    # Create transfer mapping scalar value to color
    colorTransferFunction = vtk.vtkColorTransferFunction()
    colorTransferFunction.AddRGBPoint(0, 0, 0, 0)
    colorTransferFunction.AddRGBPoint(3, 0, 0.8, 0)
    colorTransferFunction.AddRGBPoint(6, 0, 0, 0.8)
    colorTransferFunction.AddRGBPoint(9, 0.8, 0, 0)
    colorTransferFunction.AddRGBPoint(12, 0.8, 0, 0.8)
    colorTransferFunction.AddRGBPoint(255, 0.8, 0, 0.8)

    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(colorTransferFunction)
    volumeProperty.SetScalarOpacity(opacityTransferFunction)
    volumeProperty.ShadeOn()
    volumeProperty.SetInterpolationTypeToLinear()

    volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
    volumeMapper.SetBlendModeToComposite()
    volumeMapper.SetInputConnection(reader.GetOutputPort())

    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)
    # main_gui.show_gui(volume)
    return volume