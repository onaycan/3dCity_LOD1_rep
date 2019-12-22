
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.basemap import Basemap

from PyQt5 import QtWidgets, uic, QtGui, QtCore




    

class MapCanvas(FigureCanvas):
    def __init__(self, parent=None, width=8, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        
        
        self.axes = fig.add_subplot(111)
        
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        map = Basemap(llcrnrlon=25.979530,llcrnrlat=40.015137,urcrnrlon=31.979530,urcrnrlat=42.015137,
             resolution='h', projection='lcc', lat_0 = 41.015137, lon_0 = 28.979530, ax=self.axes)

        map.drawmapboundary(fill_color='aqua')
        map.fillcontinents(color='#ddaa66',lake_color='aqua')
        map.drawcoastlines()
        fig.tight_layout()
        self.axes.autoscale(enable=True,axis='both',tight=True)
        #parent.addToolBar(QtCore.Qt.BottomToolBarArea, NavigationToolbar(self, parent.groupBox_5))
        nav_widget=NavigationToolbar(self,parent)
        
        
        palette = nav_widget.palette()


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


        nav_widget.setPalette(palette)
        parent.verticalLayout_4.addWidget(nav_widget)
def set_mapcanvas(self):
    sc = MapCanvas(self, width=4, height=4, dpi=100)
    self.verticalLayout_4.addWidget(sc)
