import vtk
import trusses
import vertices
import columns
import matplotlib
import math


def mkVtkIdList(it):
    vil = vtk.vtkIdList()
    for i in it:
        vil.InsertNextId(int(i))
    return vil

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
            
                print("number of building triangles: "+str(self.vtkinteractor.building_triangles.GetNumberOfCells()))
                
                self.spressed=False
                clickPos = self.GetInteractor().GetEventPosition()
                picker = vtk.vtkCellPicker()
                picker.Pick(clickPos[0], clickPos[1], 0, self.vtkinteractor.ren)
                #picker.Pick(clickPos[0], clickPos[1], 0, self.GetDefaultRenderer())

                #cellid=picker.GetSubId()
                cellid=picker.GetCellId()
                print("selected cell id: "+str(cellid))
                #cellid=picker.GetFlatBlockIndex()

                print("selected cell id: "+str(cellid))

                numberofids=self.vtkinteractor.PolyData_BuildingCells.GetCell(cellid).GetPointIds().GetNumberOfIds()
                pointids=[]
                facetids=[]

                sets=[]
                notground=True
                for p in range(numberofids):
                    pid=self.vtkinteractor.PolyData_BuildingCells.GetCell(cellid).GetPointIds().GetId(p)
                    if self.vtkinteractor.b_VtkPointId2vertexid[pid].startswith("g"):
                        notground=False
                    else:
                        sets.append(self.vertices[self.vtkinteractor.b_VtkPointId2vertexid[pid]].homes)

                if notground:
                    self.building_vertices=set()
                    self.building_facets=set()

                    common_home=[set.intersection(*sets)][0] #in fact this is buggy.but you can not choose really a side wall or bottom triangle with common edge without being able to see it 
                    common_home=list(common_home)[0]
                    self.window.comboboxes['Buildings'].addItem(common_home)
                    self.window.comboboxes['Buildings'].setCurrentIndex(self.window.comboboxes['Buildings'].count() - 1)

                    self.get_building_vertices(common_home)
                    self.get_building_facets(common_home)


                    if self.window.buildingBlocks_pushbutton.isChecked():
                        self.window.comboboxes['Building Blocks'].addItem(self.buildings[common_home].buildingblock_id)
                        self.window.comboboxes['Building Blocks'].setCurrentIndex(self.window.comboboxes['Building Blocks'].count() - 1)
                        for n in self.buildings[common_home].neighbours:
                            self.window.comboboxes['Buildings'].addItem(n)
                            self.window.comboboxes['Buildings'].setCurrentIndex(self.window.comboboxes['Buildings'].count() - 1)
                            self.get_building_facets(n)
                            #for bb in self.buildings[n].beamsets:
                            #    for v in bb.vertices:
                            #        self.building_vertices.add(v.id)

                    #self.window.fill_table_widget()
                    self.window.append_pushbutton.setEnabled(True)


                    for pid in self.building_vertices:
                        pointids.append(self.vtkinteractor.b_vertexId2VtkPointId[pid])

                    for fid in self.building_facets:
                        facetids.append(self.vtkinteractor.b_TriangleId2VtkTriangleid[fid])




                    print("points of selected cell: "+ str(pointids))
                    #for p in pointids:
                    #    self.vtkinteractor.BuildingColors.SetTuple3(p,255,0,0)
                    for f in facetids:
                        #print("cell to be colored: "+str(f))
                        self.vtkinteractor.BuildingCellColors.SetTuple3(int(f),255,0,0)
                        
                    #print(self.vtkinteractor.building_triangles.GetNumberOfCells())
                    self.vtkinteractor.PolyData_BuildingCells.GetCellData().SetScalars(self.vtkinteractor.BuildingCellColors)
                    #this update kills! 
                    #self.vtkinteractor.mapper_BuildingCells.Update()
                    #self.vtkinteractor.PolyData_BuildingCells.GetPointData().SetScalars(self.vtkinteractor.BuildingColors)
                    self.vtkinteractor.mapper_BuildingCells.ScalarVisibilityOff()
                    self.vtkinteractor.mapper_BuildingCells.ScalarVisibilityOn()
                    self.vtkinteractor.renWin.Render()
                
        self.OnLeftButtonDown()
        return 
    
    def get_building_vertices(self,_home):
        b=_home
        print("home is selected: "+str(b))
        for bb in range(1,len(self.buildings[b].beamsets)):
            for v in self.buildings[b].beamsets[bb].vertices:
                self.building_vertices.add(v.id)

    def get_building_facets(self,_home):
        b=_home
        print("home is selected: "+str(b))
        for bs in range(0,len(self.buildings[b].basesets)):
            for f in self.buildings[b].basesets[bs].triangles:
                self.building_facets.add(f.id)
        for w in range(0,len(self.buildings[b].walls)):
            for f in self.buildings[b].walls[w].triangles:
                self.building_facets.add(f.id)


