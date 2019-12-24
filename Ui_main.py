
import os
from PyQt5 import QtWidgets, uic
from PyQt5 import Qt, QtCore, QtGui
from gui_designer.ideas4all_city_simulator_gui import Ui_MainWindow
import datetime
import numpy 

import Ui_preproc
import Ui_proc
import Ui_eqmap


       


class Ui(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Ui, self).__init__(parent)
        self.setupUi(self)
        #self.showFullScreen()
        #self.showMaximized()
        #self.setWindowFlags(
        #QtCore.Qt.Window |
        #QtCore.Qt.CustomizeWindowHint |
        #QtCore.Qt.WindowTitleHint |
        #QtCore.Qt.WindowCloseButtonHint |
        #QtCore.Qt.WindowStaysOnTopHint
        #)
        #self.hide()
        #self.show()
        self.checked_items={'Building Blocks': 2, 'Buildings': 2, 'Panels': 2, 'Panel Facets': 2, 'Panel Beams': 2, 'Panel Girders': 2, 'Walls': 2, 'Wall Facets': 2, "Wall Columns" : 2, "Terrain" :2}
        self.numberoftimeintervals=0

    def closeEvent(self, event):
        print("event")
        reply = QtWidgets.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            try:
                self.pre_eq_city.vtk_interactor.shutDownVTK()
                self.post_eq_city.vtk_interactor.shutDownVTK()
            except:
                pass
            else:
                event.accept()
        else:
            event.ignore()


    #START PREPROCESSING FUNCTIONS 
    def handleItemChanged(self, item, column):
        Ui_preproc.preproc_handleItemChanged(self,item,column)

    def manage_selection_enablebox(self):
        Ui_preproc.manage_selection_enablebox(self)

    def manage_selection_box_f(self):
        Ui_preproc.manage_selection_box_f(self)
    
    def manage_selection_box_b(self):
        Ui_preproc.manage_selection_box_b(self)

    def manage_selection_box_all(self):
        Ui_preproc.manage_selection_box_all(self)

    def manage_selection_box_bb(self):
        Ui_preproc.manage_selection_box_bb(self)

    def change_background_of_tablewidget(self):
        Ui_preproc.change_background_of_tablewidget(self)
    
    def fill_table_widget(self):
        Ui_preproc.fill_table_widget(self)

    def show_table_widget(self):
        Ui_preproc.show_table_widget(self)

    def show_tree_widget(self,_pre_eq_city):
        Ui_preproc.show_tree_widget(self,_pre_eq_city)
    #END PREPROCESSING FUNCTIONS 
    

    
    
    #START PROCESSING FUNCTIONS
    
    def manage_acc_buttons(self):
        Ui_proc.manage_acc_buttons(self)

    def selectDirDialogrun(self):
        Ui_proc.selectDirDialogrun(self)

    def selectDirDialogload(self):
        Ui_proc.selectDirDialogload(self)

    def openFileNameDialoglat(self):
        Ui_proc.openFileNameDialoglat(self)

    def openFileNameDialoglon(self):
        Ui_proc.openFileNameDialoglon(self)         
        
    def runsimulation(self):
        Ui_proc.runsimulation(self)

    def manage_simparams(self):
        Ui_proc.manage_simparams(self)

    def configure_simulation(self):
        Ui_proc.configure_simulation(self)

    def manage_runorload(self):
        Ui_proc.manage_runorload(self)

    def set_timelabel(self):
        Ui_proc.set_timelabel(self)

    def animatewindow(self):
        Ui_proc.animatewindow(self)
        
    def set_combobox_post_legend(self,value):
        Ui_proc.set_combobox_post_legend(self,value)

    def set_scalar_result(self,value):
        Ui_proc.set_scalar_result(self,value)

    def calculate_colormap_values(self):
        Ui_proc.calculate_colormap_values(self)

    def show_results(self):
        Ui_proc.show_results(self)

    def write_parameter_file(self, middlewaredir, outputpath, inputpath):
        Ui_proc.proc_write_parameter_file(self, middlewaredir, outputpath, inputpath)

    #END PROCESSING FUNCTIONS

    #START EQ MAP FUNCTIONS
    def set_mapcanvas(self):
        Ui_eqmap.set_mapcanvas(self)
    
    def config_eq_locs(self):
        Ui_eqmap.config_eq_locs(self)

    def selection_changes(self):
        Ui_eqmap.selection_changes(self)
     #END EQ MAP FUNCTIONS






    





 





