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




class vtk_interactor:
    def __init__(self):

        # create a rendering window and renderer
        self.ren = vtk.vtkRenderer()
        self.renWin = vtk.vtkRenderWindow()
        self.renWin.AddRenderer(self.ren)

        # create a renderwindowinteractor
        self.iren = vtk.vtkRenderWindowInteractor()
        self.iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        self.iren.SetRenderWindow(self.renWin)

        self.points = vtk.vtkPoints()
        self.triangles = vtk.vtkCellArray()
        self.trusses = vtk.vtkCellArray()
        
        
        
        self.mapper = vtk.vtkPolyDataMapper()

        self.PolyData = vtk.vtkPolyData()

        self.vertexId2VtkPointId={}
        self.Colors = vtk.vtkUnsignedCharArray()
        self.Colors.SetNumberOfComponents(3)
        self.Colors.SetName("Colors")
    

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


    def insert_truss(self,_truss):
        
        self.trusses.InsertNextCell(2)
        self.trusses.InsertCellPoint(self.vertexId2VtkPointId[_truss.vertices[0].id])
        self.trusses.InsertCellPoint(self.vertexId2VtkPointId[_truss.vertices[1].id])
        #print(_truss.vertices[0].id)

    def insert_polygon_as_triangle(self,_beamset):
        self.triangles.InsertNextCell(len(_beamset.vertices))
        for v in _beamset.vertices:
            self.triangles.InsertCellPoint(self.vertexId2VtkPointId[v.id])
    

    def insert_triangle(self,_triangle):
        self.triangles.InsertNextCell(3)
        self.triangles.InsertCellPoint(self.vertexId2VtkPointId[_triangle.vertices[0].id])
        self.triangles.InsertCellPoint(self.vertexId2VtkPointId[_triangle.vertices[1].id])
        self.triangles.InsertCellPoint(self.vertexId2VtkPointId[_triangle.vertices[2].id])
        
    def insert_triangles(self, _triangles):
        for tri in _triangles:
            self.insert_triangle(tri)    

    def insert_beamset(self,_beamset):
        for t in _beamset.trusses:
            self.insert_truss(t)
    
    def insert_column(self,_column):
        for t in _column.trusses:
            self.insert_truss(t)

    def insert_baseset(self,_baseset):
        for t in _baseset.triangles:
            self.insert_triangle(t)

    def insert_wall(self,_wall):
        for t in _wall.triangles:
            self.insert_triangle(t)


    def insert_building(self,_building):
        for b in _building.beamsets:
            self.insert_beamset(b)
        for c in _building.columns:
            self.insert_column(c)
        for bs in _building.basesets:
            self.insert_baseset(bs)
        for w in _building.walls:
            self.insert_wall(w)
        #for bb in _building.beamsets:
        #self.insert_polygon_as_triangle(_building.beamsets[0])

    def insert_buildings(self,_buildings):
        for b in _buildings.values():
            self.insert_building(b)
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
    def visualize(self,_triangle_or_truss, _wireframe, _origin):
        
        self.PolyData.SetPoints(self.points)
        
        self.PolyData.SetPolys(self.triangles)
        self.PolyData.SetLines(self.trusses)
        
        self.PolyData.GetPointData().SetScalars(self.Colors)

        # mapper
        if vtk.VTK_MAJOR_VERSION <= 5:
            self.mapper.SetInput(self.PolyData)
        else:
            self.mapper.SetInputData(self.PolyData)

        # actor
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)
        if _wireframe:
            self.actor.GetProperty().SetRepresentationToWireframe()

        # assign actor to the renderer
        self.ren.AddActor(self.actor)
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
        transform.Translate(_origin[0],_origin[1], 0.0)
        self.axes.SetUserTransform(transform)
        self.ren.AddActor(self.axes)


        # enable user interface interactor
        self.iren.Initialize()
        self.renWin.Render()
        self.iren.Start()