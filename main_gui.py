# -*- coding:utf-8 -*-
# @Time    : 2018/9/11 上午12:18
# @Author  : Ding Xiao Fang
# @File    : main_gui.py
# @Software: PyCharm

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import sys
import vtk
from PyQt5.QtWidgets import QFileDialog
import threshold_adaptive


class Ui_MainWindow(object):

    def setupUi(self,MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(2560, 1600)
        # 生成组件
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.vtkWidget = QVTKRenderWindowInteractor(self.centralWidget)
        self.btn_select = QtWidgets.QPushButton("选择DICOM目录")
        self.btn_select.clicked.connect(self.btn1_clicked)
        # self.buttonRight = QtWidgets.QPushButton("Right")
        # self.buttonUp = QtWidgets.QPushButton("Up")
        # self.buttonDown = QtWidgets.QPushButton("Down")
        self.checkbox = QtWidgets.QCheckBox()
        # 创建VTK布局
        self.childLayout_vtk = QtWidgets.QGridLayout()
        self.childLayout_vtk.addWidget(self.vtkWidget)

        # 创建区域子布局
        self.childLayout_button = QtWidgets.QVBoxLayout()
        self.childLayout_button.addStretch()
        self.childLayout_button.addWidget(self.btn_select)
        # self.childLayout_button.addWidget(self.buttonRight)
        # self.childLayout_button.addWidget(self.buttonUp)
        # self.childLayout_button.addWidget(self.buttonDown)
        self.childLayout_button.addStretch()
        self.childLayout_button.setSpacing(MainWindow.height()/10)

        # 创建父布局
        MainWindow.setCentralWidget(self.centralWidget)
        self.parentLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.parentLayout.addLayout(self.childLayout_button, 0, 0, 1, 1)
        self.parentLayout.addLayout(self.childLayout_vtk, 0, 2, 1, 3)

    def btn1_clicked(self):
        # filedir = QFileDialog.getExistingDirectory()
        volume = threshold_adaptive.program_start("/Users/potato/Pictures/project_image/head/")
        sv = SimpleView(volume)
        # sv.refresh_iren()



class SimpleView(QtWidgets.QMainWindow):
    def __init__(self, volume, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ren = vtk.vtkRenderer()
        self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.ui.vtkWidget.GetRenderWindow().GetInteractor()

        if volume is not None:
            for i in range(len(volume)):
                self.ren.AddActor(volume[i])
        self.iren.Initialize()
        # ren = vtk.vtkRenderer()
        # ren.AddActor(volume[0])
        # ren.AddActor(volume[1])
        # self.ui.vtkWidget.GetRenderWindow().AddRenderer(ren)
        # self.iren = self.ui.vtkWidget.GetRenderWindow().GetInteractor()

    # def refresh_iren(self,volume):
    #
    #     self.ren = vtk.vtkRenderer()
    #     for i in range(len(volume)):
    #         self.ren.AddActor(volume[i])
        #     self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        # self.iren = self.ui.vtkWidget.GetRenderWindow().GetInteractor()
        # QApplication.processEvents()

# def show_gui(volume):
#     app = QApplication(sys.argv)
#     window = SimpleView(volume)
#     window.show()
#     window.iren.Initialize()
#     sys.exit(app.exec_())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleView(None)
    window.show()
    window.iren.Initialize()
    sys.exit(app.exec_())
