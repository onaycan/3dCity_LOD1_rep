
import os
import sys
import pprint
import time
import pandas
import shutil
import datetime
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTreeWidgetItem, QColorDialog, QFileDialog, QTabWidget
from PyQt5 import Qt, QtCore, QtGui
from PyQt5.QtCore import Qt as qut
from PyQt5.QtCore import QTimer
from PyQt5 import QtTest
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from PyQt5.QtCore import QUrl, QObject, pyqtSlot
from PyQt5.QtWebChannel import QWebChannel
import matplotlib
import sys
import cities
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
import vtk_interaction
import numpy
import csv
from petl import fromcsv, look, cut, tocsv, fromtext
import petl
from astropy.io import ascii

from gui_designer.ideas4all_city_simulator_gui import Ui_MainWindow
import Ui_main


class CallHandler(QObject):

    def setmainWidget(self, mainWidget):
        self.mainWidget = mainWidget


class WebView(QWebView):

    def config(self, mainWidget, filename):
        QWebView.__init__(self)
        #self.initialize()

        #self.channel = QWebChannel()
        ##self.handler = CallHandler()
        ##self.handler.setmainWidget(mainWidget)
        ##self.channel.registerObject('handler', self.handler)
        #self.page().setWebChannel(self.channel)
        ##local_url = QUrl.fromLocalFile(filename)
        local_url=QUrl(filename)
        self.load(local_url)
        ##self.show()
    

class CheckableComboBox(QtWidgets.QComboBox):
    def __init__(self):    
        super(CheckableComboBox, self).__init__()
 

    def addItem(self, item):
        if item not in self.get_set_items():
            super(CheckableComboBox, self).addItem(item)

    def addItems(self, items):
        items = list(self.get_set_items() | set(items))
        super(CheckableComboBox, self).addItems(items)

    def get_set_items(self):
        return set([self.itemText(i) for i in range(1,self.count())])

    def flags(self):
        return Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled

