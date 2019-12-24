
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size
#import matplotlib

from PyQt5 import QtWidgets, uic, QtGui, QtCore
import csv
import numpy 
import pprint
from numpy import genfromtxt
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


    

class MapCanvas(FigureCanvas):
    def __init__(self, parent=None, width=8, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        
        
        self.axes = self.fig.add_subplot(111)
        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.geomap = Basemap(llcrnrlon=25.979530,llcrnrlat=40.015137,urcrnrlon=31.979530,urcrnrlat=42.015137,
             resolution='h', projection='cass', lat_0 = 41.015137, lon_0 = 28.979530, ax=self.axes, epsg=3857)#5520
        #self.geomap.drawmapboundary(fill_color='aqua')
        #self.geomap.fillcontinents(color='#ddaa66',lake_color='aqua')
        self.geomap.drawcoastlines()
        self.geomap.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 1500, verbose= True)
        #self.geomap.etopo()        

        self.fig.tight_layout()
        self.axes.autoscale(enable=True,axis='both',tight=True)
        self.fig.tight_layout()
        self.nav_widget=NavigationToolbar(self,parent)
        self.set_nav_palette()
        parent.verticalLayout_4.addWidget(self.nav_widget)

    def set_nav_palette(self):

        palette = self.nav_widget.palette()
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255,165,0))
        palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(255,165,0))
        palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(255,165,0))
        palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(255,165,0))
        palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Window, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Base, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Button, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, QtCore.Qt.white)
        self.nav_widget.setPalette(palette)

def set_mapcanvas(self):
    self.mapcanvas = MapCanvas(self, width=4, height=4, dpi=100)
    self.verticalLayout_4.addWidget(self.mapcanvas)

def config_eq_locs(self):

    self.additionals=False
    self.annots=[]
    
    eqsfilename=".\\eq_db\\query_eqs_2005_2019.csv"
    
    eqsdata=pd.read_csv(eqsfilename, delimiter=';').to_dict()

    
    size_scale=10
    lons=list(eqsdata['longitude'].values())
    lats=list(eqsdata['latitude'].values())
    mags_s=[float(v)*size_scale for v in eqsdata['mag'].values()]
    mags=[float(v) for v in eqsdata['mag'].values()]
    #cm = matplotlib.cm.get_cmap('viridis')
    x, y = self.mapcanvas.geomap(lons, lats)
    sc=self.mapcanvas.geomap.scatter(x, y, marker="o", s=mags_s, alpha=0.9, cmap='Oranges', c=mags)


    
    divider = make_axes_locatable(self.mapcanvas.axes)
    cax = divider.append_axes('right', size='5%', pad=0.15)
    cbar=self.mapcanvas.fig.colorbar(sc,cax=cax)
    cbar.set_label('Earthquaqe Magnitude', rotation=270,horizontalalignment='center', labelpad=10)

    times=[datetime.strptime((v.split("T")[0]+" "+v.split("T")[1].split(".")[0]), '%Y-%m-%d %H:%M:%S') for v in eqsdata['time'].values()]
    
    min_date=str(min(times))
    minqdate = QtCore.QDateTime.fromString(min_date, 'yyyy-M-d hh:mm:ss')
    self.dateTimeEdit.setDateTime(minqdate)

    max_date=str(max(times))
    maxqdate = QtCore.QDateTime.fromString(max_date, 'yyyy-M-d hh:mm:ss')
    self.dateTimeEdit_2.setDateTime(maxqdate)

    self.tableWidget_2.setColumnCount(4)
    self.tableWidget_2.setRowCount(len(times))
    self.tableWidget_2.show()
    self.tableWidget_2.setHorizontalHeaderLabels(["DateTime","Mag.","Lat.","Log"])


    #self.checkboxes={}    
    for j in range(len(times)):
        #self.checkboxes[j]=QtWidgets.QCheckBox()
        #self.checkboxes[j].setCheckState(False)
        #self.tableWidget_2.setCellWidget(j, 0, self.checkboxes[j])
        self.tableWidget_2.setItem(j, 0, QtWidgets.QTableWidgetItem(str(times[j])))
        self.tableWidget_2.setItem(j, 1, QtWidgets.QTableWidgetItem(str(mags[j])))
        self.tableWidget_2.setItem(j, 2, QtWidgets.QTableWidgetItem(str(lats[j])))
        self.tableWidget_2.setItem(j, 3, QtWidgets.QTableWidgetItem(str(lons[j])))



    self.tableWidget_2.setSortingEnabled(True)
    self.tableWidget_2.itemSelectionChanged.connect(self.selection_changes)

def selection_changes(self):
    #rows=[idx.row() for idx in self.tableWidget_2.selectionModel().selectedRows()]
    vals=[[idx.sibling(idx.row(),2).data(),idx.sibling(idx.row(),3).data(),idx.sibling(idx.row(),0).data()] for idx in self.tableWidget_2.selectionModel().selectedRows()]
    vals1=[float(v[1]) for v in vals]
    vals0=[float(v[0]) for v in vals]
    datetim=[str(v[2]) for v in vals]
    size=[float(200) for v in vals]
    

    
    x, y = self.mapcanvas.geomap(vals1, vals0)
    #if self.additionals!=False:
    if len(self.annots)>0:
        #self.additionals.remove()
        for annot in self.annots:
            annot.remove()
    
    self.annots=[]
    #self.additionals=self.mapcanvas.geomap.scatter(x, y, marker="v", s=size, color="white", zorder=10, alpha=0.7)
    for i, (X, Y) in enumerate(zip(x, y), start=1):
        annot=self.mapcanvas.axes.annotate(str(datetim[i-1]), (X,Y), xytext=(5, 5), textcoords='offset points', color="white", arrowprops=dict(facecolor='white', shrink=0.005))
        self.annots.append(annot)
    self.mapcanvas.draw()