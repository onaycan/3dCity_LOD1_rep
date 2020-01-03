from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtGui import QIcon, QPixmap, QPainter
import numpy


plt.style.use('dark_background')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Ubuntu'
plt.rcParams['font.monospace'] = 'Ubuntu Mono'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titlesize'] = 10
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 12

class DiagCanvas(FigureCanvas):
    def __init__(self, parent=None, width=8, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        
        #self.axes = self.fig.add_subplot(111)
        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        #with plt.style.context(style_label):
        
        
        self.fig.tight_layout()


def setup_Ui_preproc_diag(self):
    self.diagcanvas= DiagCanvas(self, width=4, height=4, dpi=100)
    
    
    self.verticalLayout_23.addWidget(self.diagcanvas)
    self.tabWidget_2.currentChanged.connect(self.switch_citydiag_2)
    self.tabWidget.currentChanged.connect(self.switch_citydiag)
    self.listWidget.addItem("Histogram of Building Levels")
    self.listWidget.addItem("Histogram of Building Block Poputation")

    self.listWidget.itemClicked.connect(self.selectdiagram)
    self.listWidget.setCurrentRow(0)


    attrib=['Histogram of Number of Levels','Number of Levels [-]','Frequency']
    x =[int(b.levels) for b in self.pre_eq_city.buildings.values() if b.levels.isnumeric()]
    w = self.frame_5.geometry().width()
    h = self.frame_5.geometry().height()
    pm=QPixmap("./images/histolevels.png")
    self.label_21.setPixmap(pm.scaled(w,h,QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
    self.plot_level_histogram(x, attrib)    
def selectdiagram(self, item):
    
    if item.text()=="Histogram of Building Levels":
        attrib=['Histogram of Number of Levels','Number of Levels [-]','Frequency']
        x =[int(b.levels) for b in self.pre_eq_city.buildings.values() if b.levels.isnumeric()]
        w = self.frame_5.geometry().width()
        h = self.frame_5.geometry().height()
        pm=QPixmap("./images/histolevels.png")
        self.label_21.setPixmap(pm.scaled(w,h,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))
        
    if item.text()=="Histogram of Building Block Poputation":
        attrib=['Histogram of Building Block Population','Number of Buildings in Block [-]','Frequency']
        x=[int(len(bb.buildings)) for bb in self.pre_eq_city.buildingblocks.values()]
        w = self.frame_5.geometry().width()
        h = self.frame_5.geometry().height()
        pm=QPixmap("./images/histoblocks.png")
        self.label_21.setPixmap(pm.scaled(w,h,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))
    
    self.diagcanvas.ax.remove()
    self.plot_level_histogram(x,attrib)



def switch_citydiag_2(self):
    current_index_2=self.tabWidget_2.currentIndex()
    current_text_2=self.tabWidget_2.tabText(current_index_2)
    if current_text_2=="Statistics":
        self.tabWidget.setCurrentWidget(self.tab)
    else:
        self.tabWidget.setCurrentWidget(self.tabWidget_vtk)

def switch_citydiag(self):
    current_index=self.tabWidget.currentIndex()
    current_text=self.tabWidget.tabText(current_index)
    if current_text=="Statistics":
        self.tabWidget_2.setCurrentWidget(self.pre_city_statistics)
    else:
        self.tabWidget_2.setCurrentWidget(self.pre_city_tab)
        

def plot_level_histogram(self, _x, _attr):
    x=_x
    #x =[int(b.levels) for b in self.pre_eq_city.buildings.values() if b.levels.isnumeric()]
    
    
    self.diagcanvas.ax = self.diagcanvas.fig.subplots()
    bins = numpy.arange(1,max(x)+2) - 0.5
    rw=0.9
    n, bins, patches=self.diagcanvas.ax.hist(x, bins, facecolor='blue', alpha=0.5, rwidth=rw)
    self.diagcanvas.ax.set_title(_attr[0])
    self.diagcanvas.ax.set_xlabel(_attr[1])
    self.diagcanvas.ax.set_ylabel(_attr[2])
    
    cols=[]
    tiks=[]
    for i in range(1,max(x)+1):
        tiks.append(i)
        current_percentage=n[i-1]/len(x)*100.0
        cols.append(n[i-1]/len(x))
        current_percentage=round(current_percentage,2)
        self.diagcanvas.ax.text(bins[i]-1*rw,n[i-1]+1,str(int(n[i-1]))+" ("+str(current_percentage)+"%)", size=6)
    maxc=max(cols)
    col=[c/maxc for c in cols]
    cm = plt.cm.get_cmap('RdYlBu_r')
    for c, p in zip(col, patches):
        plt.setp(p, 'facecolor', cm(c))
    
    self.diagcanvas.ax.set_xticks(tiks)
    self.diagcanvas.draw()

        