

class vertex:
    def __init__(self,_id,_coords):
        self.id=_id
        self.coords=[]
        self.coords.append(float(_coords[0]))
        self.coords.append(float(_coords[1]))
        self.coords.append(float(_coords[2]))
        self.facetids=[]
    def append_facetid(self,_id):
        self.facetids.append(_id)