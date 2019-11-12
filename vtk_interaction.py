import vtk
import trusses
import vertices
import columns
import matplotlib


def rgb(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    r/=255.0
    g/=255.0
    b/=255.0
    
    return r, g, b



class MouseInteractorHighLightActor(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self,vtkinteractor,_window,parent=None):
        self.vtkinteractor=vtkinteractor
        #self.SetDefaultRenderer(self.vtkinteractor.ren)
        self.window=_window
        self.buildings=_window.buildings
        self.ground_triangles=_window.ground_triangles
        self.vertices=_window.vertices
        #homes=[v.homes for v in self.vertices.values()]
        #print(homes)
        self.checked_items=_window.checked_items
        self.spressed=False
        #self.AddObserver("MiddleButtonReleaseEvent",self.middleButtonReleaseEvent)    
        
        self.AddObserver("LeftButtonPressEvent", self.ButtonEvent)
        self.vtkinteractor.iren.AddObserver("KeyPressEvent", self.Keypress)
        self.debugfile=open("debugfile.deb",'w')
 
    def Keypress(self,obj,event):
       
        key = obj.GetKeySym()
        #key = obj.GetKeyCode()
        self.spressed=False
        if key == "c":
            self.spressed=True
        self.OnKeyRelease()
        return

    def ButtonEvent(self,obj,event):
        
        if self.spressed:
            if self.window.buildings_pushbutton.isChecked() or self.window.buildingBlocks_pushbutton.isChecked():
                self.spressed=False
                clickPos = self.GetInteractor().GetEventPosition()
                picker = vtk.vtkCellPicker()
                #picker.Pick(clickPos[0], clickPos[1], 0, self.vtkinteractor.ren)
                picker.Pick(clickPos[0], clickPos[1], 0, self.GetDefaultRenderer())

                #cellids=picker.GetSubId()
                cellid=picker.GetCellId()

                print("selected cell id: "+str(cellid))

                numberofids=self.vtkinteractor.PolyData.GetCell(cellid).GetPointIds().GetNumberOfIds()
                pointids=[]
                

                sets=[]
                notground=True
                for p in range(numberofids):
                    pid=self.vtkinteractor.PolyData.GetCell(cellid).GetPointIds().GetId(p)
                    if self.vtkinteractor.VtkPointId2vertexid[pid].startswith("g"):
                        notground=False
                    else:
                        sets.append(self.vertices[self.vtkinteractor.VtkPointId2vertexid[pid]].homes)

                if notground:
                    self.building_vertices=set()

                    common_home=[set.intersection(*sets)][0] #in fact this is buggy.but you can not choose really a side wall or bottom triangle with common edge without being able to see it 
                    common_home=list(common_home)[0]
                    self.window.comboboxes['buildings'].addItem(common_home)
                    self.window.comboboxes['buildings'].setCurrentIndex(self.window.comboboxes['buildings'].count() - 1)

                    self.get_building_vertices(common_home)


                    if self.window.buildingBlocks_pushbutton.isChecked():
                        self.window.comboboxes['building blocks'].addItem(self.buildings[common_home].buildingblock_id)
                        self.window.comboboxes['building blocks'].setCurrentIndex(self.window.comboboxes['building blocks'].count() - 1)
                        for n in self.buildings[common_home].neighbours:
                            self.window.comboboxes['buildings'].addItem(n)
                            self.window.comboboxes['buildings'].setCurrentIndex(self.window.comboboxes['buildings'].count() - 1)
                            for bb in self.buildings[n].beamsets:
                                for v in bb.vertices:
                                    self.building_vertices.add(v.id)

                    self.window.fill_table_widget()


                    for pid in self.building_vertices:
                        pointids.append(self.vtkinteractor.vertexId2VtkPointId[pid])



                    print("points of selected cell: "+ str(pointids))
                    for p in pointids:
                        self.vtkinteractor.Colors.SetTuple3(p,255,0,0)
                    print(self.vtkinteractor.triangles.GetNumberOfCells())
                    self.vtkinteractor.mapper.Update()
                    self.vtkinteractor.mapper.ScalarVisibilityOff()
                    self.vtkinteractor.mapper.ScalarVisibilityOn()
                    self.vtkinteractor.renWin.Render()
        
        self.OnLeftButtonDown()
        return 
    
    def get_building_vertices(self,_home):
        b=_home
        print("home is selected: "+str(b))
        for bb in range(1,len(self.buildings[b].beamsets)):
            for v in self.buildings[b].beamsets[bb].vertices:
                self.building_vertices.add(v.id)



class vtk_interactor:
    def __init__(self, vtkWidget, _origin):
        self.outfile=open("debugfile.out",'w')

        self.origin=_origin
        # create a rendering window and renderer
        self.ren = vtk.vtkRenderer()
        #vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        #self.renWin = vtk.vtkRenderWindow()
        self.renWin=vtkWidget.GetRenderWindow()
        self.renWin.AddRenderer(self.ren)

        # create a renderwindowinteractor
        #self.iren = vtk.vtkRenderWindowInteractor()
        self.iren=vtkWidget.GetRenderWindow().GetInteractor()

        #self.iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        self.iren.SetRenderWindow(self.renWin)
        self.PolyData = vtk.vtkPolyData()
        self.PolyData_Lines = vtk.vtkPolyData()
        
        #self.PolyData=vtk.vtkExtractPolyDataGeometry()
        self.Colors = vtk.vtkUnsignedCharArray()
        self.Colors.SetNumberOfComponents(3)
        self.Colors.SetName("Colors")

        self.LineColors = vtk.vtkUnsignedCharArray()
        self.LineColors.SetNumberOfComponents(3)
        self.LineColors.SetName("LineColors")

        

        

        self.points = vtk.vtkPoints()
        self.triangles = vtk.vtkCellArray()
        self.numberoftriangles=0
        self.trusses = vtk.vtkCellArray()
        
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper_Lines = vtk.vtkPolyDataMapper()
        self.vertexId2VtkPointId={}
        self.VtkPointId2vertexid={}
        self.VtkTriangleId2Triangleid={}
        
        
    

    def insert_vertices(self,_vertices, _colormap=None):
        min_elevation=min([v.coordsX[2] for v in _vertices])*1.8
        max_elevation=max([v.coordsX[2] for v in _vertices])
        #print(min_elevation)
        #print(max_elevation)

        for v in _vertices:
            VtkPointId=self.points.InsertNextPoint(v.coordsX[0],v.coordsX[1],v.coordsX[2])
            if _colormap!=None:
                cmap = matplotlib.cm.get_cmap(_colormap)
                val=v.coordsX[2]/(max_elevation-min_elevation)
                r,g,b,a = cmap(val)
            else:
                r,g,b=rgb(min_elevation,max_elevation,v.coordsX[2])
        
            self.Colors.InsertNextTuple3(r*255,g*255,b*255)
            self.vertexId2VtkPointId[v.id]=VtkPointId
            self.VtkPointId2vertexid[VtkPointId]=v.id


    def insert_truss(self,_truss, _type):
        
        self.trusses.InsertNextCell(2)
        self.trusses.InsertCellPoint(self.vertexId2VtkPointId[_truss.vertices[0].id])
        self.trusses.InsertCellPoint(self.vertexId2VtkPointId[_truss.vertices[1].id])

        if _type=="beam":
            self.LineColors.InsertNextTuple3(0,255,0)
        if _type=="column":
            self.LineColors.InsertNextTuple3(0,0,255)
        #print(_truss.vertices[0].id)

    def insert_polygon_as_triangle(self,_beamset):
        self.triangles.InsertNextCell(len(_beamset.vertices))
        for v in _beamset.vertices:
            self.triangles.InsertCellPoint(self.vertexId2VtkPointId[v.id])
    

    def insert_triangle(self,_triangle):
        
        VtkTriangleId=self.triangles.InsertNextCell(3)
        self.triangles.InsertCellPoint(self.vertexId2VtkPointId[_triangle.vertices[0].id])
        self.triangles.InsertCellPoint(self.vertexId2VtkPointId[_triangle.vertices[1].id])
        self.triangles.InsertCellPoint(self.vertexId2VtkPointId[_triangle.vertices[2].id])
        self.VtkTriangleId2Triangleid[VtkTriangleId]=_triangle.id
        self.numberoftriangles+=1
        #print(self.numberoftriangles)
        #self.outfile.write(str(self.numberoftriangles)+"\n")
        
    def insert_triangles(self, _triangles, _checked_items):
        if _checked_items['Terrain']>0:
            for tri in _triangles:
                self.insert_triangle(tri)    

    def insert_beamset(self,_beamset):
        for t in _beamset.beams:
            self.insert_truss(t, "beam")
    
    def insert_column(self,_column):
        for t in _column.trusses:
            self.insert_truss(t, "column")

    def insert_baseset(self,_baseset):
        for t in _baseset.triangles:
            self.insert_triangle(t)

    def insert_wall(self,_wall):
        for t in _wall.triangles:
            self.insert_triangle(t)


    def insert_building(self,_building, _checked_items):
        if _checked_items['Panel Beams']>0:
            for b in _building.beamsets:
                self.insert_beamset(b)
        if _checked_items['Wall Columns']>0:
            for c in _building.columns:
                self.insert_column(c)
        if _checked_items['Panel Facets']>0:
            for bs in _building.basesets:
                self.insert_baseset(bs)
        if _checked_items['Wall Facets']>0:
            for w in _building.walls:
                self.insert_wall(w)
        #for bb in _building.beamsets:
        #self.insert_polygon_as_triangle(_building.beamsets[0])

    def insert_buildings(self,_buildings,_checked_items):
        if _checked_items['Buildings']>0:    
            for b in _buildings.values():
                self.insert_building(b,_checked_items)
            #print(b.name)
            



    '''
    def insert_building_triangle(self,_building):
        
        #for v in _building.vertices:
        #    VtkPointId=self.points.InsertNextPoint(v.coords[0],v.coords[1],v.coords[2])
        #    self.vertexId2VtkPointId[v.id]=VtkPointId

        #print(vertexId2VtkPointId.keys())
        for f in _building.facets:
            triangle = vtk.vtkTriangle()
            for i in range(3):
                triangle.GetPointIds().SetId(i,self.vertexId2VtkPointId[f.vertices[i].id])
            self.triangles.InsertNextCell(triangle)

    def insert_building_truss(self,_building):
        truss_counter=1
        candidate_trusses=[]
        
        for f in _building.facets:
            candidate_trusses.append(trusses.truss(truss_counter,[f.vertices[0],f.vertices[1]]))    
            truss_counter+=1
            candidate_trusses.append(trusses.truss(truss_counter,[f.vertices[1],f.vertices[2]]))
            truss_counter+=1    
            candidate_trusses.append(trusses.truss(truss_counter,[f.vertices[2],f.vertices[1]]))    
            truss_counter+=1
        
        truss_counter=1
        for c in candidate_trusses:
            if c.check_if_beam() or c.check_if_column():
                if not _building.check_truss_contained(c):
                    c.id=truss_counter
                    _building.append_truss(c)
                    truss_counter+=1

        for t in _building.trusses:
            self.trusses.InsertNextCell(2)
            self.trusses.InsertCellPoint(self.vertexId2VtkPointId[t.vertices[0].id])
            self.trusses.InsertCellPoint(self.vertexId2VtkPointId[t.vertices[1].id])

    def insert_buildings_triangle(self,_buildings):
        for b in _buildings:
            self.insert_building_triangle(b)
            #print(b.name)
    '''
    def visualize(self):
        
        _wireframe=True
        if(self.triangles.GetNumberOfCells()==0):
            _wireframe=False


        # start triangles.ss
        self.PolyData.SetPoints(self.points)
        
        self.PolyData.SetPolys(self.triangles)
        #self.PolyData.SetLines(self.trusses)
        
        self.PolyData.GetPointData().SetScalars(self.Colors)

        # mapper
        
        self.mapper.SetInputData(self.PolyData)
        
        self.mapper.Update()
        # actor
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)
        if not _wireframe:
            self.actor.GetProperty().SetRepresentationToWireframe()
        #end triangles



        #start lines
        self.PolyData_Lines.SetPoints(self.points)
        self.PolyData_Lines.SetLines(self.trusses)
        
        self.PolyData_Lines.GetCellData().SetScalars(self.LineColors)
        
        # mapper
        
        self.mapper_Lines.SetInputData(self.PolyData_Lines)
        
        self.mapper_Lines.Update()
        # actor
        self.actor_Lines = vtk.vtkActor()
        self.actor_Lines.SetMapper(self.mapper_Lines)
        if not _wireframe:
            self.actor_Lines.GetProperty().SetRepresentationToWireframe()
        # end lines


        # assign actor to the renderer
        self.ren.AddActor(self.actor)
        self.ren.AddActor(self.actor_Lines)
        self.axes = vtk.vtkAxesActor()


        xAxisLabel = self.axes.GetXAxisCaptionActor2D()#.GetTextActor().SetTextScaleModeToNone()
        xAxisLabel.GetTextActor().SetTextScaleModeToNone()
        xAxisLabel.GetCaptionTextProperty().SetFontSize(10) 
        yAxisLabel = self.axes.GetYAxisCaptionActor2D()#.GetTextActor().SetTextScaleModeToNone()
        yAxisLabel.GetCaptionTextProperty().SetFontSize(10) #
        yAxisLabel.GetTextActor().SetTextScaleModeToNone()
        
        zAxisLabel = self.axes.GetZAxisCaptionActor2D()#.GetTextActor().SetTextScaleModeToNone()
        zAxisLabel.GetCaptionTextProperty().SetFontSize(10) 
        zAxisLabel.GetTextActor().SetTextScaleModeToNone()
         

        self.axes.SetShaftTypeToLine()
        self.axes.SetTotalLength(100, 100, 100)
        self.axes.SetNormalizedShaftLength(1.0, 1.0, 1.0)
        self.axes.SetNormalizedTipLength(0.05, 0.05, 0.05) 

        transform = vtk.vtkTransform()
        transform.Translate(self.origin[0],self.origin[1], 0.0)
        self.axes.SetUserTransform(transform)
        self.ren.AddActor(self.axes)