class ColorButton(QtWidgets.QPushButton):
    def __init__(self,_city_vtk, _objects_key, _buildings, _checked_items):
        super().__init__()
        self.setText('')
        self.city_vtk=_city_vtk
        self.objects_key=_objects_key
        self.buildings=_buildings
        self.checked_items=_checked_items

    def on_click(self):

        
        color = QColorDialog.getColor()
        #print(color.getRgb())
        self.setStyleSheet("background:rgb("+str(color.getRgb()[0])+","+str(color.getRgb()[1])+","+str(color.getRgb()[2])+")")
        current_color=[color.getRgb()[0],color.getRgb()[1],color.getRgb()[2]]
        self.city_vtk.LineColorLabels[self.objects_key]=current_color
        self.city_vtk.LineColors = vtk.vtkUnsignedCharArray()
        self.city_vtk.LineColors.SetNumberOfComponents(3)
        self.city_vtk.LineColors.SetName("LineColors")
        
        self.city_vtk.BuildingColorLabels[self.objects_key]=current_color
        self.city_vtk.BuildingCellColors = vtk.vtkUnsignedCharArray()
        self.city_vtk.BuildingCellColors.SetNumberOfComponents(3)
        self.city_vtk.BuildingCellColors.SetName("BuildingCellColors")
        
        self.city_vtk.insert_buildings(self.buildings,self.checked_items, _only_colors=True)
        
        self.city_vtk.PolyData_Lines = vtk.vtkPolyData()
        self.city_vtk.PolyData_BuildingCells = vtk.vtkPolyData()
        self.city_vtk.visualize()
        #self.city_vtk.mapper_BuildingCells.ScalarVisibilityOn()
        self.city_vtk.renWin.Render()
       



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
    # start application of dark theme
    set_app_style(app)
    # end application of dark theme
    
    window = Ui_main.Ui()
    window.showMaximized()
    window.show_table_widget()

    

    frame = window.tabWidget

    vl=window.vtkLayout
    vtkWidget = QVTKRenderWindowInteractor(frame)
    vl.addWidget(vtkWidget)

    window.manage_simparams()

    
    pre_eq_city=cities.city("caferaga","pre-eq",vtkWidget,"map_kadiköy_caferaga_small.osm","map_kadiköy_caferaga.json")
    pre_eq_city.build_city()
    pre_eq_city.set_interactor()
    
    window.show_tree_widget(pre_eq_city)
    
    window.EnableSelection_checkBox.stateChanged.connect(window.manage_selection_enablebox)
    #window.buildings_pushbutton.clicked.connect(window.manage_selection_box_b)
    window.all_pushbutton.clicked.connect(window.manage_selection_box_all)
    window.buildingBlocks_pushbutton.clicked.connect(window.manage_selection_box_bb)
    window.append_pushbutton.clicked.connect(window.fill_table_widget)
    window.configure_simulation_pushbutton.clicked.connect(window.configure_simulation)

    pre_eq_city.vtk_interactor.style = vtk_interaction.MouseInteractorHighLightActor(pre_eq_city.vtk_interactor, window)
    pre_eq_city.vtk_interactor.style.SetDefaultRenderer(pre_eq_city.vtk_interactor.ren)
    pre_eq_city.vtk_interactor.iren.SetInteractorStyle(pre_eq_city.vtk_interactor.style)
    pre_eq_city.vtk_interactor.visualize(_initial=True)
    pre_eq_city.vtk_interactor.renWin.Render()
    print("render window is rendered")
    pre_eq_city.vtk_interactor.iren.Initialize()
    pre_eq_city.vtk_interactor.iren.Start()
    



    # start postwindow
    post_frame = window.Postprocessing_tabwidget
    vpl=window.vtkPostLayout
    postvtkWidget = QVTKRenderWindowInteractor(post_frame)
    vpl.addWidget(postvtkWidget)
    post_eq_city=cities.city("caferaga","post-eq",postvtkWidget,"map_kadiköy_caferaga_small.osm","map_kadiköy_caferaga.json")
    post_eq_city.copy_city(pre_eq_city)
    post_eq_city.set_interactor()
    #post_eq_city.copy_city_interactor_properties(pre_eq_city)
    window.post_eq_city=post_eq_city
    post_eq_city.vtk_interactor.iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
    post_eq_city.vtk_interactor.visualize(_initial=True)
    post_eq_city.vtk_interactor.renWin.Render()
    print("render window is rendered")
    post_eq_city.vtk_interactor.iren.Initialize()
    post_eq_city.vtk_interactor.iren.Start()


    errOut = vtk.vtkFileOutputWindow()
    errOut.SetFileName("VTK Error Out.txt")
    #vtkStdErrOut = vtk.vtkOutputWindow()
    #vtkStdErrOut.SetInstance(errOut)

    


    window.runorloadcheckBox.stateChanged.connect(window.manage_runorload)
    window.showresults_pushButton.clicked.connect(window.show_results)
    window.run_pushButton.clicked.connect(window.runsimulation)
    window.tensorresult_comboBox.addItem("Displacement")        
    window.tensorresult_comboBox.addItem("Stress")
    window.tensorresult_comboBox.addItem("Strain")
    window.tensorresult_comboBox.setCurrentText("Displacement")
    window.set_combobox_post_legend("Displacement")
    window.scalarresult_comboBox.setCurrentText("Displacement Mag")
    window.tensorresult_comboBox.currentTextChanged.connect(window.set_combobox_post_legend)
    window.scalarresult_comboBox.currentTextChanged.connect(window.set_scalar_result)
    window.legend_table=QtWidgets.QTableWidget()
    window.legend_layout.addWidget(window.legend_table)
    
        


    #mapwidget = WebView()
    #mapwidget.config(window,"https://www.google.com/")
    ##mapwidget.config(window, os.path.abspath(".\\LeafLetOffline\\plot_robust.html"))
    ##window.Postprocessing_tabwidget.setTabsClosable(True)
    ##window.Postprocessing_tabwidget.setMovable(True)
    ##window.Postprocessing_tabwidget.setStyleSheet("QTabBar::tab:selected { color: blue; }")
    ##window.Postprocessing_tabwidget.addTab(mapwidget, "yarro")
    #window.horizontalLayout_2.addWidget(mapwidget)


    

    #window.webTabwidget = QTabWidget()
    #window.webTabwidget.setTabsClosable(True)
    #window.webTabwidget.setMovable(True)
    #window.webTabwidget.addTab(mapwidget, "seismic map")
    #window.preeq_post_tabwidget.addTab(mapwidget, "yarro")
    
    







    #edit=window.textEdit_Log
    #sys.stdout = OutLog( edit, sys.stdout)
    


    sys.exit(app.exec_())
    #app.quit()
    
    
    
    



