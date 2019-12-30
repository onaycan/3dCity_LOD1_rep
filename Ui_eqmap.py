
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
from sklearn.preprocessing import minmax_scale
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from geopy.distance import geodesic
    
from PyQt5 import QtCore 

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
        self.geomap.drawmapboundary(fill_color='aqua')
        self.geomap.fillcontinents(color='#ddaa66',lake_color='aqua')
        self.geomap.drawcoastlines()

        #this does not work offline. alternative: find a picture wrap instead. 
        #self.geomap.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 1500, verbose= True)
        
        #this is an alternative 
        #self.geomap.etopo()        

        self.fig.tight_layout()
        self.fig.patch.set_facecolor('black')
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


def setup_Ui_eqmap(self):
    self.set_mapcanvas()
    self.config_eq_locs()

def set_mapcanvas(self):
    self.mapcanvas = MapCanvas(self, width=4, height=4, dpi=100)
    self.verticalLayout_4.addWidget(self.mapcanvas)

def config_eq_locs(self):

    self.lineEdit.setText("40.98549606")
    self.lineEdit_2.setText("29.03533319")
    self.lineEdit.setReadOnly(True)
    self.lineEdit_2.setReadOnly(True)
    
    self.orig=[float(self.lineEdit.text()),float(self.lineEdit_2.text())]
    x, y = self.mapcanvas.geomap(self.orig[1], self.orig[0])
    origin_marker=self.mapcanvas.geomap.scatter(x, y, marker="$City$", s=250, color="red", zorder=10, alpha=0.9)
    self.mapcanvas.draw()


    self.additionals=False
    self.annots=[]
    self.cluster_annots=[]
    self.eq_distlines=[]
    eqsfilename=".\\eq_db\\query_eqs_1500_2019.csv"
    self.eqsdata=pd.read_csv(eqsfilename, delimiter=',').to_dict()


    self.eq_times=list(self.eqsdata['time'].values())
    self.eq_lons=list(self.eqsdata['longitude'].values())
    self.eq_lats=list(self.eqsdata['latitude'].values())
    self.eq_mags=[float(v) for v in self.eqsdata['mag'].values()]
    self.eq_depths=[float(v) for v in self.eqsdata['depth'].values()]
        
    numberofclusters=11
    self.cluster_labels=self.cluster_eqs(numberofclusters)
    #pprint.pprint(cluster_labels)

    self.sc=False
    self.cbar_occurence=-1    

    times=[datetime.strptime((v.split("T")[0]+" "+v.split("T")[1].split(".")[0]), '%Y-%m-%d %H:%M:%S') for v in self.eqsdata['time'].values()]
    min_date=str(min(times))
    minqdate = QtCore.QDateTime.fromString(min_date, 'yyyy-M-d hh:mm:ss')
    self.dateTimeEdit.setDateTime(minqdate)
    self.dateTimeEdit.setReadOnly(True)
    max_date=str(max(times))
    maxqdate = QtCore.QDateTime.fromString(max_date, 'yyyy-M-d hh:mm:ss')
    self.dateTimeEdit_2.setDateTime(maxqdate)
    self.dateTimeEdit_2.setReadOnly(True)

    #start clusters table 
    self.eq_checkboxes={}
    self.eq_clusters={}
    for c in range(numberofclusters):   
        cluster_mags=numpy.array([self.eq_mags[ci] for ci in range(len(self.cluster_labels)) if self.cluster_labels[ci]==c])
        cluster_depths=numpy.array([self.eq_depths[ci] for ci in range(len(self.cluster_labels)) if self.cluster_labels[ci]==c])
        cluster_lats=numpy.array([self.eq_lats[ci] for ci in range(len(self.cluster_labels)) if self.cluster_labels[ci]==c])
        cluster_lons=numpy.array([self.eq_lons[ci] for ci in range(len(self.cluster_labels)) if self.cluster_labels[ci]==c])
        max_cluster_mags=round(max(cluster_mags),2)
        std_cluster_mags=round(numpy.std(cluster_mags),2)
        std_cluster_depths=round(numpy.std(cluster_depths),2)
        mean_cluster_mags=round(numpy.mean(cluster_mags),2)
        mean_cluster_depths=round(numpy.mean(cluster_depths),2)
        mean_cluster_lats=round(numpy.mean(cluster_lats),2)
        mean_cluster_lons=round(numpy.mean(cluster_lons),2)

        here=(mean_cluster_lats,mean_cluster_lons)
        dist=round(geodesic(self.orig,here).kilometers,2)
        current_res=[c, len(cluster_mags), dist, max_cluster_mags, mean_cluster_mags, std_cluster_mags, mean_cluster_depths, std_cluster_depths, mean_cluster_lats, mean_cluster_lons]
        self.eq_clusters[c]=current_res


    self.tableWidget_3.setColumnCount(10)
    self.tableWidget_3.setRowCount(numberofclusters)
    self.tableWidget_3.show()
    self.tableWidget_3.setHorizontalHeaderLabels(["cluster-id", "#events","Distance2Orig","Max Mag.","Mean Mag.","Std. Mag.","Mean Depth","Std. Depth", "Mean Lat.", "Mean Lon."])
    for j in range(len(self.eq_clusters)):
        for i in range(10):
            item = QtWidgets.QTableWidgetItem()
            item.setData(QtCore.Qt.DisplayRole,float(self.eq_clusters[j][i]))
            self.tableWidget_3.setItem(j, i, item)
            #self.tableWidget_3.setItem(j, i, QtWidgets.QTableWidgetItem(self.eq_clusters[j][i])))


    #pprint.pprint(self.eq_clusters)
    self.tableWidget_3.setSortingEnabled(True)
    #self.tableWidget_3.resizeColumnsToContents()

    self.checkall_pushButton.clicked.connect(self.clickall_eqclusters)
    self.uncheckall_pushButton.clicked.connect(self.unclickall_eqclusters)
    self.tableWidget_3.cellClicked.connect(self.eq_cl_cell_was_clicked)
    #self.tableWidget_3.itemSelectionChanged.connect(self.selection_changes_cl)


    self.tableWidget_2.setSortingEnabled(True)
    self.tableWidget_2.cellClicked.connect(self.eq_events_cell_was_clicked)
    #self.tableWidget_2.itemSelectionChanged.connect(self.selection_changes)


