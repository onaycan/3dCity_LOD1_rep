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

#findig the mid of floors
for b in buildings.values():
    b.set_floor_mid()


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


#zero_beamsets=[build.beamsets[0] for build in buildings.values()]
#misc.elevate_floors_corners(ground_vertices, zero_beamsets)



triangle_or_truss=True
wireframe=False
start_time = time.time()
vtk_interactor=vtk_interaction.vtk_interactor()
elapsed_time = time.time() - start_time
print("interactor needs: "+str(elapsed_time))

vtk_interactor.insert_vertices(vertices.values())
vtk_interactor.insert_vertices(ground_vertices.values())
vtk_interactor.insert_buildings(buildings)
vtk_interactor.insert_triangles(ground_triangles.values())

vtk_interactor.visualize(triangle_or_truss, wireframe, origin)


