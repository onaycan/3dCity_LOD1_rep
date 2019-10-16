import buildings
import vertices
import facets


def parse_objs(objfile, _buildings, _vertices, _facets):
    objlines=objfile.read().splitlines()
    
    vertex_counter=1
    facet_counter=1
    l=0
    while(l<len(objlines)):
        line=objlines[l]
        if line.startswith("v  "): 
            _vertices[vertex_counter]=vertices.vertex(vertex_counter,line.split("v")[1].strip().split())
            vertex_counter+=1
        if line.startswith("f "): 
            facet_vertices=[_vertices[int(v)] for v in line.split("f")[1].strip().split()]
            _facets[facet_counter]=facets.facet(facet_counter,facet_vertices)
            facet_counter+=1
        if line.startswith("o Building"):
            building_name=objlines[l].split("Building")[1].strip()
            _buildings[building_name]=buildings.building(building_name)
            l+=1
            line=objlines[l]
            while(not line.startswith("o")):
                if line.startswith("v  "): 
                    _vertices[vertex_counter]=vertices.vertex(vertex_counter,line.split("v")[1].strip().split())
                    _buildings[building_name].append_vertex(_vertices[vertex_counter])
                    vertex_counter+=1
                if line.startswith("f "): 
                    facet_vertices=[_vertices[int(v)] for v in line.split("f")[1].strip().split()]
                    _facets[facet_counter]=facets.facet(facet_counter,facet_vertices)
                    _buildings[building_name].append_facet(_facets[facet_counter])
                    facet_counter+=1
                    
                l+=1
                line=objlines[l]
        l+=1