import vertices
#import trusses
import beams
import beamsets
import buildings
import xml.etree.ElementTree as ET

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
                        #START OF ESTIMATED COLUMNS IMPLEMENTATION
                        for ndid in range(len(current_node_ids)-1):
                            nd_tip=current_node_ids[ndid]
                            nd_tail=current_node_ids[ndid+1]
                            current_node_appended_ids.append(nd_tip)
                            current_length=_vertices[nd_tip].dist_2_another_vertex_in_m(_vertices[nd_tail].coords_lat_long)
                            d_lat=_vertices[nd_tail].coords_lat_long[0]-_vertices[nd_tip].coords_lat_long[0]
                            d_lon=_vertices[nd_tail].coords_lat_long[1]-_vertices[nd_tip].coords_lat_long[1]
                            #print(current_length)
                            number_of_columns_2_inverted=int(int(current_length)/int(column_interval))+1
                            #print(current_length,number_of_columns_2_inverted)
                            #_beamsets[current_beamset_id].append_vertex(_vertices[nd_tip])
                            if number_of_columns_2_inverted>1:
                                for an in range(number_of_columns_2_inverted-1):
                                    ani=an+1
                                    # id: building id plus delim + tip node id + delim + counter
                                    thisvertexid=child.attrib["id"]+delim+nd_tip+delim+str(an)
                                    thislat=d_lat/number_of_columns_2_inverted*ani+_vertices[nd_tip].coords_lat_long[0]
                                    thislong=d_lon/number_of_columns_2_inverted*ani+_vertices[nd_tip].coords_lat_long[1]
                                    _vertices[thisvertexid]=vertices.vertex(thisvertexid, [thislat,thislong])
                                    _vertices[thisvertexid].convert_lat_long2m(_origin)
                                    current_node_appended_ids.append(thisvertexid)
                        current_node_appended_ids.append(nd_tail)


                        #print("start")
                        for nd in current_node_appended_ids: # the start id is twice inside! this may cause problem! 
                            _beamsets[current_beamset_id].append_vertex(_vertices[nd])
                            #print(nd,_vertices[nd].coords_lat_long[0],_vertices[nd].coords_lat_long[1])
                        #print("end")
                        for ndid in range(len(current_node_appended_ids)-1):
                            nd_tip=current_node_appended_ids[ndid]
                            nd_tail=current_node_appended_ids[ndid+1]
                            _beams[current_beamset_id+delim+nd_tip]=beams.beam(current_beamset_id+delim+nd_tip,[_vertices[nd_tip],_vertices[nd_tail]])
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