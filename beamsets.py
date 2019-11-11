
import vertices
import beams
import numpy as np

class beamset:
    def __init__(self,_id):
        self.id=_id
        self.vertices=[]
        self.beams=[]
    def append_vertex(self,_vertex):
        self.vertices.append(_vertex)
    def append_beam(self,_beam):
        self.beams.append(_beam)
    def set_floor_mid(self):
        all_coords=np.array([]).reshape(0,3)
        for v in range(len(self.vertices)-1):
            ver=self.vertices[v]
            all_coords=np.vstack([all_coords,[ver.coordsX[0],ver.coordsX[1],ver.coordsX[2]]])
        self.mid=np.mean(all_coords,axis=0)
        return self.mid
    def set_footprint_max_elev(self):
        self.fp_max_elev=max([v.coordsX[2] for v in self.vertices])
        return self.fp_max_elev
    def shift_and_copy_beamset(self,_vertices,_beams, _level, _shift, _last_vertex_id,_origin):
        delim="##"
        #last_vertex_id=max([int(v) for v in _vertices.keys()])
        #print(last_vertex_id)
        return_beamset_id=self.id.split(delim)[0]+delim+_level
        return_beamset=beamset(return_beamset_id)
        copied_vertex_ids=[]
        for v in self.vertices:
            new_coords_lat_long=[0.0,0.0]
            for c in range(2):
                new_coords_lat_long[c]=v.coords_lat_long[c]
            _vertices[str(_last_vertex_id+1)]=vertices.vertex(str(_last_vertex_id+1),new_coords_lat_long)
            for c in range(2):
                _vertices[str(_last_vertex_id+1)].coordsX[c]=v.coordsX[c]
            _vertices[str(_last_vertex_id+1)].coordsX[2]=self.fp_max_elev
            for c in range(3):
                _vertices[str(_last_vertex_id+1)].coordsX[c]+=_shift[c]
            copied_vertex_ids.append(str(_last_vertex_id+1))
            return_beamset.append_vertex(_vertices[str(_last_vertex_id+1)])
            _last_vertex_id+=1
        for ndid in range(len(copied_vertex_ids)-1):
            nd_tip=copied_vertex_ids[ndid]
            nd_tail=copied_vertex_ids[ndid+1]
            _beams[self.id+delim+nd_tip]=beams.beam(self.id+delim+nd_tip,[_vertices[nd_tip],_vertices[nd_tail]])
            return_beamset.append_beam(_beams[self.id+delim+nd_tip])
        
        return return_beamset, _last_vertex_id



        
             