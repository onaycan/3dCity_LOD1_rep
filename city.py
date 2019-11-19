import objparser
import osmparser
import pprint
import vtk_interaction
import os
import time
import requests
import json
import ground
import numpy as np
import misc
import vertices as _vertices

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import DesiredCapabilities


def define_city(vtkWidget):
    vertices={}
    beamsets={}
    trusses={}
    beams={}
    columns_and_beams={}
    buildings={}
    buildingblocks={}
    all_triangles={}
    origin,ground_vertices,ground_triangles, nw=ground.ground_geometry()
    print("origin: "+str(origin))

    for gi,gv in ground_triangles.items():
        all_triangles[gi]=gv

    debugfile=open("debugfile.inp", 'w')

    #osmfilename="map_inönü_kücükcekmece_mixed.osm"
    #page="https://keos.kucukcekmece.bel.tr/keos/"
    #osmfilename="map_bagcilar_demirkapi.osm"
    #page="https://bbgis.bagcilar.bel.tr/keos/"
    osmfilename="map_kadiköy_caferaga.osm"
    page="https://webgis.kadikoy.bel.tr/keos/"



    mahalle='caferaga'
    osmfile=open(os.path.join("OSM_DB",osmfilename),'r', encoding="utf8")
    osmparser.parse_objs(osmfile,vertices,beamsets,beams,buildings,origin)
    max_home_numbers=max([len(v.homes) for b in beamsets.values() for v in b.vertices])
    

    # setting the fem id for the ground beams
    columns_and_beams_counter=len(columns_and_beams.keys())
    for b in beams.values():
        columns_and_beams[columns_and_beams_counter]=b
        b.femid=columns_and_beams_counter
        columns_and_beams_counter+=1


    print("max number of home buildings sharing the same vertex: "+str(max_home_numbers))


    misc.elevate_floors_corners(ground_vertices, beamsets)

    for b in buildings.values():
        b.set_footprint_max_elev()
    #misc.elevate_floors_mid(ground_vertices,beamsets)
    #up above there are only the base beamsets stored! 



    buildings_dic={}
    buildings_dic[mahalle]={}
    prev_file=open("map_kadiköy_caferaga.json",'r', encoding='utf-8')
    start_time = time.time()
    buildings_dic=json.load(prev_file)
    elapsed_time = time.time() - start_time
    print("json load needs: "+str(elapsed_time))

    
    for bk in buildings_dic[mahalle].keys():
        buildings[bk].levels=buildings_dic[mahalle][bk]["numberoflevels"]


    start_time = time.time()
    last_vertex_id=max([int(v) for v in vertices.keys() if "#" not in v])
    numberofbuildingswithheight=0
    for b in buildings.values():
        numberofbuildingswithheight,last_vertex_id=b.build_building(beamsets,vertices,trusses,columns_and_beams,beams,numberofbuildingswithheight,last_vertex_id, origin, all_triangles)
    elapsed_time = time.time() - start_time
    print("building needs: "+str(elapsed_time))

    print("number of buildings with height: "+str(numberofbuildingswithheight))

    for v in vertices.values():
        v.convert_CoordsX2FemCoordsX(nw)
    
    for v in ground_vertices.values():
        v.convert_CoordsX2FemCoordsX(nw)

    # start assigning homes to vertices and neighbour information and calculation of the floor mids
    for b in buildings.values():
        b.assign_homes_to_vertices(vertices)
    
    for b in buildings.values():
        neighboursofthis=set()
        b.find_neighbours(vertices,buildings,neighboursofthis)
        b.neighbours=neighboursofthis
    
    #set femids for the vertices:
    _femid=1
    for v in vertices.values():
        v.set_fem_id(_femid)
        _femid+=1
    
    last_vertex_femid=max([int(v.femid) for v in vertices.values()])
    floorvertices=[]
    dummy_vertex=_vertices.vertex(str(last_vertex_femid+1),[0.0,0.0])
    floorvertices.append(dummy_vertex)
    for b in buildings.values():
        b.adoptto_building_blocks(buildingblocks,buildings)
        b.set_floor_mid(floorvertices)
    # end assigning homes to vertices and neighbour information
    
    




   
    start_time = time.time()
    vtk_interactor=vtk_interaction.vtk_interactor(vtkWidget, origin)
    elapsed_time = time.time() - start_time
    print("interactor needs: "+str(elapsed_time))

    vtk_interactor.insert_building_vertices(vertices.values(),_colormap="gray")
    #vtk_interactor.insert_vertices(ground_vertices.values(),_colormap="gist_earth")
    vtk_interactor.insert_ground_vertices(ground_vertices.values(),_colormap="terrain")
    #vtk_interactor.insert_vertices(ground_vertices.values(),_colormap="CMRmap")
    
    checked_items={'Building Blocks': 2, 'Buildings': 2, 'Panels': 2, 'Panel Facets': 2, 'Panel Beams': 2, 'Panel Girders': 2, 'Walls': 2, 'Wall Facets': 2, "Wall Columns" : 2, "Terrain" :2}
    vtk_interactor.insert_buildings(buildings,checked_items)
    print("Buldings are inserted")
    vtk_interactor.insert_ground_triangles(ground_triangles.values(),checked_items)
    print("Ground Triangles are inserted")
    return vtk_interactor, buildings, ground_triangles, vertices, buildingblocks, beams, beamsets


