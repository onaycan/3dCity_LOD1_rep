from geopy.distance import geodesic
import math

class vertex:
    def __init__(self,_id,_coords_lat_long):
        self.id=_id
        self.coords_lat_long=[]
        self.coordsX=[0.0]*3
        self.coordsx=[]
        self.coords_lat_long.append(float(_coords_lat_long[0]))#lat
        self.coords_lat_long.append(float(_coords_lat_long[1]))#long
        #self.homes=[]
        self.homes=set()
        #self.coords.append(float(_coords[2]))#dummy
        self.facetids=[]
        self.results={}
    def append_facetid(self,_id):
        self.facetids.append(_id)

    def set_result(self,_resultname,_result):
        self.results[_resultname]=_result
        #for t in range(len(_result["time"])):
        #    self.coordsx[t][0]=_result["xDisp"][t]+self.coordsX[0]
        #    self.coordsx[t][1]=_result["yDisp"][t]+self.coordsX[1]
        #    self.coordsx[t][2]=_result["zDisp"][t]+self.coordsX[2]
        #print(self.id)
        #print(":\n")
        #print(_result)
    def set_fem_id(self,_femid):
        self.femid=_femid

    def convert_lat_long2m(self, _origin):

        x_origin=(self.coords_lat_long[0],_origin[1])
        x_target=(self.coords_lat_long[0],self.coords_lat_long[1])
        self.coordsX[0]=geodesic(x_origin, x_target).meters      
        

        y_origin=(_origin[0],self.coords_lat_long[1])
        y_target=(self.coords_lat_long[0],self.coords_lat_long[1])
        self.coordsX[1]=geodesic(y_origin, y_target).meters      
        


    def dist_2_another_vertex_in_m(self, _origin):

        x_origin=(self.coords_lat_long[0],_origin[1])
        x_target=(self.coords_lat_long[0],self.coords_lat_long[1])
        retx=geodesic(x_origin, x_target).meters        

        y_origin=(_origin[0],self.coords_lat_long[1])
        y_target=(self.coords_lat_long[0],self.coords_lat_long[1])
        rety=geodesic(y_origin, y_target).meters      

        return math.sqrt(retx*retx+rety*rety)

    def convert_CoordsX2FemCoordsX(self,nw):
        old_CoordsX_x=self.coordsX[0]
        old_CoordsX_y=self.coordsX[1]
        old_CoordsX_z=self.coordsX[2]

        #self.coordsX[0]=old_CoordsX_y
        #self.coordsX[1]=-1*old_CoordsX_z
        #self.coordsX[2]=-1*old_CoordsX_x
               

        self.coordsX[0]=old_CoordsX_x
        self.coordsX[1]=old_CoordsX_z
        self.coordsX[2]=-1.0*old_CoordsX_y+nw
