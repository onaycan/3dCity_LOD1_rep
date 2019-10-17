
import vertices
import trusses

class beamset:
    def __init__(self,_id):
        self.id=_id
        self.vertices=[]
        self.trusses=[]
    def append_vertex(self,_vertex):
        self.vertices.append(_vertex)
    def append_truss(self,_truss):
        self.trusses.append(_truss)        
    def shift_and_copy_beamset(self,_vertices,_trusses, _level, _shift, _last_vertex_id):
        delim="##"
        #last_vertex_id=max([int(v) for v in _vertices.keys()])
        #print(last_vertex_id)
        return_beamset_id=self.id.split(delim)[0]+delim+_level
        return_beamset=beamset(return_beamset_id)
        copied_vertex_ids=[]
        for v in self.vertices:
            new_coords=[0.0,0.0,0.0]
            for c in range(3):
                new_coords[c]=v.coords[c]+_shift[c]
            _vertices[str(_last_vertex_id+1)]=vertices.vertex(str(_last_vertex_id+1),new_coords)
            copied_vertex_ids.append(str(_last_vertex_id+1))
            return_beamset.append_vertex(_vertices[str(_last_vertex_id+1)])
            _last_vertex_id+=1
        for ndid in range(len(copied_vertex_ids)-1):
            nd_tip=copied_vertex_ids[ndid]
            nd_tail=copied_vertex_ids[ndid+1]
            #print(_vertices[nd_tip].id)
            _trusses[self.id+delim+nd_tip]=trusses.truss(self.id+delim+nd_tip,[_vertices[nd_tip],_vertices[nd_tail]])
            return_beamset.append_truss(_trusses[self.id+delim+nd_tip])
        
        return return_beamset, _last_vertex_id



        
             