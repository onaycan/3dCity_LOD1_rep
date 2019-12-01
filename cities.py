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



class city:

    def __init__(self,_label,_status,_vtkWidget,_osmfilename,_lod1filename):
        self.label=_label
        self.status=_status
        self.vertices={}
        self.beamsets={}
        self.trusses={}
        self.beams={}
        self.columns_and_beams={}
        self.buildings={}
        self.buildingblocks={}
        self.all_triangles={}
        self.origin=[]
        self.ground_vertices={}
        self.ground_triangles={}
        self.vtkWidget=_vtkWidget
        self.osmfilename=_osmfilename
        self.lod1filename=_lod1filename
    
    def build_city(self):
            
        self.origin,self.ground_vertices,self.ground_triangles, nw=ground.ground_geometry()
        print("origin: "+str(self.origin))

        for gi,gv in self.ground_triangles.items():
            self.all_triangles[gi]=gv


        #osmfilename="map_kadiköy_caferaga.osm"



        #mahalle='caferaga'
        self.osmfile=open(os.path.join("OSM_DB",self.osmfilename),'r', encoding="utf8")
        osmparser.parse_objs(self.osmfile,self.vertices,self.beamsets,self.beams,self.buildings,self.origin)
        max_home_numbers=max([len(v.homes) for b in self.beamsets.values() for v in b.vertices])


        # setting the fem id for the ground beams
        columns_and_beams_counter=len(self.columns_and_beams.keys())
        for b in self.beams.values():
            self.columns_and_beams[columns_and_beams_counter]=b
            b.femid=columns_and_beams_counter
            columns_and_beams_counter+=1


        print("max number of home buildings sharing the same vertex: "+str(max_home_numbers))


        misc.elevate_floors_corners(self.ground_vertices, self.beamsets)

        for b in self.buildings.values():
            b.set_footprint_max_elev()


        self.buildings_dic={}
        self.buildings_dic[self.label]={}
        #prev_file=open("map_kadiköy_caferaga.json",'r', encoding='utf-8')
        self.lod1_file=open(self.lod1filename,'r', encoding='utf-8')
        
        start_time = time.time()
        self.buildings_dic=json.load(self.lod1_file)
        elapsed_time = time.time() - start_time
        print("json load needs: "+str(elapsed_time))


        #for bk in self.buildings_dic[self.label].keys():
        #    self.buildings[bk].levels=self.buildings_dic[self.label][bk]["numberoflevels"]

        for bk in self.buildings.keys():
            if bk in self.buildings_dic[self.label].keys():
                self.buildings[bk].levels=self.buildings_dic[self.label][bk]["numberoflevels"]

        start_time = time.time()
        last_vertex_id=max([int(v) for v in self.vertices.keys() if "#" not in v])
        numberofbuildingswithheight=0
        for b in self.buildings.values():
            numberofbuildingswithheight,last_vertex_id=b.build_building(self.beamsets,self.vertices,self.trusses,self.columns_and_beams,self.beams,numberofbuildingswithheight,last_vertex_id, self.origin, self.all_triangles)
        elapsed_time = time.time() - start_time
        print("building needs: "+str(elapsed_time))

        print("number of buildings with height: "+str(numberofbuildingswithheight))

        for v in self.vertices.values():
            v.convert_CoordsX2FemCoordsX(nw)

        for v in self.ground_vertices.values():
            v.convert_CoordsX2FemCoordsX(nw)

        # start assigning homes to vertices and neighbour information and calculation of the floor mids
        for b in self.buildings.values():
            b.assign_homes_to_vertices(self.vertices)

        for b in self.buildings.values():
            neighboursofthis=set()
            b.find_neighbours(self.vertices,self.buildings,neighboursofthis)
            b.neighbours=neighboursofthis

        #set femids for the vertices:
        _femid=1
        self.femid2vertexid={}
        for v in self.vertices.values():
            v.set_fem_id(_femid)
            self.femid2vertexid[str(_femid)]=v.id
            _femid+=1

        last_vertex_femid=max([int(v.femid) for v in self.vertices.values()])
        floorvertices=[]
        dummy_vertex=_vertices.vertex(str(last_vertex_femid+1),[0.0,0.0])
        floorvertices.append(dummy_vertex)
        for b in self.buildings.values():
            b.adoptto_building_blocks(self.buildingblocks,self.buildings)
            b.set_floor_mid(floorvertices)
        # end assigning homes to vertices and neighbour information





    def set_interactor(self):
    
        start_time = time.time()
        self.vtk_interactor=vtk_interaction.vtk_interactor(self.vtkWidget, self.origin)
        elapsed_time = time.time() - start_time
        print("interactor needs: "+str(elapsed_time))

        self.vtk_interactor.insert_building_vertices(self.vertices.values(),_colormap="gray")
        #vtk_interactor.insert_vertices(ground_vertices.values(),_colormap="gist_earth")
        self.vtk_interactor.insert_ground_vertices(self.ground_vertices.values(),_colormap="terrain")
        #vtk_interactor.insert_vertices(ground_vertices.values(),_colormap="CMRmap")

        checked_items={'Building Blocks': 2, 'Buildings': 2, 'Panels': 2, 'Panel Facets': 2, 'Panel Beams': 2, 'Panel Girders': 2, 'Walls': 2, 'Wall Facets': 2, "Wall Columns" : 2, "Terrain" :2}
        self.vtk_interactor.insert_buildings(self.buildings,checked_items)
        print("Buldings are inserted")
        self.vtk_interactor.insert_ground_triangles(self.ground_triangles.values(),checked_items)
        print("Ground Triangles are inserted")
        print("the city has been build")
        #return self.vtk_interactor, self.buildings, self.ground_triangles, self.vertices, self.buildingblocks, self.beams, self.beamsets



    def copy_city(self,_origincity):
        self.vertices=_origincity.vertices
        self.beamsets=_origincity.beamsets
        self.trusses=_origincity.trusses
        self.beams=_origincity.beams
        self.columns_and_beams=_origincity.columns_and_beams
        self.buildings=_origincity.buildings
        self.buildingblocks=_origincity.buildingblocks
        self.all_triangles=_origincity.all_triangles
        self.origin=_origincity.origin
        self.ground_vertices=_origincity.ground_vertices
        self.ground_triangles=_origincity.ground_triangles
        self.femid2vertexid=_origincity.femid2vertexid
    
    def copy_city_interactor_properties(self,_origincity):
        self.vtk_interactor.b_vertexId2VtkPointId=_origincity.vtk_interactor.b_vertexId2VtkPointId