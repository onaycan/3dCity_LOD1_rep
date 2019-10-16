import vtk
import trusses
import vertices
import columns

def rgb(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
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
    

    def insert_all_vertices(self,_vertices):
        min_elevation=min([v.coords[2] for v in _vertices])
        max_elevation=max([v.coords[2] for v in _vertices])
        print(min_elevation)
        print(max_elevation)

        for v in _vertices:
            VtkPointId=self.points.InsertNextPoint(v.coords[0],v.coords[1],v.coords[2])
            r,g,b=rgb(min_elevation,30,v.coords[1])
            self.Colors.InsertNextTuple3(r,g,b)
            self.vertexId2VtkPointId[v.id]=VtkPointId

    def insert_truss(self,_truss):
        
        self.trusses.InsertNextCell(2)
        self.trusses.InsertCellPoint(self.vertexId2VtkPointId[_truss.vertices[0].id])
        self.trusses.InsertCellPoint(self.vertexId2VtkPointId[_truss.vertices[1].id])
        #print(_truss.vertices[0].id)

    def insert_triangle(self,_triangle):
        self.triangles.InsertNextCell(3)
        self.triangles.InsertCellPoint(self.vertexId2VtkPointId[_triangle.vertices[0].id])
        self.triangles.InsertCellPoint(self.vertexId2VtkPointId[_triangle.vertices[1].id])
        self.triangles.InsertCellPoint(self.vertexId2VtkPointId[_triangle.vertices[2].id])
        

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
    def visualize(self,_triangle_or_truss, _wireframe):
        
        self.PolyData.SetPoints(self.points)
        
        self.PolyData.SetPolys(self.triangles)
        self.PolyData.SetLines(self.trusses)
        
        #self.PolyData.GetPointData().SetScalars(self.Colors)

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

        # enable user interface interactor
        self.iren.Initialize()
        self.renWin.Render()
        self.iren.Start()