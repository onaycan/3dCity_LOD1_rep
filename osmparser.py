import vertices
import trusses
import beamsets
import buildings
import xml.etree.ElementTree as ET

def parse_objs(osmfile,_vertices, _beamsets, _trusses, _buildings):
    #osmlines=osmfile.read()
    delim="##"
    valid_buildings=["building","building:part"]
    tree = ET.parse(osmfile)
    root = tree.getroot()
    #print(root.tag)
    for child in root:
        if child.tag=="node":
            #print(child.attrib["id"])
            _vertices[child.attrib["id"]]=vertices.vertex(child.attrib["id"],[child.attrib["lat"],child.attrib["lon"],0.0])

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
                        for nd in current_node_ids:
                            _beamsets[current_beamset_id].append_vertex(_vertices[nd])
                        for ndid in range(len(current_node_ids)-1):
                            nd_tip=current_node_ids[ndid]
                            nd_tail=current_node_ids[ndid+1]
                            _trusses[current_beamset_id+delim+nd_tip]=trusses.truss(current_beamset_id+delim+nd_tip,[_vertices[nd_tip],_vertices[nd_tail]])
                            _beamsets[current_beamset_id].append_truss(_trusses[current_beamset_id+delim+nd_tip])
                        _buildings[child.attrib["id"]].append_beamset(_beamsets[current_beamset_id])
            if isbuilding:
                _buildings[child.attrib["id"]].assign_attributes(current_attributes)
                        #print(childofchild.attrib["k"],childofchild.attrib["v"])