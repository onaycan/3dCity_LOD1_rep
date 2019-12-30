
import os
import sys
import pprint
import time
import pandas
import shutil
import datetime
from PyQt5.QtWidgets import QTreeWidgetItem, QColorDialog, QFileDialog, QTabWidget
from PyQt5.QtCore import Qt as qut
from PyQt5 import QtWidgets, uic
from PyQt5 import Qt, QtCore, QtGui
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from PyQt5.QtCore import QUrl, QObject, pyqtSlot
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtGui import QPainter
import sys
import cities
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
import vtk_interaction
import numpy
from petl import fromcsv, look, cut, tocsv, fromtext
import petl
from astropy.io import ascii


import Ui_main



#warnings.filterwarnings("ignore")



class OutLog:
    def __init__(self, edit, out=None, color=None):

        self.edit = edit
        self.out = None
        self.color = color

    def write(self, m):
        if self.color:
            tc = self.edit.textColor()
            self.edit.setTextColor(self.color)

        self.edit.moveCursor(QtGui.QTextCursor.End)
        self.edit.insertPlainText( m )

        if self.color:
            self.edit.setTextColor(tc)

        if self.out:
            self.out.write(m)


def set_app_style(_app):
    _app.setStyle("Fusion")
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53,53,53))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15,15,15))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53,53,53))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53,53,53))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)



    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Window, QtCore.Qt.gray)
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtCore.Qt.gray)
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Base, QtCore.Qt.gray)
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, QtCore.Qt.gray)
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, QtCore.Qt.gray)
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, QtCore.Qt.gray)
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtCore.Qt.gray)
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Button, QtCore.Qt.gray)
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, QtCore.Qt.gray)
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, QtCore.Qt.gray)


    palette.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Button, QtGui.QColor(53,53,53))
    
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142,45,197).lighter())
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)   
    _app.setPalette(palette)


if __name__=='__main__':

    

    app = QtWidgets.QApplication(sys.argv)
    screen_rect = app.desktop().screenGeometry()
    width, height = screen_rect.width(), screen_rect.height()
    set_app_style(app)
    
    window = Ui_main.Ui(width,height)


    #START PREPROCESSING TAB 
    window.show_table_widget()
    pre_frame = window.preFrame
    window.prevtkWidget = QVTKRenderWindowInteractor(pre_frame)
    pre_eq_city=cities.city("caferaga","pre-eq",window.prevtkWidget,"map_kadiköy_caferaga_small.osm","map_kadiköy_caferaga.json")
    pre_eq_city.build_city()
    pre_eq_city.set_interactor()
    window.pre_eq_city=pre_eq_city
    window.setup_Ui_preproc()
    pre_eq_city.vtk_interactor.style = vtk_interaction.MouseInteractorHighLightActor(pre_eq_city.vtk_interactor, window)
    pre_eq_city.vtk_interactor.style.SetDefaultRenderer(pre_eq_city.vtk_interactor.ren)
    pre_eq_city.vtk_interactor.iren.SetInteractorStyle(pre_eq_city.vtk_interactor.style)
    pre_eq_city.vtk_interactor.visualize(_initial=True)
    pre_eq_city.vtk_interactor.renWin.Render()
    print("render window is rendered")
    pre_eq_city.vtk_interactor.iren.Initialize()
    pre_eq_city.vtk_interactor.iren.Start()
    #END PREPROCESSING TAB


    #START EQ MAP
    window.setup_Ui_eqmap()
    #END EQ MAP

    
    #START PROCESSING TAB
    post_frame = window.postFrame
    vpl=window.postvtkLayout
    postvtkWidget = QVTKRenderWindowInteractor(post_frame)
    vpl.addWidget(postvtkWidget)
    post_eq_city=cities.city("caferaga","post-eq",postvtkWidget,"map_kadiköy_caferaga_small.osm","map_kadiköy_caferaga.json")
    post_eq_city.copy_city(pre_eq_city)
    post_eq_city.set_interactor()
    window.post_eq_city=post_eq_city
    post_eq_city.vtk_interactor.iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
    post_eq_city.vtk_interactor.visualize(_initial=True)
    post_eq_city.vtk_interactor.renWin.Render()
    print("render window is rendered")
    post_eq_city.vtk_interactor.iren.Initialize()
    post_eq_city.vtk_interactor.iren.Start()
    window.setup_Ui_proc()
    #END PROCESSING TAB



    #edit=window.textEdit_Log
    #sys.stdout = OutLog( edit, sys.stdout)

    errOut = vtk.vtkFileOutputWindow()
    errOut.SetFileName("VTK Error Out.txt")



     
    

    


    
    


    sys.exit(app.exec_())
    #app.quit()
    
    
    
    



