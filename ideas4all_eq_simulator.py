
import sys
import pprint
import time
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5 import Qt, QtCore
import sys
import city
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk



class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.adjustSize()
        uic.loadUi('./gui_designer/ideas4all_city_simulator_gui.ui', self)
        self.show()

    def handleItemChanged(self, item, column):
        checked_items={'basesets': 0, 'beamsets': 0, 'buildings': 0, 'columns': 0, 'walls': 0, 'terrain': 0}
        if item.checkState(column) == QtCore.Qt.Checked:
            print('Item Checked')
        elif item.checkState(column) == QtCore.Qt.Unchecked:
            print('Item Unchecked')
        for item in self.treeWidget.findItems("", QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive):
            if (item.checkState(0)>0):
                checked_items[item.text(0)]=item.checkState(0)
                #print (item.text(0),item.checkState(0))
        pprint.pprint(checked_items)

        triangle_or_truss=True
        wireframe=False
        self.city_vtk.triangles = vtk.vtkCellArray()
        self.city_vtk.trusses = vtk.vtkCellArray()
        self.city_vtk.insert_buildings(self.buildings,checked_items)
        self.city_vtk.insert_triangles(self.ground_triangles.values(),checked_items)
        self.city_vtk.visualize(triangle_or_truss, wireframe, origin)
        city_vtk.renWin.Render()

    def show_tree_widget(self, buildings, ground_triangles, city_vtk):
        self.city_vtk=city_vtk
        self.buildings=buildings
        self.ground_triangles=ground_triangles
        tw    = self.treeWidget
        tw.setHeaderLabels(['City Item', 'Quantity [-]', 'Remark'])
        tw.setAlternatingRowColors(True)

        b = QtWidgets.QTreeWidgetItem(tw, ['buildings', str(len(buildings.keys())), '# of Buildings'])
        b.setFlags(b.flags() |QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
        #b.setCheckState(0, QtCore.Qt.Checked)

        self.gt = QtWidgets.QTreeWidgetItem(tw, ['terrain', str(len(ground_triangles.keys())), '# of triangles of geoterrain'])
        self.gt.setCheckState(0, QtCore.Qt.Checked)
        
        
        beamsets=0
        basesets=0
        columns=0
        walls=0

        for bui in buildings.values():
            beamsets+=len(bui.beamsets)
            basesets+=len(bui.basesets)
            columns+=len(bui.columns)
            walls+=len(bui.columns)

        b1=QtWidgets.QTreeWidgetItem(b, ['beamsets', str(beamsets), '# of Horizintal beams'])
        b1.setFlags(b1.flags() | QtCore.Qt.ItemIsUserCheckable)
        b1.setCheckState(0, QtCore.Qt.Checked)
        b2=QtWidgets.QTreeWidgetItem(b, ['basesets', str(basesets), '# of triangles on floors and roofs'])
        b2.setFlags(b2.flags() | QtCore.Qt.ItemIsUserCheckable)
        b2.setCheckState(0, QtCore.Qt.Checked)
        b3=QtWidgets.QTreeWidgetItem(b, ['columns', str(columns), '# of vertical columns'])
        b3.setFlags(b3.flags() | QtCore.Qt.ItemIsUserCheckable)
        b3.setCheckState(0, QtCore.Qt.Checked)
        b4=QtWidgets.QTreeWidgetItem(b, ['walls', str(walls), '# of triangles on walls'])
        b4.setFlags(b4.flags() | QtCore.Qt.ItemIsUserCheckable)
        b4.setCheckState(0, QtCore.Qt.Checked)
        
        #instead of itemchecked, itemlicked need to be used to avoid recursive effects
        self.treeWidget.itemClicked.connect(self.handleItemChanged)
        
        tw.show()
        




class OutLog:
    def __init__(self, edit, out=None, color=None):
        """(edit, out=None, color=None) -> can write stdout, stderr to a
        QTextEdit.
        edit = QTextEdit
        out = alternate stream ( can be the original sys.stdout )
        color = alternate color (i.e. color stderr a different color)
        """
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

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.showMaximized()

    frame = window.tabWidget


    vl=window.verticalLayout
    vtkWidget = QVTKRenderWindowInteractor(frame)
    vl.addWidget(vtkWidget)

    city_vtk, origin, buildings, ground_triangles=city.define_city(vtkWidget)
    window.show_tree_widget(buildings, ground_triangles, city_vtk)

    triangle_or_truss=True
    wireframe=False
    city_vtk.visualize(triangle_or_truss, wireframe, origin)
    city_vtk.renWin.Render()
    city_vtk.iren.Initialize()
    city_vtk.iren.Start()
    #edit=
    #sys.stdout = OutLog( edit, sys.stdout)
    app.exec_()
    
    
    
    



