import misc



class facet:
    def __init__(self,_id,_vertices):
        self.id=_id
        self.vertices=[]
        for i in range(3):
            self.vertices.append(_vertices[i])
            _vertices[i].append_facetid(id)
        
        
        self.normal=[]
        v1=[self.vertices[0].coords[0]-self.vertices[1].coords[0],self.vertices[0].coords[1]-self.vertices[1].coords[1],self.vertices[0].coords[2]-self.vertices[1].coords[2]]
        v2=[self.vertices[1].coords[0]-self.vertices[2].coords[0],self.vertices[1].coords[1]-self.vertices[2].coords[1],self.vertices[1].coords[2]-self.vertices[2].coords[2]]
        self.normal=misc.cross_product(v1,v2)