def fill_eq_events_table(self, mags_s):
    self.tableWidget_2.clear()
    times=[self.eq_times[i] for i in range(len(mags_s)) if mags_s[i]!=0]
    mags=[self.eq_mags[i] for i in range(len(mags_s)) if mags_s[i]!=0]
    lats=[self.eq_lats[i] for i in range(len(mags_s)) if mags_s[i]!=0]
    lons=[self.eq_lons[i] for i in range(len(mags_s)) if mags_s[i]!=0]
    cluster_labels=[self.cluster_labels[i] for i in range(len(mags_s)) if mags_s[i]!=0]

    self.tableWidget_2.setColumnCount(5)
    self.tableWidget_2.setRowCount(len(times))
    self.tableWidget_2.show()
    self.tableWidget_2.setHorizontalHeaderLabels(["DateTime","Mag.","Lat.","Lon.","Cluster"])
    for j in range(len(times)):
        #self.tableWidget_2.setItem(j, 0, QtWidgets.QTableWidgetItem(str(times[j])))
        #self.tableWidget_2.setItem(j, 1, QtWidgets.QTableWidgetItem(str(mags[j])))
        #self.tableWidget_2.setItem(j, 2, QtWidgets.QTableWidgetItem(str(lats[j])))
        #self.tableWidget_2.setItem(j, 3, QtWidgets.QTableWidgetItem(str(lons[j])))
        #self.tableWidget_2.setItem(j, 4, QtWidgets.QTableWidgetItem(str(cluster_labels[j])))

        item = QtWidgets.QTableWidgetItem()
        item.setData(QtCore.Qt.DisplayRole,str(times[j]))
        self.tableWidget_2.setItem(j, 0, item)

        item = QtWidgets.QTableWidgetItem()
        item.setData(QtCore.Qt.DisplayRole,float(mags[j]))
        self.tableWidget_2.setItem(j, 1, item)

        item = QtWidgets.QTableWidgetItem()
        item.setData(QtCore.Qt.DisplayRole,float(lats[j]))
        self.tableWidget_2.setItem(j, 2, item)

        item = QtWidgets.QTableWidgetItem()
        item.setData(QtCore.Qt.DisplayRole,float(lons[j]))
        self.tableWidget_2.setItem(j, 3, item)

        item = QtWidgets.QTableWidgetItem()
        item.setData(QtCore.Qt.DisplayRole,int(cluster_labels[j]))
        self.tableWidget_2.setItem(j, 4, item)



def selection_changes_cl(self):
    self.cbar_occurence+=1
    if type(self.sc)!=bool:
        self.sc.remove()
    selecteds=[int(idx.sibling(idx.row(),0).data()) for idx in self.tableWidget_3.selectionModel().selectedRows()]
    mags_s=[]
    size_scale=10
    for v in range(len(self.eqsdata['mag'].keys())):
        if self.cluster_labels[v] in selecteds:
            mags_s.append(size_scale)
        else:
            mags_s.append(0)
    x, y = self.mapcanvas.geomap(self.eq_lons, self.eq_lats)
    self.sc=self.mapcanvas.geomap.scatter(x, y, marker="o", s=mags_s, alpha=0.9, cmap='rainbow', c=self.cluster_labels)
    if self.cbar_occurence==0:
        divider = make_axes_locatable(self.mapcanvas.axes)
        cax = divider.append_axes('right', size='5%', pad=0.15)
        cax.tick_params(color="white", labelcolor="white")
        cbar=self.mapcanvas.fig.colorbar(self.sc,cax=cax)
        cbar.set_label('Eartquake Clusters', rotation=270,horizontalalignment='center', labelpad=10, color="white")
    #self.mapcanvas.draw()
    self.draw_cluster_annotations()
    self.fill_eq_events_table(mags_s)
    self.selection_changes()


