
import sys
import pprint
import time
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTreeWidgetItem, QColorDialog
from PyQt5 import Qt, QtCore, QtGui
from PyQt5.QtCore import Qt as qut
from PyQt5.QtCore import QTimer
import sys
import city
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
import vtk_interaction


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
       



class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.adjustSize()
        uic.loadUi('./gui_designer/ideas4all_city_simulator_gui.ui', self)
        self.show()
        self.checked_items={'Building Blocks': 2, 'Buildings': 2, 'Panels': 2, 'Panel Facets': 2, 'Panel Beams': 2, 'Panel Girders': 2, 'Walls': 2, 'Wall Facets': 2, "Wall Columns" : 2, "Terrain" :2}

    def handleItemChanged(self, item, column):
        checked_items={'Building Blocks': 0, 'Buildings': 0, 'Panels': 0, 'Panel Facets': 0, 'Panel Beams': 0, 'Panel Girders': 0, 'Walls': 0, 'Wall Facets': 0, "Wall Columns" : 0, "Terrain" : 0}
        if item.checkState(column) == QtCore.Qt.Checked:
            print('Item Checked')
        elif item.checkState(column) == QtCore.Qt.Unchecked:
            print('Item Unchecked')
        for item in self.treeWidget.findItems("", QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive):
            if (item.checkState(0)>0):
                checked_items[item.text(0)]=item.checkState(0)
                #print (item.text(0),item.checkState(0))
        print(checked_items)

        
        
        self.city_vtk.ground_triangles = vtk.vtkCellArray()
        self.city_vtk.building_triangles = vtk.vtkCellArray()
        self.city_vtk.trusses = vtk.vtkCellArray()
        self.city_vtk.LineColors = vtk.vtkUnsignedCharArray()
        self.city_vtk.LineColors.SetNumberOfComponents(3)
        self.city_vtk.LineColors.SetName("LineColors")
        self.city_vtk.BuildingCellColors = vtk.vtkUnsignedCharArray()
        self.city_vtk.BuildingCellColors.SetNumberOfComponents(3)
        self.city_vtk.BuildingCellColors.SetName("BuildingCellColors")
        self.city_vtk.insert_buildings(self.buildings,checked_items)
        self.city_vtk.insert_ground_triangles(self.ground_triangles.values(),checked_items)
        #refresh is necessary, otherwise it blows! apperantly set data appends sometimes
        self.city_vtk.PolyData_BuildingCells = vtk.vtkPolyData()
        self.city_vtk.PolyData_GroundCells = vtk.vtkPolyData()
        self.city_vtk.PolyData_Lines = vtk.vtkPolyData()
        self.city_vtk.visualize()
        self.city_vtk.renWin.Render()
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

    def change_background_of_tablewidget(self):
        self.tableWidget.item(1,2).setBackground(QtGui.QColor(255, 255, 255))
        
        
    def fill_table_widget(self):
        
        
        attr = ['Building Blocks','Buildings', 'Panel Facets', 'Panel Beams', 'Panel Girders', 'Wall Facets', 'Wall Columns', 'Vertices']
        selected_buildings=[self.comboboxes['Buildings'].itemText(i) for i in range(self.comboboxes['Buildings'].count())]

        pf=[]
        pb=[]
        pg=[]
        vc=[]
        wf=[]
        wc=[]


        for s in selected_buildings:
            if s!="None":
                current_building=self.buildings[s]
                for bs in current_building.basesets:
                    for f in bs.triangles:    
                        #self.comboboxes['Panel Facets'].addItem(str(f.id))
                        pf.append(str(f.id))
                
                for bm in current_building.beamsets:
                    for b in bm.beams:    
                        if b._type=="beam":
                            #self.comboboxes['Panel Beams'].addItem(str(b.id))
                            pb.append(str(b.femid))
                        if b._type=="girder":
                            pg.append(str(b.femid))
                    for v in bm.vertices:
                        #self.comboboxes['Vertices'].addItem(str(v.id))
                        vc.append(str(v.id))

                for w in current_building.walls:
                    for f in w.triangles:
                        #self.comboboxes['Wall Facets'].addItem(str(f.id))
                        wf.append(str(f.id))

                for c in current_building.columns:
                    wc.append(str(c.femid))

        self.comboboxes['Panel Facets'].addItems(pf)    
        self.comboboxes['Panel Beams'].addItems(pb) 
        self.comboboxes['Panel Girders'].addItems(pg)    
        self.comboboxes['Vertices'].addItems(vc)
        self.comboboxes['Wall Facets'].addItems(wf)
        self.comboboxes['Wall Columns'].addItems(wc)

        i=0
        for j in attr:
            number=str(self.comboboxes[j].count()-1)
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(number))
            i += 1
        # performing these actions in the loop is very time consuming
        self.comboboxes['Panel Facets'].setCurrentIndex(self.comboboxes['Panel Facets'].count() - 1)
        self.comboboxes['Panel Beams'].setCurrentIndex(self.comboboxes['Panel Beams'].count() - 1)
        self.comboboxes['Panel Girders'].setCurrentIndex(self.comboboxes['Panel Girders'].count() - 1)
        self.comboboxes['Vertices'].setCurrentIndex(self.comboboxes['Vertices'].count() - 1)
        self.comboboxes['Wall Facets'].setCurrentIndex(self.comboboxes['Wall Facets'].count() - 1)
        self.comboboxes['Wall Columns'].setCurrentIndex(self.comboboxes['Wall Columns'].count() - 1)

        



    def show_table_widget(self):
        attr = ['Building Blocks','Buildings', 'Panel Facets', 'Panel Beams', 'Panel Girders', 'Wall Facets', 'Wall Columns', 'Vertices']

        
        
        self.comboboxes={}
        self.checkboxes={}
        
        for i in attr:
            #current_comboBox = QtWidgets.QComboBox()
            current_comboBox=CheckableComboBox()
            self.comboboxes[i]=current_comboBox
            self.comboboxes[i].addItem("None")
            #self.comboboxes[i].setEditable(True)
            self.comboboxes[i].setMaxVisibleItems(5)
            self.checkboxes[i]=QtWidgets.QCheckBox()
            self.checkboxes[i].setCheckState(False)
        


        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(8)
        self.tableWidget.show()
        self.tableWidget.setHorizontalHeaderLabels(["Item Type","Item Id[s]","# of Selected Items","Annotations"])
        i=0
        for j in attr:
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(j))
            self.tableWidget.setCellWidget(i, 1, self.comboboxes[j])
            number=str(self.comboboxes[j].count()-1)
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(number))
            self.tableWidget.setCellWidget(i, 3, self.checkboxes[j])
            i += 1

    def show_tree_widget(self, buildings, ground_triangles, city_vtk, vertices, building_blocks, beams, beamsets):
        self.city_vtk=city_vtk
        self.buildings=buildings
        self.building_blocks=building_blocks
        self.vertices=vertices
        self.ground_triangles=ground_triangles
        tw    = self.treeWidget
        tw.setHeaderLabels(['City Item', 'Quantity [-]', 'Remark', 'Color'])
        tw.setAlternatingRowColors(True)

        bb = QtWidgets.QTreeWidgetItem(tw, ['Building Blocks', str(len(building_blocks.keys())), '# of Building Blocks'])
        bb.setFlags(bb.flags() |QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)

        b = QtWidgets.QTreeWidgetItem(bb, ['Buildings', str(len(buildings.keys())), '# of Buildings'])
        b.setFlags(b.flags() |QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)

        self.gt = QtWidgets.QTreeWidgetItem(tw, ['Terrain', str(len(ground_triangles.keys())), '# of triangles of geoterrain'])
        self.gt.setCheckState(0, QtCore.Qt.Checked)
        
        
        columns=0
        
        panltriangles=0
        walltriangles=0

        for bui in buildings.values():
            for bs in bui.basesets:
                panltriangles+=len(bs.triangles)
            
            for w in bui.walls:
                walltriangles+=len(w.triangles)
            columns+=len(bui.columns)


        b1=QtWidgets.QTreeWidgetItem(b, ['Panels', str(len(beamsets.keys())), '# of Panels'])
        b1.setFlags(b1.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
        #b1.setCheckState(0, QtCore.Qt.Checked)
        b11=QtWidgets.QTreeWidgetItem(b1, ['Panel Facets', str(panltriangles), '# of triangles on Panels'])
        self.PanelFacetPushbutton=ColorButton(self.city_vtk,'Panel Facets', self.buildings, self.checked_items)
        self.PanelFacetPushbutton.setStyleSheet("background:rgb(0,100,150)")
        self.PanelFacetPushbutton.clicked.connect(self.PanelFacetPushbutton.on_click)
        tw.setItemWidget(b11,3,self.PanelFacetPushbutton)
        b11.setFlags(b1.flags() | QtCore.Qt.ItemIsUserCheckable)
        b11.setCheckState(0, QtCore.Qt.Checked)

        bms=[b for b in beams.values() if b._type=="beam"]
        b12=QtWidgets.QTreeWidgetItem(b1, ['Panel Beams', str(len(bms)), '# of Beams around Panels'])
        self.PanelBeamPushbutton=ColorButton(self.city_vtk,'Panel Beams', self.buildings, self.checked_items)
        self.PanelBeamPushbutton.setStyleSheet("background:rgb(0,0,150)")
        self.PanelBeamPushbutton.clicked.connect(self.PanelBeamPushbutton.on_click)
        tw.setItemWidget(b12,3,self.PanelBeamPushbutton)
        b12.setFlags(b1.flags() | QtCore.Qt.ItemIsUserCheckable)
        b12.setCheckState(0, QtCore.Qt.Checked)

        grds=[b for b in beams.values() if b._type=="girder"]
        b13=QtWidgets.QTreeWidgetItem(b1, ['Panel Girders', str(len(grds)), '# of Girders around Panels'])
        self.PanelGirderPushbutton=ColorButton(self.city_vtk,'Panel Girders', self.buildings, self.checked_items)
        self.PanelGirderPushbutton.setStyleSheet("background:rgb(150,0,150)")
        self.PanelGirderPushbutton.clicked.connect(self.PanelGirderPushbutton.on_click)
        tw.setItemWidget(b13,3,self.PanelGirderPushbutton)
        b13.setFlags(b1.flags() | QtCore.Qt.ItemIsUserCheckable)
        b13.setCheckState(0, QtCore.Qt.Checked)


        b2=QtWidgets.QTreeWidgetItem(b, ['Walls', str(columns/2), '# of Walls'])
        b2.setFlags(b2.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
        #b1.setCheckState(0, QtCore.Qt.Checked)
        b21=QtWidgets.QTreeWidgetItem(b2, ['Wall Facets', str(walltriangles), '# of triangles on Walls'])
        self.WallFacetPushbutton=ColorButton(self.city_vtk, 'Wall Facets', self.buildings, self.checked_items)
        self.WallFacetPushbutton.setStyleSheet("background:rgb(0,150,100)")
        self.WallFacetPushbutton.clicked.connect(self.WallFacetPushbutton.on_click)
        tw.setItemWidget(b21,3,self.WallFacetPushbutton)
        b21.setFlags(b2.flags() | QtCore.Qt.ItemIsUserCheckable)
        b21.setCheckState(0, QtCore.Qt.Checked)



        b22=QtWidgets.QTreeWidgetItem(b2, ['Wall Columns', str(columns), '# of Columns along Walls'])
        self.WallColumnPushbutton=ColorButton(self.city_vtk, 'Wall Columns', self.buildings, self.checked_items)
        self.WallColumnPushbutton.setStyleSheet("background:rgb(0,150,0)")
        self.WallColumnPushbutton.clicked.connect(self.WallColumnPushbutton.on_click)
        tw.setItemWidget(b22,3,self.WallColumnPushbutton)
        b22.setFlags(b2.flags() | QtCore.Qt.ItemIsUserCheckable)
        b22.setCheckState(0, QtCore.Qt.Checked)


        
        #instead of itemchecked, itemlicked need to be used to avoid recursive effects
        self.treeWidget.itemClicked.connect(self.handleItemChanged)
        tw.expandAll()
        tw.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        tw.header().setStretchLastSection(False)
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
    window.showMaximized()
    window.show_table_widget()


    frame = window.tabWidget




    
    vl=window.vtkLayout
    vtkWidget = QVTKRenderWindowInteractor(frame)
    vl.addWidget(vtkWidget)

    

    city_vtk, buildings, ground_triangles, vertices, building_blocks, beams, beamsets=city.define_city(vtkWidget)
    window.show_tree_widget(buildings, ground_triangles, city_vtk, vertices, building_blocks, beams, beamsets)
    
    window.EnableSelection_checkBox.stateChanged.connect(window.manage_selection_enablebox)
    window.buildings_pushbutton.clicked.connect(window.manage_selection_box_b)
    window.buildingBlocks_pushbutton.clicked.connect(window.manage_selection_box_bb)
    window.append_pushbutton.clicked.connect(window.fill_table_widget)

    city_vtk.style = vtk_interaction.MouseInteractorHighLightActor(city_vtk, window)
    city_vtk.style.SetDefaultRenderer(city_vtk.ren)
    city_vtk.iren.SetInteractorStyle(city_vtk.style)
    city_vtk.visualize(_initial=True)
    city_vtk.renWin.Render()
    print("render window is rendered")
    city_vtk.iren.Initialize()
    city_vtk.iren.Start()
    edit=window.textEdit_Log
    sys.stdout = OutLog( edit, sys.stdout)
    


    app.exec_()
    
    
    
    



