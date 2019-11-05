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

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import DesiredCapabilities


def define_city(vtkWidget):
    origin,ground_vertices,ground_triangles=ground.ground_geometry()
    print("origin: "+str(origin))



    #osmfilename="map_inönü_kücükcekmece_mixed.osm"
    #page="https://keos.kucukcekmece.bel.tr/keos/"
    #osmfilename="map_bagcilar_demirkapi.osm"
    #page="https://bbgis.bagcilar.bel.tr/keos/"
    osmfilename="map_kadiköy_caferaga.osm"
    page="https://webgis.kadikoy.bel.tr/keos/"



    mahalle='caferaga'
    vertices={}
    beamsets={}
    trusses={}
    buildings={}
    osmfile=open(os.path.join("OSM_DB",osmfilename),'r', encoding="utf8")
    osmparser.parse_objs(osmfile,vertices,beamsets,trusses,buildings,origin)
    max_home_numbers=max([len(v.homes) for b in beamsets.values() for v in b.vertices])
    print("max number of home buildings sharing the same vertex: "+str(max_home_numbers))


    misc.elevate_floors_corners(ground_vertices, beamsets)

    for b in buildings.values():
        b.set_footprint_max_elev()
    #misc.elevate_floors_mid(ground_vertices,beamsets)
    #up above there are only the base beamsets stored! 



    counter=0
    buildings_dic={}
    buildings_dic[mahalle]={}
    prev_file=open("map_kadiköy_caferaga.json",'r', encoding='utf-8')
    start_time = time.time()
    buildings_dic=json.load(prev_file)
    elapsed_time = time.time() - start_time
    print("json load needs: "+str(elapsed_time))

    last_key=list(buildings_dic[mahalle].keys())[-1]

    for bk in buildings_dic[mahalle].keys():
        buildings[bk].levels=buildings_dic[mahalle][bk]["numberoflevels"]
    #start wo crawling

    #end wo crawling

    start_time = time.time()
    last_vertex_id=max([int(v) for v in vertices.keys()])
    numberofbuildingswithheight=0
    for b in buildings.values():
        numberofbuildingswithheight,last_vertex_id=b.build_building(beamsets,vertices,trusses,numberofbuildingswithheight,last_vertex_id, origin)
    elapsed_time = time.time() - start_time
    print("building needs: "+str(elapsed_time))

    print("number of buildings with height: "+str(numberofbuildingswithheight))

    '''
    #start opensses convertion
    #finding the mid of floors
    femidcounter=1
    for b in buildings.values():
        b.set_floor_mid()
        b.femid=femidcounter
        femidcounter+=1
        b.building2opensees()
    #end opensees convertion

    #print("max: "+str(femidcounter))
    '''

    '''
    vertex_digits=set(len(str(v.id)) for v in vertices.values())

    digits=set()
    for b in buildings.values():
        digits.add(b.building2opensees())

    print(digits)
    print(vertex_digits)
    '''



   
    start_time = time.time()
    vtk_interactor=vtk_interaction.vtk_interactor(vtkWidget)
    elapsed_time = time.time() - start_time
    print("interactor needs: "+str(elapsed_time))

    vtk_interactor.insert_vertices(vertices.values(),_colormap="gray")
    vtk_interactor.insert_vertices(ground_vertices.values(),_colormap="gist_earth")
    vtk_interactor.insert_buildings(buildings)
    vtk_interactor.insert_triangles(ground_triangles.values())

    #triangle_or_truss=True
    #wireframe=False
    #vtk_interactor.visualize(triangle_or_truss, wireframe, origin)
    return vtk_interactor, origin