def draw_cluster_annotations(self):
    selecteds=[[int(idx.sibling(idx.row(),0).data()),float(idx.sibling(idx.row(),8).data()),float(idx.sibling(idx.row(),9).data()),
                int(idx.sibling(idx.row(),1).data()),float(idx.sibling(idx.row(),3).data()),float(idx.sibling(idx.row(),4).data()),
                float(idx.sibling(idx.row(),2).data())] 
                for idx in self.tableWidget_3.selectionModel().selectedRows()]
    vals1=[float(v[2]) for v in selecteds]
    vals0=[float(v[1]) for v in selecteds]
    size=[float(200) for v in selecteds]
    clusternames=["Cluster: "+str(v[0])+"\n#ofevents: "+str(v[3])+"\nMean Mag: "+str(v[5])+"\nMax Mag: "+str(v[4])+"\nDist. to City: "+str(v[6]) for v in selecteds]
    x, y = self.mapcanvas.geomap(vals1, vals0)
    if len(self.cluster_annots)>0:
        for annot in self.cluster_annots:
            annot.remove()
        for line in self.eq_distlines:
            line.remove()
    
    self.cluster_annots=[]
    self.eq_distlines=[]
    additional_marker=self.mapcanvas.geomap.scatter(x, y, marker="+", s=size, color="white", zorder=10, alpha=0.7)
    self.cluster_annots.append(additional_marker)
    for i, (X, Y) in enumerate(zip(x, y), start=1):
        annot=self.mapcanvas.axes.annotate(str(clusternames[i-1]), (X,Y), xytext=(23, 23), textcoords='offset points', color="white", arrowprops=dict(facecolor='white', shrink=0.005), size=9)
        self.cluster_annots.append(annot)


    #x, y = self.mapcanvas.geomap(self.orig[1], self.orig[0])
    for v in range(len(vals0)):
        line,=self.mapcanvas.geomap.plot([self.orig[1], vals1[v]],[self.orig[0],vals0[v]],linewidth=1, color="white",mfc='none', mec='k', latlon=True, linestyle=":")
        self.eq_distlines.append(line)
        
    self.mapcanvas.draw()


def clickall_eqclusters(self):
    self.tableWidget_3.selectAll()
    self.selection_changes_cl()

def unclickall_eqclusters(self):
    self.tableWidget_3.clearSelection()
    self.selection_changes_cl()

def eq_cl_cell_was_clicked(self, row, column):
    self.tableWidget_3.selectRow(row)
    self.selection_changes_cl()
    

def eq_events_cell_was_clicked(self, row, column):
    self.tableWidget_2.selectRow(row)
    self.selection_changes()


def cluster_eqs(self, _numberofclusters):
    mags=numpy.array(self.eq_mags)
    lons=numpy.array(self.eq_lons)
    lats=numpy.array(self.eq_lats)
    depths=numpy.array(self.eq_depths)

    self.normal_eqsdata=numpy.stack((mags, lons, lats, depths), axis = 1) 
    self.normal_eqsdata = minmax_scale(self.normal_eqsdata, feature_range=(0,1), axis=0)

    k_means = KMeans(n_clusters=_numberofclusters, random_state=0).fit(self.normal_eqsdata)
    #pprint.pprint(list(k_means.labels_))
    #print(_numberofclusters,k_means.inertia_)
    ssc=silhouette_score(self.normal_eqsdata, k_means.labels_, metric = 'euclidean')
    print(_numberofclusters, ssc)
    return list(k_means.labels_)
    #pprint.pprint(self.normal_eqsdata)


def selection_changes(self):
    vals=[[idx.sibling(idx.row(),2).data(),idx.sibling(idx.row(),3).data(),idx.sibling(idx.row(),0).data(),idx.sibling(idx.row(),1).data()] for idx in self.tableWidget_2.selectionModel().selectedRows()]
    vals1=[float(v[1]) for v in vals]
    vals0=[float(v[0]) for v in vals]
    datetim=["date: "+str(v[2])+"\nmag: "+str(v[3]) for v in vals]
    x, y = self.mapcanvas.geomap(vals1, vals0)
    if len(self.annots)>0:
        for annot in self.annots:
            annot.remove()
    
    self.annots=[]
    #self.additionals=self.mapcanvas.geomap.scatter(x, y, marker="v", s=size, color="white", zorder=10, alpha=0.7)
    for i, (X, Y) in enumerate(zip(x, y), start=1):
        annot=self.mapcanvas.axes.annotate(str(datetim[i-1]), (X,Y), xytext=(0, -15), textcoords='offset points', color="white", arrowprops=dict(facecolor='white', shrink=0.005), size=8)
        self.annots.append(annot)
    self.mapcanvas.draw()