class vtk_interactor:
    def __init__(self, vtkWidget, _origin):
        self.outfile=open("debugfile.out",'w')

        self.origin=_origin
        # create a rendering window and renderer
        self.ren = vtk.vtkRenderer()
        self.bren = vtk.vtkRenderer()
        #vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        #self.renWin = vtk.vtkRenderWindow()
        self.renWin=vtkWidget.GetRenderWindow()
        self.renWin.AddRenderer(self.ren)
        
        # create a renderwindowinteractor
        #self.iren = vtk.vtkRenderWindowInteractor()
        self.iren=vtkWidget.GetRenderWindow().GetInteractor()

        #self.iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        self.iren.SetRenderWindow(self.renWin)
        self.PolyData_BuildingCells = vtk.vtkPolyData()
        self.PolyData_GroundCells = vtk.vtkPolyData()
        self.PolyData_Lines = vtk.vtkPolyData()
        
        #self.PolyData=vtk.vtkExtractPolyDataGeometry()
        self.Colors = vtk.vtkUnsignedCharArray()
        self.Colors.SetNumberOfComponents(3)
        self.Colors.SetName("Colors")

        self.BuildingColors = vtk.vtkUnsignedCharArray()
        self.BuildingColors.SetNumberOfComponents(3)
        self.BuildingColors.SetName("BuildingColors")


        self.LineColors = vtk.vtkUnsignedCharArray()
        self.LineColors.SetNumberOfComponents(3)
        self.LineColors.SetName("LineColors")

        self.BuildingCellColors = vtk.vtkUnsignedCharArray()
        self.BuildingCellColors.SetNumberOfComponents(3)
        self.BuildingCellColors.SetName("BuildingCellColors")

        

        

        self.ground_points = vtk.vtkPoints()
        self.ground_triangles = vtk.vtkCellArray()

        self.building_points = vtk.vtkPoints()
        self.building_triangles = vtk.vtkCellArray()


        self.numberoftriangles=0
        self.trusses = vtk.vtkCellArray()
        
        self.mapper_BuildingCells = vtk.vtkPolyDataMapper()
        self.mapper_GroundCells = vtk.vtkPolyDataMapper()
        self.mapper_Lines = vtk.vtkPolyDataMapper()
        
        self.b_vertexId2VtkPointId={}
        self.b_VtkPointId2vertexid={}
        
        self.g_vertexId2VtkPointId={}
        self.g_VtkPointId2vertexid={}
        

        self.b_VtkTriangleId2Triangleid={} 
        self.g_VtkTriangleId2Triangleid={}

        self.b_TriangleId2VtkTriangleid={} 
        self.g_TriangleId2VtkTriangleid={}
        

        self.LineColorLabels={}
        self.LineColorLabels['Panel Beams']=[0,0,150]
        self.LineColorLabels['Panel Girders']=[100,0,150]
        self.LineColorLabels['Wall Columns']=[0,150,0]

        self.BuildingColorLabels={}
        self.BuildingColorLabels['Panel Facets']=[0,100,150]
        self.BuildingColorLabels['Wall Facets']=[0,150,100]
        
        

    def insert_building_vertices(self,_vertices, _colormap=None):
        min_elevation=min([v.coordsX[1] for v in _vertices])
        max_elevation=max([v.coordsX[1] for v in _vertices])
        print("min elevation: "+str(min_elevation))
        print("max elevation: "+str(max_elevation))

        for v in _vertices:
            VtkPointId=self.building_points.InsertNextPoint(v.coordsX[0],v.coordsX[1],v.coordsX[2])
            if _colormap!=None:
                cmap = matplotlib.cm.get_cmap(_colormap)
                val=(v.coordsX[1]-min_elevation)/(max_elevation-min_elevation)
                r,g,b,a = cmap(val)
            else:
                r,g,b=rgb(min_elevation,max_elevation,v.coordsX[1])
            self.BuildingColors.InsertNextTuple3(r*255,g*255,b*255)
            self.b_vertexId2VtkPointId[v.id]=VtkPointId
            self.b_VtkPointId2vertexid[VtkPointId]=v.id



    def insert_ground_vertices(self,_vertices, _colormap=None):
        min_elevation=min([v.coordsX[1] for v in _vertices])
        max_elevation=max([v.coordsX[1] for v in _vertices])
        print("min elevation: "+str(min_elevation))
        print("max elevation: "+str(max_elevation))

        for v in _vertices:
            VtkPointId=self.ground_points.InsertNextPoint(v.coordsX[0],v.coordsX[1],v.coordsX[2])
            if _colormap!=None:
                cmap = matplotlib.cm.get_cmap(_colormap)
                val=(v.coordsX[1]-min_elevation)/(max_elevation-min_elevation)
                #if val<0 and val>-0.01:
                #    val=0
                #if val>0.01 and val<0.2:
                #    val=0.2
                r,g,b,a = cmap(val*3)
            else:
                r,g,b=rgb(min_elevation,max_elevation,v.coordsX[1])
        
            self.Colors.InsertNextTuple3(r*255,g*255,b*255)
            self.g_vertexId2VtkPointId[v.id]=VtkPointId
            self.g_VtkPointId2vertexid[VtkPointId]=v.id


    def insert_truss(self,_truss, _type, _only_colors):
        if not _only_colors:
            self.trusses.InsertNextCell(2)
            self.trusses.InsertCellPoint(self.b_vertexId2VtkPointId[_truss.vertices[0].id])
            self.trusses.InsertCellPoint(self.b_vertexId2VtkPointId[_truss.vertices[1].id])

            if _type=="beam":
                self.LineColors.InsertNextTuple3(self.LineColorLabels['Panel Beams'][0],self.LineColorLabels['Panel Beams'][1],self.LineColorLabels['Panel Beams'][2])
            if _type=="girder":
                self.LineColors.InsertNextTuple3(self.LineColorLabels['Panel Girders'][0],self.LineColorLabels['Panel Girders'][1],self.LineColorLabels['Panel Girders'][2])
            if _type=="column":
                self.LineColors.InsertNextTuple3(self.LineColorLabels['Wall Columns'][0],self.LineColorLabels['Wall Columns'][1],self.LineColorLabels['Wall Columns'][2])
        else:
            if _type=="beam":
                self.LineColors.InsertNextTuple3(self.LineColorLabels['Panel Beams'][0],self.LineColorLabels['Panel Beams'][1],self.LineColorLabels['Panel Beams'][2])
            if _type=="girder":
                self.LineColors.InsertNextTuple3(self.LineColorLabels['Panel Girders'][0],self.LineColorLabels['Panel Girders'][1],self.LineColorLabels['Panel Girders'][2])
            if _type=="column":
                self.LineColors.InsertNextTuple3(self.LineColorLabels['Wall Columns'][0],self.LineColorLabels['Wall Columns'][1],self.LineColorLabels['Wall Columns'][2])
        #print(_truss.vertices[0].id)

    #def insert_polygon_as_triangle(self,_beamset):
    #    self.triangles.InsertNextCell(len(_beamset.vertices))
    #    for v in _beamset.vertices:
    #        self.triangles.InsertCellPoint(self.vertexId2VtkPointId[v.id])
    
    def insert_building_triangle(self,_triangle, _type, _only_colors):
        if not _only_colors:
            VtkTriangleId=self.building_triangles.InsertNextCell(3)
            self.building_triangles.InsertCellPoint(self.b_vertexId2VtkPointId[_triangle.vertices[0].id])
            self.building_triangles.InsertCellPoint(self.b_vertexId2VtkPointId[_triangle.vertices[1].id])
            self.building_triangles.InsertCellPoint(self.b_vertexId2VtkPointId[_triangle.vertices[2].id])
            
            self.b_VtkTriangleId2Triangleid[VtkTriangleId]=_triangle.id

            self.b_TriangleId2VtkTriangleid[_triangle.id]=VtkTriangleId
            #self.outfile.write(str(_triangle.id)+"\t"+str(VtkTriangleId)+"\n")
            #self.numberoftriangles+=1
            if _type=="panel":
                self.BuildingCellColors.InsertNextTuple3(self.BuildingColorLabels['Panel Facets'][0],self.BuildingColorLabels['Panel Facets'][1],self.BuildingColorLabels['Panel Facets'][2])
            if _type=="wall":
                self.BuildingCellColors.InsertNextTuple3(self.BuildingColorLabels['Wall Facets'][0],self.BuildingColorLabels['Wall Facets'][1],self.BuildingColorLabels['Wall Facets'][2])
        else:
            if _type=="panel":
                self.BuildingCellColors.InsertNextTuple3(self.BuildingColorLabels['Panel Facets'][0],self.BuildingColorLabels['Panel Facets'][1],self.BuildingColorLabels['Panel Facets'][2])
            if _type=="wall":
                self.BuildingCellColors.InsertNextTuple3(self.BuildingColorLabels['Wall Facets'][0],self.BuildingColorLabels['Wall Facets'][1],self.BuildingColorLabels['Wall Facets'][2])



    def insert_ground_triangle(self,_triangle):
        
        VtkTriangleId=self.ground_triangles.InsertNextCell(3)
        self.ground_triangles.InsertCellPoint(self.g_vertexId2VtkPointId[_triangle.vertices[0].id])
        self.ground_triangles.InsertCellPoint(self.g_vertexId2VtkPointId[_triangle.vertices[1].id])
        self.ground_triangles.InsertCellPoint(self.g_vertexId2VtkPointId[_triangle.vertices[2].id])
        self.g_VtkTriangleId2Triangleid[VtkTriangleId]=_triangle.id
        #self.numberoftriangles+=1
        #print(self.numberoftriangles)
        #self.outfile.write(str(self.numberoftriangles)+"\n")
        
    def insert_ground_triangles(self, _triangles, _checked_items):
        if _checked_items['Terrain']>0:
            for tri in _triangles:
                self.insert_ground_triangle(tri)    

    def insert_beamset(self,_beamset, _prefered_type, _only_colors):
        for t in _beamset.beams:
            if t._type==_prefered_type:
                self.insert_truss(t, t._type, _only_colors)
 
    def insert_column(self,_column, _only_colors):
        for t in _column.trusses:
            self.insert_truss(t, "column", _only_colors)

    def insert_baseset(self,_baseset,_only_colors):
        for t in _baseset.triangles:
            self.insert_building_triangle(t,"panel",_only_colors)

    def insert_wall(self,_wall,_only_colors):
        for t in _wall.triangles:
            self.insert_building_triangle(t,"wall",_only_colors)


    def insert_building(self,_building, _checked_items, _only_colors):
        if _checked_items['Panel Beams']>0:
            for b in _building.beamsets:
                self.insert_beamset(b,"beam", _only_colors)
        if _checked_items['Panel Girders']>0:
            for b in _building.beamsets:
                self.insert_beamset(b,"girder", _only_colors)
        if _checked_items['Wall Columns']>0:
            for c in _building.columns:
                self.insert_column(c, _only_colors)
        if _checked_items['Panel Facets']>0:
            for bs in _building.basesets:
                self.insert_baseset(bs,_only_colors)
        if _checked_items['Wall Facets']>0:
            for w in _building.walls:
                self.insert_wall(w,_only_colors)
        #for bb in _building.beamsets:
        #self.insert_polygon_as_triangle(_building.beamsets[0])

    def insert_buildings(self,_buildings,_checked_items, _only_colors=False):
        if _checked_items['Buildings']>0:    
            for b in _buildings.values():
                self.insert_building(b,_checked_items, _only_colors)
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
        if(self.ground_triangles.GetNumberOfCells()==0 and self.building_triangles.GetNumberOfCells()==0):
            _wireframe=False


        # START TRIANGLES OF BUILDINGS
        self.PolyData_BuildingCells.SetPoints(self.building_points)
        self.PolyData_BuildingCells.SetPolys(self.building_triangles)
        #self.PolyData_BuildingCells.GetPointData().SetScalars(self.BuildingColors)
        self.PolyData_BuildingCells.GetCellData().SetScalars(self.BuildingCellColors)
        self.mapper_BuildingCells.SetInputData(self.PolyData_BuildingCells)
        self.mapper_BuildingCells.ScalarVisibilityOn()
        self.mapper_BuildingCells.Update()
        self.actor_BuildingCells = vtk.vtkActor()
        self.actor_BuildingCells.SetMapper(self.mapper_BuildingCells)
        self.actor_BuildingCells.GetProperty().SetRepresentationToSurface()
        if not _wireframe:
            self.actor_BuildingCells.GetProperty().SetRepresentationToWireframe()
        # START TRIANGLES OF BUILDINGS
        print("actor of building triangles are finished")


        # START TRIANGLES OF GROUND
        self.PolyData_GroundCells.SetPoints(self.ground_points)
        self.PolyData_GroundCells.SetPolys(self.ground_triangles)
        self.PolyData_GroundCells.GetPointData().SetScalars(self.Colors)
        self.mapper_GroundCells.SetInputData(self.PolyData_GroundCells)
        self.mapper_GroundCells.Update()
        self.actor_GroundCells = vtk.vtkActor()
        self.actor_GroundCells.SetMapper(self.mapper_GroundCells)
        if not _wireframe:
            self.actor_GroundCells.GetProperty().SetRepresentationToWireframe()
        # START TRIANGLES OF GROUND
        print("actor of ground triangles are finished")



        #START BULDING LINES
        self.PolyData_Lines.SetPoints(self.building_points)
        self.PolyData_Lines.SetLines(self.trusses)
        self.PolyData_Lines.GetCellData().SetScalars(self.LineColors)
        self.mapper_Lines.SetInputData(self.PolyData_Lines)
        self.mapper_Lines.Update()
        self.actor_Lines = vtk.vtkActor()
        self.actor_Lines.SetMapper(self.mapper_Lines)
        if not _wireframe:
            self.actor_Lines.GetProperty().SetRepresentationToWireframe()
        #END BUILDING LINES
        print("actor of building lines are finished")


        # assign actor to the renderer
        self.ren.AddActor(self.actor_BuildingCells)
        self.ren.AddActor(self.actor_GroundCells)
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
        # this is necessary for osm
        transform.Translate(self.origin[0],0.0, -1.0*self.origin[1])
        self.axes.SetUserTransform(transform)
        self.ren.AddActor(self.axes)
        print("all actors are added to renderer")
