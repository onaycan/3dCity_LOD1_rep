import os
import buildings
import vertices
import trusses
from itertools import combinations


class buildingblock:
    def __init__(self,_id):
        self.id=_id
        self.buildings=[]


        #pounding objects
        self.extranodes={}
        self.constrain_els={}
        self.impact_els={}
        self.zerolengt_els={}
        
        #this name should be equal in building block as well
        self.femvertexids=set()


    def set_buildingblock_femvertexids(self):
        for b in self.buildings:
            for bsi in range(0,len(b.beamsets)):
                bs=b.beamsets[bsi]
                for vi in range(0,len(bs.vertices)-1):
                    if len(bs.vertices[vi].home_columns)==0:
                        print("ANNNNNNNAANANASSSKA")
                    v=bs.vertices[vi].femid
                    self.femvertexids.add(v)

    def append_building(self,_building):
        self.buildings.append(_building)

    
    def define_single_pounding_pair(self, max_vertex_id, max_el_id, v1, v2):
        self.extranodes[max_vertex_id+1]=[(v1.coordsX[0]+v2.coordsX[0])*0.5,(v1.coordsX[1]+v2.coordsX[1])*0.5,(v1.coordsX[2]+v2.coordsX[2])*0.5]
        firstnode_femid=max_vertex_id+1
        max_vertex_id+=1
        self.extranodes[max_vertex_id+1]=[(v1.coordsX[0]+v2.coordsX[0])*0.5,(v1.coordsX[1]+v2.coordsX[1])*0.5,(v1.coordsX[2]+v2.coordsX[2])*0.5]
        secondnode_femid=max_vertex_id+1
        max_vertex_id+=1

        self.constrain_els[max_el_id+1]=[v1.femid, firstnode_femid]
        max_el_id+=1
        self.constrain_els[max_el_id+1]=[v2.femid, secondnode_femid]
        max_el_id+=1
        self.impact_els[max_el_id+1]=[firstnode_femid,secondnode_femid]
        max_el_id+=1
        #self.impact_els[max_el_id+1]=[firstnode_femid,secondnode_femid]
        #max_el_id+=1
        self.zerolengt_els[max_el_id+1]=[firstnode_femid,secondnode_femid]
        max_el_id+=1
        #self.zerolengt_els[max_el_id+1]=[firstnode_femid,secondnode_femid]
        #max_el_id+=1
        
        return max_vertex_id, max_el_id


    def configure_pounding(self, _allvertices):

        max_native_vertex_id=max([v.femid for b in self.buildings for bs in b.beamsets for v in bs.vertices])
        max_mid_vertex_id=max([int(b.beamsets[bsi].mid_vertex.id) for b in self.buildings for bsi in range(1,len(b.beamsets))])
        max_vertex_id=max(max_native_vertex_id,max_mid_vertex_id)
        max_beam_or_girder_id=max([be.femid for b in self.buildings for bs in b.beamsets for be in bs.beams])
        max_column_id=max([c.femid for b in self.buildings for c in b.columns])
        max_el_id=max(max_beam_or_girder_id,max_column_id)

        #print(max_vertex_id, max_el_id)

        current_bb_pair_sets={}


        buildings_of_this={}
        for b in self.buildings:
            buildings_of_this[b.name]=b
            b.pounding_building=True

        for b in self.buildings:
            found=b.beamsets[0]
            for vi in range(len(found.vertices)-1):
                v=found.vertices[vi]
                vid=found.vertices[vi].id
                if(len(v.homes)>1):
                    for h in v.homes:
                        if h!=b.name:
                            min_storeys=min(len(b.beamsets),len(buildings_of_this[h].beamsets))
                            vcis=[vci for vci in range(len(buildings_of_this[h].beamsets[0].vertices)-1) if buildings_of_this[h].beamsets[0].vertices[vci].id==vid]
                            vci=vcis[0]
                            for s in range(1, min_storeys):
                                #print(vi,len(buildings_of_this[h].beamsets[s].vertices))
                                b.beamsets[s].vertices[vi].pounding_counter_vs.add(buildings_of_this[h].beamsets[s].vertices[vci].id)
                                buildings_of_this[h].beamsets[s].vertices[vci].pounding_counter_vs.add(b.beamsets[s].vertices[vi].id)

        for b in self.buildings:
            for bsi in range(1, len(b.beamsets)):
                bs=b.beamsets[bsi]
                for vi in range(len(bs.vertices)-1):
                    v=bs.vertices[vi]
                    if len(v.pounding_counter_vs)>0:
                        current_set=set()
                        current_set.add(v.id)
                        for vid in v.pounding_counter_vs:
                            current_set.add(vid)
                        current_set=sorted(current_set)
                        current_bb_pair_sets[str(current_set)]=current_set

        for s in current_bb_pair_sets.keys():
            combs=combinations(current_bb_pair_sets[s],2)
            for comb in combs:
                #print(comb[0], comb[1])
                max_vertex_id, max_el_id=self.define_single_pounding_pair(max_vertex_id, max_el_id, _allvertices[comb[0]], _allvertices[comb[1]])
            #print(current_bb_pair_sets[s])
        
    def print_pounding_file(self, _dir):
        meter2inches=39.3701
        precision=4
        current_file=open(_dir+"\\POUNDING_"+self.id+".tcl", 'w')
        

        current_file.write("#EXTRANODES\n")
        for nid, n in self.extranodes.items():
            printed=[]
            printed.append(round(n[0]*meter2inches,precision))
            printed.append(round(n[1]*meter2inches,precision))
            printed.append(round(n[2]*meter2inches,precision))
            current_file.write("node"+"\t"+str(nid)+"\t"+str(printed[0])+"\t"+str(printed[1])+"\t"+str(printed[2])+"\n") 

        current_file.write("#CONSTRAINTS\n")
        for eid, e in self.constrain_els.items():
            current_file.write("constraint"+"\t"+str(e[0])+"\t"+str(e[1])+"\n") 
        

        current_file.write("#ZEROLENGTHIMPACT ELEMENTS\n")
        for eid, e in self.impact_els.items():
            current_file.write("impact"+"\t"+str(eid)+"\t"+str(e[0])+"\t"+str(e[1])+"\t1""\n") 

        current_file.write("#ZEROLENGTHELEMENTS\n")
        for eid, e in self.zerolengt_els.items():
            current_file.write("element"+"\t"+str(eid)+"\t"+str(e[0])+"\t"+str(e[1])+"\n") 
        current_file.write("#END\n")
        
        for b in self.buildings:
            inputpath=_dir+"/b_"+str(b.name)
            os.makedirs(inputpath, exist_ok=True)
            b.print_simulation_file(inputpath+"/"+"INPUT_"+b.name+".tcl")


             #self.extranodes={}
             #self.constrain_els={}
             #self.impact_els={}
             #self.zerolengt_els={}