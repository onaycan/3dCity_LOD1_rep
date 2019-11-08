from geopy.distance import geodesic

class vertex:
    def __init__(self,_id,_coords_lat_long):
        self.id=_id
        self.coords_lat_long=[]
        self.coordsX=[0.0]*3
        self.coords_lat_long.append(float(_coords_lat_long[0]))#lat
        self.coords_lat_long.append(float(_coords_lat_long[1]))#long
        #self.homes=[]
        self.homes=set()
        #self.coords.append(float(_coords[2]))#dummy
        self.facetids=[]
    def append_facetid(self,_id):
        self.facetids.append(_id)

    def convert_lat_long2m(self, _origin):

        x_origin=(self.coords_lat_long[0],_origin[1])
        x_target=(self.coords_lat_long[0],self.coords_lat_long[1])
        self.coordsX[0]=geodesic(x_origin, x_target).meters        

        y_origin=(_origin[0],self.coords_lat_long[1])
        y_target=(self.coords_lat_long[0],self.coords_lat_long[1])
        self.coordsX[1]=geodesic(y_origin, y_target).meters      
