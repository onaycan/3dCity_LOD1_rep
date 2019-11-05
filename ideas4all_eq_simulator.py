
from PyQt5 import QtWidgets, uic
from PyQt5 import Qt
import sys
import city
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('./gui_designer/ideas4all_city_simulator_gui.ui', self)
        self.show()



app = QtWidgets.QApplication(sys.argv)
window = Ui()
frame = window.frame
vl=window.verticalLayout
vtkWidget = QVTKRenderWindowInteractor(frame)
vl.addWidget(vtkWidget)

city_vtk, origin=city.define_city(vtkWidget)
triangle_or_truss=True
wireframe=False
city_vtk.visualize(triangle_or_truss, wireframe, origin)
city_vtk.renWin.Render()
app.exec_()
city_vtk.iren.Initialize()
city_vtk.iren.Start()



