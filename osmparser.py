import vertices
#import trusses
import beams
import beamsets
import buildings
import xml.etree.ElementTree as ET
import numpy as np
import numpy.linalg as la
import math

def py_ang(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'    """
    n_v1=la.norm(v1)
    n_v2=la.norm(v2)
    v1 = v1/n_v1
    v2 = v2/n_v2
    cosang = np.dot(v1, v2)
    sinang = la.norm(np.cross(v1, v2))
    return np.arctan(sinang/cosang)

def parse_objs(osmfile,_vertices, _beamsets, _beams, _buildings,_origin):
    #osmlines=osmfile.read()
    column_interval=15
    delim="##"
    valid_buildings=["building","building:part"]
    tree = ET.parse(osmfile)
    root = tree.getroot()
    #print(root.tag)
    for child in root:
        if child.tag=="node":
            #print(child.attrib["id"])
            _vertices[child.attrib["id"]]=vertices.vertex(child.attrib["id"],[child.attrib["lat"],child.attrib["lon"]])
            _vertices[child.attrib["id"]].convert_lat_long2m(_origin)

    ids=[int(v) for v in _vertices.keys()]
    vertex_id_counter=1+max(ids)

    for child in root: 
        if child.tag=="way":
            #print(child.attrib)
            current_node_ids=[]
            
            current_attributes={}
            isbuilding=False
            for childofchild in child:    
                if childofchild.tag=="nd":
                    current_node_ids.append(childofchild.attrib["ref"])
            for childofchild in child:
                if childofchild.tag=="tag":
                    current_attributes[childofchild.attrib["k"]]=childofchild.attrib["v"]
                    if childofchild.attrib["k"] in valid_buildings and not isbuilding:
                        isbuilding=True # so that you only build once. 
                        _buildings[child.attrib["id"]]=buildings.building(child.attrib["id"])
                        current_beamset_id=child.attrib["id"]+delim+"0"
                        _beamsets[current_beamset_id]=beamsets.beamset(current_beamset_id)
                        current_node_appended_ids=[]
                        max_length=0
                        max_vec=np.zeros(2)
                        #START OF ESTIMATED COLUMNS IMPLEMENTATION
                        for ndid in range(len(current_node_ids)-1):
                            nd_tip=current_node_ids[ndid]
                            nd_tail=current_node_ids[ndid+1]
                            current_node_appended_ids.append(nd_tip)
                            current_length=_vertices[nd_tip].dist_2_another_vertex_in_m(_vertices[nd_tail].coords_lat_long)
                            d_lat=_vertices[nd_tail].coords_lat_long[0]-_vertices[nd_tip].coords_lat_long[0]
                            d_lon=_vertices[nd_tail].coords_lat_long[1]-_vertices[nd_tip].coords_lat_long[1]
                            if(current_length>max_length):
                                max_length=current_length
                                max_vec=np.array([d_lat,d_lon])
                            
                            #print(current_length)
                            number_of_columns_2_inverted=int(int(current_length)/int(column_interval))+1
                            #print(current_length,number_of_columns_2_inverted)
                            if number_of_columns_2_inverted>1:
                                for an in range(number_of_columns_2_inverted-1):
                                    ani=an+1
                                    # id: building id plus delim + tip node id + delim + counter
                                    # this can be used to distinguish in between the intermediate nodes and the counter nodes
                                    thisvertexid=child.attrib["id"]+delim+nd_tip+delim+str(an)
                                    thisvertexkey=str(vertex_id_counter)
                                    vertex_id_counter+=1
                                    thislat=d_lat/number_of_columns_2_inverted*ani+_vertices[nd_tip].coords_lat_long[0]
                                    thislong=d_lon/number_of_columns_2_inverted*ani+_vertices[nd_tip].coords_lat_long[1]
                                    
                                    _vertices[thisvertexkey]=vertices.vertex(thisvertexkey, [thislat,thislong])
                                    _vertices[thisvertexkey].convert_lat_long2m(_origin)
                                    current_node_appended_ids.append(thisvertexkey)
                        current_node_appended_ids.append(nd_tail)


                        #print("start")
                        for nd in current_node_appended_ids: # the start id is twice inside! this may cause problem! 
                            _beamsets[current_beamset_id].append_vertex(_vertices[nd])
                            #print(nd,_vertices[nd].coords_lat_long[0],_vertices[nd].coords_lat_long[1])
                        #print("end")
                        for ndid in range(len(current_node_appended_ids)-1):
                            nd_tip=current_node_appended_ids[ndid]
                            nd_tail=current_node_appended_ids[ndid+1]
                            d_lat=_vertices[nd_tail].coords_lat_long[0]-_vertices[nd_tip].coords_lat_long[0]
                            d_lon=_vertices[nd_tail].coords_lat_long[1]-_vertices[nd_tip].coords_lat_long[1]
                            #BEAM GIRDER DIFF IS APPLIED HERE
                            current_vector=np.array([d_lat,d_lon])
                            angle=py_ang(max_vec,current_vector)
                            #first take the absolute value
                            dangle=math.fabs(angle)*180.0/3.14
                            #print(dangle)
                            if dangle<30:
                                _type="beam"
                            else:
                                _type="girder"
                            _beams[current_beamset_id+delim+nd_tip]=beams.beam(current_beamset_id+delim+nd_tip,[_vertices[nd_tip],_vertices[nd_tail]],_type)
                            _beamsets[current_beamset_id].append_beam(_beams[current_beamset_id+delim+nd_tip])
                        #END OF ESTIMATED COLUMNS IMPLEMENTATION


                        #START ORIGINAL COLUMNS IMPLEMENTATION
                        #for nd in current_node_ids: # the start id is twice inside! this may cause problem! 
                        #    _beamsets[current_beamset_id].append_vertex(_vertices[nd])
                        #for ndid in range(len(current_node_ids)-1):
                        #    nd_tip=current_node_ids[ndid]
                        #    nd_tail=current_node_ids[ndid+1]
                        #    _beams[current_beamset_id+delim+nd_tip]=beams.beam(current_beamset_id+delim+nd_tip,[_vertices[nd_tip],_vertices[nd_tail]])
                        #    _beamsets[current_beamset_id].append_beam(_beams[current_beamset_id+delim+nd_tip])
                        #END ORIGINAL COLUMNS IMPLEMENTATION
                        _buildings[child.attrib["id"]].append_beamset(_beamsets[current_beamset_id])
            if isbuilding:
                _buildings[child.attrib["id"]].assign_attributes(current_attributes)
                        #print(childofchild.attrib["k"],childofchild.attrib["v"])