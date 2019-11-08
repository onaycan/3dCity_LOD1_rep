
import sys
import pprint
import time
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5 import Qt, QtCore, QtGui
import sys
import city
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
import vtk_interaction


# overwrite combobox, so that no duplicates are allowed. 
class ComboBox(QtWidgets.QComboBox):
    def addItem(self, item):
        if item not in self.get_set_items():
            super(ComboBox, self).addItem(item)

    def addItems(self, items):
        items = list(self.get_set_items() | set(items))
        super(ComboBox, self).addItems(items)

    def get_set_items(self):
        return set([self.itemText(i) for i in range(self.count())])


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.adjustSize()
        uic.loadUi('./gui_designer/ideas4all_city_simulator_gui.ui', self)
        self.show()
        self.checked_items={'basesets': 2, 'beamsets': 2, 'buildings': 2, 'columns': 2, 'walls': 2, 'terrain': 2}
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
        print(checked_items)

        
        self.city_vtk.triangles = vtk.vtkCellArray()
        self.city_vtk.trusses = vtk.vtkCellArray()
        self.city_vtk.insert_buildings(self.buildings,checked_items)
        self.city_vtk.insert_triangles(self.ground_triangles.values(),checked_items)
        #refresh is necessary, otherwise it blows! apperantly set data appends sometimes
        self.city_vtk.PolyData = vtk.vtkPolyData()
        self.city_vtk.visualize()
        city_vtk.renWin.Render()
        self.checked_items=checked_items
    
    def manage_selection_enablebox(self):
        if self.EnableSelection_checkBox.isChecked():
            print("Selection is Enabled")
            #self.facets_pushbutton.setEnabled(True)
            self.buildings_pushbutton.setEnabled(True)
            self.buildingBlocks_pushbutton.setEnabled(True)
        else:
            print("Selection is Disabled")
            #self.facets_pushbutton.setChecked(False)
            self.buildings_pushbutton.setChecked(False)
            self.buildingBlocks_pushbutton.setChecked(False)
            #self.facets_pushbutton.setEnabled(False)
            self.buildings_pushbutton.setEnabled(False)
            self.buildingBlocks_pushbutton.setEnabled(False)


    def manage_selection_box_f(self):
        if self.facets_pushbutton.isChecked():
            print("Facet selection is activated")
            self.buildings_pushbutton.setChecked(False)
            self.buildingBlocks_pushbutton.setChecked(False)

    def manage_selection_box_b(self):
         if self.buildings_pushbutton.isChecked():
            print("Building selection is activated")
            #self.facets_pushbutton.setChecked(False)
            self.buildingBlocks_pushbutton.setChecked(False)

    def manage_selection_box_bb(self):
        if self.buildingBlocks_pushbutton.isChecked():
            print("Building Block selection is activated")
            #self.facets_pushbutton.setChecked(False)
            self.buildings_pushbutton.setChecked(False)
        



    def show_table_widget(self, triggered=False):
        attr = ['buildings', 'beamsets', 'columns', 'basesets', 'walls']

        if not triggered:
            self.comboboxes={}
            for i in attr:
                current_comboBox = QtWidgets.QComboBox()
                self.comboboxes[i]=current_comboBox
                self.comboboxes[i].addItem("None")


        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(5)
        self.tableWidget.show()
        self.tableWidget.setHorizontalHeaderLabels(["Item Type","Item Id[s]"])
        i=0
        for j in attr:
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(j))
            self.tableWidget.setCellWidget(i, 1, self.comboboxes[j])
            i += 1

    def show_tree_widget(self, buildings, ground_triangles, city_vtk, vertices):
        self.city_vtk=city_vtk
        self.buildings=buildings
        self.vertices=vertices
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
    # start application of dark theme
    app.setStyle("Fusion")
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
         
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142,45,197).lighter())
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)   
    app.setPalette(palette)
    # end application of dark theme
    
    window = Ui()
    #window.showMaximized()

    frame = window.tabWidget


    vl=window.vtkLayout
    vtkWidget = QVTKRenderWindowInteractor(frame)
    vl.addWidget(vtkWidget)

    city_vtk, buildings, ground_triangles, vertices=city.define_city(vtkWidget)
    window.show_tree_widget(buildings, ground_triangles, city_vtk, vertices)
    window.show_table_widget()
    window.EnableSelection_checkBox.stateChanged.connect(window.manage_selection_enablebox)
    #window.facets_pushbutton.clicked.connect(window.manage_selection_box_f)
    window.buildings_pushbutton.clicked.connect(window.manage_selection_box_b)
    window.buildingBlocks_pushbutton.clicked.connect(window.manage_selection_box_bb)

    city_vtk.style = vtk_interaction.MouseInteractorHighLightActor(city_vtk, window)
    city_vtk.style.SetDefaultRenderer(city_vtk.ren)
    city_vtk.iren.SetInteractorStyle(city_vtk.style)


    city_vtk.visualize()
    city_vtk.renWin.Render()
    city_vtk.iren.Initialize()
    city_vtk.iren.Start()
    edit=window.textEdit_Log
    sys.stdout = OutLog( edit, sys.stdout)

    app.exec_()
    
    
    
    



