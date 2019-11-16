
import vertices
import triangles

class baseset:
    def __init__(self,_id):
        self.id=_id
        self.vertices=[]
        self.triangles=[]
    def append_vertex(self,_vertex):
        self.vertices.append(_vertex)
    def append_triangle(self,_triangle):
        self.triangles.append(_triangle)        
    
import math



class beam:
    def __init__(self,_id,_vertices):
        self.id=_id
        self.vertices=[]
        self.vertices.append(_vertices[0])
        self.vertices.append(_vertices[1])
        self.dir=[]
        for i in range(3):
            self.dir.append(self.vertices[1].coordsX[i]-self.vertices[0].coordsX[i])
    #def dot_product(self, _anytruss):
    #    return math.sqrt(self.dir[0]*_anytruss.dir[0]+self.dir[1]*_anytruss.dir[1]+self.dir[2]*_anytruss.dir[2])
    #def check_if_beam(self):
    #    returnvalue=False
    #    if self.dir[1]==0.0:
    #        returnvalue=True
    #    return returnvalue
    #def check_if_column(self):
    #    returnvalue=False
    #    if self.dir[0]==0.0 and self.dir[2]==0:
    #        returnvalue=True
    #    return returnvalue
    #def check_if_edge(self):
        

        
             

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



        
             
import buildings



class buildingblock:
    def __init__(self,_id):
        self.id=_id
        self.buildings=[]

    def append_building(self,_building):
        self.buildings.append(_building)
import geocoder
import numpy as np
import time
import columns
import trusses
import basesets
import triangles
import basesets
import buildingblocks
import walls
import misc

import geopy
from geopy.geocoders import Nominatim
from geopy.geocoders import GeocodeFarm
from geopy.exc import GeocoderTimedOut
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from scipy.spatial import Delaunay




class building:
    def __init__(self,_name):
        self.name=_name
        self.femid=0
        self.buildingblock_id=None
        self.beamsets=[]
        self.basesets=[]
        self.columns=[]
        self.walls=[]
        self.attributes={}
        self.neighbours=set()
        self.osm_feasible=False
        self.levels="NotFound"

        self.buildingname=''
        self.sitename=''
        self.aciklama=""
        self.groundarea=0.0
        
    def append_beamset(self,_beamset):
        self.beamsets.append(_beamset)
    def assign_attributes(self,_attributes):
        self.attributes=_attributes

    def print_building(self,_intersection):
        printstr=self.name
        for i in _intersection:
            printstr+=" "+i+"="+self.attributes[i]
        print(printstr)

    def set_feasibility(self,_necessary_information):
        if "building:part" not in self.attributes.keys():
            intersection=set(_necessary_information).intersection(set(self.attributes.keys()))
            if len(intersection)>0:
                self.osm_feasible=True
                #self.print_building(intersection)
    
    def set_floor_mid(self):
        self.mid=self.beamsets[0].set_floor_mid()
        for bs in range(1,len(self.beamsets)):
            self.beamsets[bs].set_floor_mid()

    def set_footprint_max_elev(self):
        self.fp_max_elev=self.beamsets[0].set_footprint_max_elev()

    def assign_homes_to_vertices(self,_vertices):
        for bs in self.beamsets:
            for v in bs.vertices:
                _vertices[v.id].homes.add(self.name)

    def find_neighbours(self, _vertices,_buildings, _neighboursofthis):
        for bs in self.beamsets:
            for v in bs.vertices:
                for h in _vertices[v.id].homes:
                    if h not in _neighboursofthis:
                        #self.neighbours.add(h)
                        _neighboursofthis.add(h)
                        _buildings[h].find_neighbours(_vertices, _buildings, _neighboursofthis)

    def adoptto_building_blocks(self,_building_blocks, _buildings):
        if self.buildingblock_id==None:
            current_bb_id="bb"+str(len(_building_blocks.keys()))
            _building_blocks[current_bb_id]=buildingblocks.buildingblock(current_bb_id)
            _building_blocks[current_bb_id].append_building(self)
            self.buildingblock_id=current_bb_id
            for bb in self.neighbours:
                _building_blocks[current_bb_id].append_building(_buildings[bb])
                _buildings[bb].buildingblock_id=current_bb_id







    def get_building_level(self,_driver,_action):
        time.sleep(1)
        #araclar_tab=_driver.find_element_by_xpath("//a[@title='AraÃ§lar']")
        araclar_tab=_driver.find_element_by_xpath("//a[@title='Ã‡izim']")
        time.sleep(4)
        araclar_tab.click()
        nokta_tab=_driver.find_element_by_xpath("//i[@title='Nokta Ã‡iz']")
        time.sleep(2)
        nokta_tab.click()
        option=_driver.find_element_by_xpath("//option[@data-i18n='COGRAFIED50']")
        option.click()
        #they wrote the fields wrong
        y_coord_field=_driver.find_element_by_xpath("//input[@id='_pskgoXCoord']")
        y_coord_field.clear()
        y_coord_field.send_keys(str(self.lon))
        x_coord_field=_driver.find_element_by_xpath("//input[@id='_pskgoYCoord']")
        x_coord_field.clear()
        x_coord_field.send_keys(str(self.lat))
        
        git=_driver.find_element_by_xpath("//a[@data-i18n='araclar.koordinatekle']")
        time.sleep(2)
        git.click()


        nokta_bilgisi=git=_driver.find_element_by_xpath("//i[@class='icon-nokta-bilgisi']")
        nokta_bilgisi.click()
        time.sleep(2)

        target=_driver.find_element_by_xpath("//div[@class='ol-overlay-container ol-selectable']")
        time.sleep(2)
        target.click()
        #_action.move_to_element(target).perform()

        drob_down_menu=_driver.find_element_by_xpath("//i[@class='icon-arama-sonuclari']")
        time.sleep(2)

        yapi_cand=drob_down_menu.find_elements_by_xpath("//div[@class='_ncresult-list-title']")
        time.sleep(2)

        for yapi in yapi_cand:
            #print(yapi.text)
            if "YapÄ±" in yapi.text:
                yapi.click()
                break
            
            
        _driver.switch_to_default_content()
        time.sleep(2)
        mainframe=_driver.find_element_by_xpath("//iframe[@autoresize='1']")
        time.sleep(2)
        _driver.switch_to.frame(mainframe)
        names=_driver.find_elements_by_id("string")
        time.sleep(2)
        self.buildingname=names[0].text
        self.sitename=names[1].text
        self.aciklama=names[2].text
        
        names=_driver.find_elements_by_id("real")
        self.levels=names[0].text
        self.groundarea=names[1].text

        _driver.switch_to_default_content()
        #this wait should be long enough. it was simply killing every 100 times the server, refresh difficult with close of driver. 
        time.sleep(1)
        _driver.find_element_by_xpath("//i[@class='icon-temizle']").click()
        time.sleep(2)





    def get_address_and_level(self,_buildings_dic_m,_driver,_action, _mahalle, _building_counter, _restarted):
        
        lats=[v.coords[0] for v in self.beamsets[0].vertices]
        lons=[v.coords[1] for v in self.beamsets[0].vertices]
        self.lat=np.mean(lats)
        self.lon=np.mean(lons)
        self.address="inÃ¶nÃ¼"
        #geocode was not working well
        geolocator = Nominatim()
        try:
            self.address=geolocator.reverse([self.lat,self.lon])
        except:
            pass
        #except GeocoderTimedOut:
        #    pass
        
        #print("trying for: "+str(self.address))
        print("trying to get the adress")
        try:
            self.get_building_level(_driver,_action)
        except:
            return True
            #pass
            #restart_driver(_driver,_action,_restarted)
        #else:
        _buildings_dic_m[self.name]={}
        _buildings_dic_m[self.name]["mid_lat"]=self.lat
        _buildings_dic_m[self.name]["mid_lon"]=self.lon
        _buildings_dic_m[self.name]["address"]=str(self.address)
        _buildings_dic_m[self.name]["numberoflevels"]=self.levels
        _buildings_dic_m[self.name]["buildingname"]=self.buildingname
        _buildings_dic_m[self.name]["sitename"]=self.sitename
        _buildings_dic_m[self.name]["groundarea"]=self.groundarea
        #print("finished: "+str(self.address)+" levels: "+self.levels)#+" coords: "+str([self.lat,self.lon]))
        print("finished: "+self.name+" levels: "+self.levels)
        print("\n")
        #print(self.levels)
        #print(self.lat)
        #print(self.lon)
        #if _building_counter==0 or _restarted:
        #    checkboxes=_driver.find_elements_by_xpath("//input[@type='checkbox']")
        #    time.sleep(2)
        #    for cb in checkboxes:
        #        try:
        #            cb.click()
        #            print("clicked for simplification")
        #        except:
        #            pass
        #            print("passed bec. not possible to click")
        #        time.sleep(1)
        return False
            


    def build_building(self,_beamsets,_vertices,_trusses,_beams,_numberofbuildingswithheight, _lastvertexid, _origin, _all_triangles):
        triangle_counter=len(_all_triangles.keys())
        delim="##"
        retval=_numberofbuildingswithheight
        floor_height=16.0/5.0
        if self.levels.isdigit():
            if int(self.levels)>0:
                #print("here")
                numberoflevels=int(self.levels)
                for l in range(1,numberoflevels+1):
                    #print("beamset inserted in "+self.name)
                    next_beamset, _lastvertexid=self.beamsets[0].shift_and_copy_beamset(_vertices,_beams, str(l), [0.0,0.0,l*floor_height], _lastvertexid, _origin)
                    #next_beamset, _lastvertexid=self.beamsets[0].shift_and_copy_beamset(_vertices,_beams, str(l), [0.0,l*floor_height,0.0], _lastvertexid, _origin)
                    
                    _beamsets[next_beamset.id]=next_beamset
                    self.beamsets.append(next_beamset)
                    


                    
                    #start columns
                    current_column=columns.column(self.name)
                    both_vertices=self.beamsets[l-1].vertices+self.beamsets[l-1].vertices
                    current_column.vertices=both_vertices
                    for v in range(len(self.beamsets[l-1].vertices)):
                        #this id plus from which stage to which, and the corner counter
                        truss_id=self.name+delim+str(l-1)+delim+str(l)+delim+str(v)
                        current_truss=trusses.truss(truss_id,[self.beamsets[l-1].vertices[v],self.beamsets[l].vertices[v]])
                        _trusses[truss_id]=current_truss
                        current_column.append_truss(current_truss)
                    self.columns.append(current_column)
                    #end columns

                    #start walls
                    current_wall=walls.wall(self.name+delim+str(l))
                    for v in range(0,len(self.beamsets[l-1].vertices)-1):
                        numberofvertices=len(self.beamsets[l-1].vertices)
                        current_vertices=[self.beamsets[l-1].vertices[v],self.beamsets[l-1].vertices[int((v+1)%numberofvertices)],self.beamsets[l].vertices[int((v+1)%numberofvertices)]]
                        current_triangle=triangles.triangle(self.name+delim+str(l)+delim+str(self.beamsets[l-1].vertices[v].id+delim+"0"),current_vertices,triangle_counter)
                        triangle_counter+=1
                        current_wall.append_triangle(current_triangle)
                        current_wall.append_vertex(self.beamsets[l-1].vertices[1])
                        current_wall.append_vertex(self.beamsets[l-1].vertices[int((v+1)%numberofvertices)])
                        current_wall.append_vertex(self.beamsets[l].vertices[int((v+1)%numberofvertices)])

                        current_vertices=[self.beamsets[l-1].vertices[v],self.beamsets[l].vertices[v],self.beamsets[l].vertices[int((v+1)%numberofvertices)]]
                        current_triangle=triangles.triangle(self.name+delim+str(l)+delim+str(self.beamsets[l-1].vertices[v].id+delim+"1"),current_vertices,triangle_counter)
                        triangle_counter+=1
                        current_wall.append_triangle(current_triangle)
                        current_wall.append_vertex(self.beamsets[l-1].vertices[1])
                        current_wall.append_vertex(self.beamsets[l].vertices[v])
                        current_wall.append_vertex(self.beamsets[l].vertices[int((v+1)%numberofvertices)])
                    self.walls.append(current_wall)
                    #end wall

                l=0
                current_baseset=basesets.baseset(self.name+delim+str(l))
                points=np.array([]).reshape(0,2)
                ground_triangles={}
                ground_vertices={}
                coun=0
                for v in range(len(self.beamsets[l].vertices)-1):
                    ver=self.beamsets[l].vertices[v]
                    points=np.vstack([points,[ver.coordsX[0],ver.coordsX[1]]])
                    
                    ground_vertices["g"+str(coun)]=ver
                    current_baseset.append_vertex(ver)
                    coun+=1
                #su aritma tesisleri
                #if (self.name=="236167025"):
                #    print(points)
                tris, ret=misc.constrained_polygon_triangulation(points)
                coun=0
                if ret:
                    for tri in tris:
                        ground_triangles["t"+str(coun)]=triangles.triangle("t"+str(coun),[ground_vertices["g"+str(tri[0])],ground_vertices["g"+str(tri[1])],ground_vertices["g"+str(tri[2])]],triangle_counter)
                        triangle_counter+=1
                        current_baseset.append_triangle(ground_triangles["t"+str(coun)])
                        coun+=1
                    self.basesets.append(current_baseset)
                #other floors:
                for l in range(1,len(self.beamsets)):
                    current_baseset=basesets.baseset(self.name+delim+str(l))
                    ground_triangles={}
                    ground_vertices={}
                    coun=0
                    for v in range(len(self.beamsets[l].vertices)-1):
                        ver=self.beamsets[l].vertices[v]
                        points=np.vstack([points,[ver.coordsX[0],ver.coordsX[1]]])
                        ground_vertices["g"+str(coun)]=ver
                        current_baseset.append_vertex(ver)
                        coun+=1
                    coun=0
                    if ret:
                        for tri in tris:
                            ground_triangles["t"+str(coun)]=triangles.triangle("t"+str(coun),[ground_vertices["g"+str(tri[0])],ground_vertices["g"+str(tri[1])],ground_vertices["g"+str(tri[2])]],triangle_counter)
                            triangle_counter+=1
                            current_baseset.append_triangle(ground_triangles["t"+str(coun)])
                            coun+=1
                        self.basesets.append(current_baseset)

                    #end basesets
                    
                   
                retval=_numberofbuildingswithheight+1
        return retval, _lastvertexid
    
    def building2opensees(self):
        file=open("./OpenSeesFiles/building_"+str(self.name)+".tcl","w")
        file.write("#BUILDING"+"\n")
        file.write("set BuildingID "+str(self.name)+";"+"\n")
        level=0
        file.write("#NODES"+"\n")
        for bs in self.beamsets:
            level+=1
            vertex_counter=1
            file.write("#NODES OF FLOOR # "+str(level)+"\n")
            for vi in range(len(bs.vertices)-1):
                v=bs.vertices[vi]
                current_id=str(level)+str(self.femid).zfill(5)+str(vertex_counter).zfill(2)  
                vertex_counter+=1
                file.write("node\t"+current_id+"\t"+str(v.coordsX[0])+"\t"+str(v.coordsX[2])+"\t"+str(v.coordsX[1])+"\n")
        level=0
        file.write("#MASTERNODES"+"\n")
        for bs in self.beamsets:
            level+=1
            vertex_counter=2
            if level>1:
                current_id=str(99)+str(self.femid).zfill(5)+str(vertex_counter).zfill(2)
                vertex_counter+=1
                file.write("node\t"+current_id+"\t"+str(v.coordsX[0])+"\t"+str(v.coordsX[2])+"\t"+str(v.coordsX[1])+"\n")
        level=0
        file.write("#RIGIDELEMENTS"+"\n")
        for bs in self.beamsets:
            level+=1
            if level>1:
                current_id=str(99)+str(self.femid).zfill(5)+str(level).zfill(2)
                vertex_counter=1
                str2print="rigidDiaphragm 2\t"+current_id+"\t"
                for vi in range(len(bs.vertices)-1):
                    v=bs.vertices[vi]
                    vertex_id=str(level)+str(self.femid).zfill(5)+str(vertex_counter).zfill(2) 
                    str2print+=vertex_id+"\t"
                    vertex_counter+=1
                file.write(str2print+"\n")

                
                
        file.close()
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
    vertices={}
    beamsets={}
    trusses={}
    beams={}
    buildings={}
    buildingblocks={}
    all_triangles={}
    origin,ground_vertices,ground_triangles=ground.ground_geometry()
    print("origin: "+str(origin))
    all_triangles=ground_triangles

    debugfile=open("debugfile.inp", 'w')

    #osmfilename="map_inÃ¶nÃ¼_kÃ¼cÃ¼kcekmece_mixed.osm"
    #page="https://keos.kucukcekmece.bel.tr/keos/"
    #osmfilename="map_bagcilar_demirkapi.osm"
    #page="https://bbgis.bagcilar.bel.tr/keos/"
    osmfilename="map_kadikÃ¶y_caferaga.osm"
    page="https://webgis.kadikoy.bel.tr/keos/"



    mahalle='caferaga'
    osmfile=open(os.path.join("OSM_DB",osmfilename),'r', encoding="utf8")
    osmparser.parse_objs(osmfile,vertices,beamsets,beams,buildings,origin)
    max_home_numbers=max([len(v.homes) for b in beamsets.values() for v in b.vertices])
    
    


    print("max number of home buildings sharing the same vertex: "+str(max_home_numbers))


    misc.elevate_floors_corners(ground_vertices, beamsets)

    for b in buildings.values():
        b.set_footprint_max_elev()
    #misc.elevate_floors_mid(ground_vertices,beamsets)
    #up above there are only the base beamsets stored! 



    buildings_dic={}
    buildings_dic[mahalle]={}
    prev_file=open("map_kadikÃ¶y_caferaga.json",'r', encoding='utf-8')
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
        numberofbuildingswithheight,last_vertex_id=b.build_building(beamsets,vertices,trusses,beams,numberofbuildingswithheight,last_vertex_id, origin, all_triangles)
    elapsed_time = time.time() - start_time
    print("building needs: "+str(elapsed_time))

    print("number of buildings with height: "+str(numberofbuildingswithheight))

    for v in vertices.values():
        v.convert_CoordsX2FemCoordsX()
    
    for v in ground_vertices.values():
        v.convert_CoordsX2FemCoordsX()

    # start assigning homes to vertices and neighbour information
    for b in buildings.values():
        b.assign_homes_to_vertices(vertices)
    
    for b in buildings.values():
        neighboursofthis=set()
        b.find_neighbours(vertices,buildings,neighboursofthis)
        b.neighbours=neighboursofthis
    
    for b in buildings.values():
        b.adoptto_building_blocks(buildingblocks,buildings)
    # end assigning homes to vertices and neighbour information
    




   
    start_time = time.time()
    vtk_interactor=vtk_interaction.vtk_interactor(vtkWidget, origin)
    elapsed_time = time.time() - start_time
    print("interactor needs: "+str(elapsed_time))

    vtk_interactor.insert_building_vertices(vertices.values(),_colormap="gray")
    #vtk_interactor.insert_vertices(ground_vertices.values(),_colormap="gist_earth")
    vtk_interactor.insert_ground_vertices(ground_vertices.values(),_colormap="terrain")
    #vtk_interactor.insert_vertices(ground_vertices.values(),_colormap="CMRmap")
    
    checked_items={'Building Blocks': 2, 'Buildings': 2, 'Panels': 2, 'Panel Facets': 2, 'Panel Beams': 2, 'Walls': 2, 'Wall Facets': 2, "Wall Columns" : 2, "Terrain" :2}
    vtk_interactor.insert_buildings(buildings,checked_items)
    print("Buldings are inserted")
    vtk_interactor.insert_ground_triangles(ground_triangles.values(),checked_items)
    print("Ground Triangles are inserted")
    return vtk_interactor, buildings, ground_triangles, vertices, buildingblocks, beams, beamsets



import vertices
import trusses

class column:
    def __init__(self,_id):
        self.id=_id
        self.vertices=[]
        self.trusses=[]
    def append_vertex(self,_vertex):
        self.vertices.append(_vertex)
    def append_truss(self,_truss):
        self.trusses.append(_truss)        
    
import misc



class facet:
    def __init__(self,_id,_vertices):
        self.id=_id
        self.vertices=[]
        for i in range(3):
            self.vertices.append(_vertices[i])
            _vertices[i].append_facetid(id)
        
        
        self.normal=[]
        v1=[self.vertices[0].coords[0]-self.vertices[1].coords[0],self.vertices[0].coords[1]-self.vertices[1].coords[1],self.vertices[0].coords[2]-self.vertices[1].coords[2]]
        v2=[self.vertices[1].coords[0]-self.vertices[2].coords[0],self.vertices[1].coords[1]-self.vertices[2].coords[1],self.vertices[1].coords[2]-self.vertices[2].coords[2]]
        self.normal=misc.cross_product(v1,v2)
import numpy as np
from scipy.spatial import Delaunay
import vertices
import triangles
import vtk_interaction

def ground_geometry():
    number_of_triangles=0
    origin=[]
    ground_vertices={}
    ground_triangles={}    

    with open("elevations/elevations.txt",'r') as f:
        lines=f.read().splitlines()
        coun=0
        for l in lines:
            current_coords_lat_long=l.split()
            temp=current_coords_lat_long[0]
            current_coords_lat_long[0]=current_coords_lat_long[1]
            current_coords_lat_long[1]=temp
            ground_vertices["g"+str(coun)]=vertices.vertex("g"+str(coun),current_coords_lat_long)
            ground_vertices["g"+str(coun)].coordsX[2]=float(current_coords_lat_long[2])
            coun+=1 
            

    for i in range(2):
        origin.append(min([v.coords_lat_long[i] for v in ground_vertices.values()]))

    for gv in ground_vertices.values():
        gv.convert_lat_long2m(origin)

    points=np.array([]).reshape(0,2)    
    for ver in ground_vertices.values():
        points=np.vstack([points,[ver.coordsX[0],ver.coordsX[1]]])    


    coun=0
    trigls = Delaunay(points)
    for tri in trigls.simplices:
        #print(tri)
        ground_triangles["gt"+str(coun)]=triangles.triangle("gt"+str(coun),[ground_vertices["g"+str(tri[0])],ground_vertices["g"+str(tri[1])],ground_vertices["g"+str(tri[2])]],number_of_triangles)
        number_of_triangles+=1
        coun+=1

    return origin,ground_vertices,ground_triangles
#print(trigls.simplices)
#
#triangle_or_truss=True
#wireframe=True
#vtk_interactor=vtk_interaction.vtk_interactor()
#vtk_interactor.insert_all_vertices(ground_vertices.values())
#for t in ground_triangles.values():
#    vtk_interactor.insert_triangle(t)
#
#vtk_interactor.visualize(triangle_or_truss, wireframe)

import sys
import pprint
import time
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTreeWidgetItem, QColorDialog
from PyQt5 import Qt, QtCore, QtGui
from PyQt5.QtCore import Qt as qut
import sys
import city
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
import vtk_interaction


class ColorButton(QtWidgets.QPushButton):
    def __init__(self,_city_vtk, _objects_key, _buildings, _checked_items):
        super().__init__()
        self.setText('')
        self.city_vtk=_city_vtk
        self.objects_key=_objects_key
        self.buildings=_buildings
        self.checked_items=_checked_items

    def on_click(self):
        color = QColorDialog.getColor()
        #print(color.getRgb())
        self.setStyleSheet("background:rgb("+str(color.getRgb()[0])+","+str(color.getRgb()[1])+","+str(color.getRgb()[2])+")")
        current_color=[color.getRgb()[0],color.getRgb()[1],color.getRgb()[2]]
        if self.objects_key=='Panel Beams' or self.objects_key=='Wall Columns':
            self.city_vtk.LineColorLabels[self.objects_key]=current_color
            self.city_vtk.LineColors = vtk.vtkUnsignedCharArray()
            self.city_vtk.LineColors.SetNumberOfComponents(3)
            self.city_vtk.LineColors.SetName("LineColors")
            self.city_vtk.insert_buildings(self.buildings,self.checked_items,_only_colors=True)
            self.city_vtk.PolyData_Lines = vtk.vtkPolyData()
            self.city_vtk.visualize()
            city_vtk.renWin.Render()
        else:
            self.city_vtk.BuildingColorLabels[self.objects_key]=current_color
            self.city_vtk.BuildingCellColors = vtk.vtkUnsignedCharArray()
            self.city_vtk.BuildingCellColors.SetNumberOfComponents(3)
            self.city_vtk.BuildingCellColors.SetName("BuildingCellColors")
            self.city_vtk.insert_buildings(self.buildings,self.checked_items,_only_colors=True)
            self.city_vtk.PolyData_BuildingCells = vtk.vtkPolyData()
            self.city_vtk.visualize()
            city_vtk.renWin.Render()


# overwrite combobox, so that no duplicates are allowed. 
class ComboBox(QtWidgets.QComboBox):
    def addItem(self, item):
        if item not in self.get_set_items():
            super(ComboBox, self).addItem(item)

    def addItems(self, items):
        items = list(self.get_set_items() | set(items))
        super(ComboBox, self).addItems(items)

    def get_set_items(self):
        return set([self.itemText(i) for i in range(self.count())])


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.adjustSize()
        uic.loadUi('./gui_designer/ideas4all_city_simulator_gui.ui', self)
        self.show()
        self.checked_items={'Building Blocks': 2, 'Buildings': 2, 'Panels': 2, 'Panel Facets': 2, 'Panel Beams': 2, 'Walls': 2, 'Wall Facets': 2, "Wall Columns" : 2, "Terrain" :2}

    def handleItemChanged(self, item, column):
        checked_items={'Building Blocks': 0, 'Buildings': 0, 'Panels': 0, 'Panel Facets': 0, 'Panel Beams': 0, 'Walls': 0, 'Wall Facets': 0, "Wall Columns" : 0, "Terrain" : 0}
        if item.checkState(column) == QtCore.Qt.Checked:
            print('Item Checked')
        elif item.checkState(column) == QtCore.Qt.Unchecked:
            print('Item Unchecked')
        for item in self.treeWidget.findItems("", QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive):
            if (item.checkState(0)>0):
                checked_items[item.text(0)]=item.checkState(0)
                #print (item.text(0),item.checkState(0))
        print(checked_items)

        
        self.city_vtk.ground_triangles = vtk.vtkCellArray()
        self.city_vtk.building_triangles = vtk.vtkCellArray()
        self.city_vtk.trusses = vtk.vtkCellArray()
        self.city_vtk.LineColors = vtk.vtkUnsignedCharArray()
        self.city_vtk.LineColors.SetNumberOfComponents(3)
        self.city_vtk.LineColors.SetName("LineColors")
        self.city_vtk.insert_buildings(self.buildings,checked_items)
        self.city_vtk.insert_ground_triangles(self.ground_triangles.values(),checked_items)
        #refresh is necessary, otherwise it blows! apperantly set data appends sometimes
        self.city_vtk.PolyData_BuildingCells = vtk.vtkPolyData()
        self.city_vtk.PolyData_GroundCells = vtk.vtkPolyData()
        self.city_vtk.PolyData_Lines = vtk.vtkPolyData()
        self.city_vtk.visualize()
        city_vtk.renWin.Render()
        self.checked_items=checked_items
    
    def manage_selection_enablebox(self):
        if self.EnableSelection_checkBox.isChecked():
            print("Selection is Enabled")
            #self.facets_pushbutton.setEnabled(True)
            self.buildings_pushbutton.setEnabled(True)
            self.buildingBlocks_pushbutton.setEnabled(True)
        else:
            print("Selection is Disabled")
            #self.facets_pushbutton.setChecked(False)
            self.buildings_pushbutton.setChecked(False)
            self.buildingBlocks_pushbutton.setChecked(False)
            #self.facets_pushbutton.setEnabled(False)
            self.buildings_pushbutton.setEnabled(False)
            self.buildingBlocks_pushbutton.setEnabled(False)


    def manage_selection_box_f(self):
        if self.facets_pushbutton.isChecked():
            print("Facet selection is activated")
            self.buildings_pushbutton.setChecked(False)
            self.buildingBlocks_pushbutton.setChecked(False)

    def manage_selection_box_b(self):
         if self.buildings_pushbutton.isChecked():
            print("Building selection is activated")
            #self.facets_pushbutton.setChecked(False)
            self.buildingBlocks_pushbutton.setChecked(False)

    def manage_selection_box_bb(self):
        if self.buildingBlocks_pushbutton.isChecked():
            print("Building Block selection is activated")
            #self.facets_pushbutton.setChecked(False)
            self.buildings_pushbutton.setChecked(False)
        
    def fill_table_widget(self):
        attr = ['building blocks','buildings', 'beamsets', 'columns', 'basesets', 'walls', 'vertices']
        selected_buildings=[self.comboboxes['buildings'].itemText(i) for i in range(self.comboboxes['buildings'].count())]

        for s in selected_buildings:
            if s!="None":
                current_building=self.buildings[s]
                for bs in current_building.beamsets:
                    self.comboboxes['beamsets'].addItem(bs.id)
                    self.comboboxes['beamsets'].setCurrentIndex(self.comboboxes['beamsets'].count() - 1)
                    for v in bs.vertices:
                        self.comboboxes['vertices'].addItem(v.id)
                        self.comboboxes['vertices'].setCurrentIndex(self.comboboxes['vertices'].count() - 1)

                for c in current_building.columns:
                    self.comboboxes['columns'].addItem(c.id)
                    self.comboboxes['columns'].setCurrentIndex(self.comboboxes['columns'].count() - 1)
                for bas in current_building.basesets:
                    self.comboboxes['basesets'].addItem(bas.id)
                    self.comboboxes['basesets'].setCurrentIndex(self.comboboxes['basesets'].count() - 1)
                for w in current_building.walls:
                    self.comboboxes['walls'].addItem(w.id)
                    self.comboboxes['walls'].setCurrentIndex(self.comboboxes['walls'].count() - 1)
            i=0
            for j in attr:
                number=str(self.comboboxes[j].count()-1)
                self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(number))
                i += 1



    def show_table_widget(self, triggered=False):
        attr = ['building blocks','buildings', 'beamsets', 'columns', 'basesets', 'walls', 'vertices']

        if not triggered:
            self.comboboxes={}
            for i in attr:
                current_comboBox = QtWidgets.QComboBox()
                self.comboboxes[i]=current_comboBox
                self.comboboxes[i].addItem("None")
                self.comboboxes[i].setEditable(True)
                self.comboboxes[i].setMaxVisibleItems(5)

        


        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(7)
        self.tableWidget.show()
        self.tableWidget.setHorizontalHeaderLabels(["Item Type","Item Id[s]","# of Selected Items"])
        i=0
        for j in attr:
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(j))
            self.tableWidget.setCellWidget(i, 1, self.comboboxes[j])
            number=str(self.comboboxes[j].count()-1)
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(number))
            i += 1

    def show_tree_widget(self, buildings, ground_triangles, city_vtk, vertices, building_blocks, beams, beamsets):
        self.city_vtk=city_vtk
        self.buildings=buildings
        self.building_blocks=building_blocks
        self.vertices=vertices
        self.ground_triangles=ground_triangles
        tw    = self.treeWidget
        tw.setHeaderLabels(['City Item', 'Quantity [-]', 'Remark', 'Color'])
        tw.setAlternatingRowColors(True)

        bb = QtWidgets.QTreeWidgetItem(tw, ['Building Blocks', str(len(building_blocks.keys())), '# of Building Blocks'])
        bb.setFlags(bb.flags() |QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)

        b = QtWidgets.QTreeWidgetItem(bb, ['Buildings', str(len(buildings.keys())), '# of Buildings'])
        b.setFlags(b.flags() |QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)

        self.gt = QtWidgets.QTreeWidgetItem(tw, ['Terrain', str(len(ground_triangles.keys())), '# of triangles of geoterrain'])
        self.gt.setCheckState(0, QtCore.Qt.Checked)
        
        
        columns=0
        
        panltriangles=0
        walltriangles=0

        for bui in buildings.values():
            for bs in bui.basesets:
                panltriangles+=len(bs.triangles)
            
            for w in bui.walls:
                walltriangles+=len(w.triangles)
            columns+=len(bui.columns)


        b1=QtWidgets.QTreeWidgetItem(b, ['Panels', str(len(beamsets.keys())), '# of Panels'])
        b1.setFlags(b1.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
        #b1.setCheckState(0, QtCore.Qt.Checked)
        b11=QtWidgets.QTreeWidgetItem(b1, ['Panel Facets', str(panltriangles), '# of triangles on Panels'])
        self.PanelFacetPushbutton=ColorButton(self.city_vtk,'Panel Facets', self.buildings, self.checked_items)
        self.PanelFacetPushbutton.setStyleSheet("background:rgb(0,100,150)")
        self.PanelFacetPushbutton.clicked.connect(self.PanelFacetPushbutton.on_click)
        tw.setItemWidget(b11,3,self.PanelFacetPushbutton)
        b11.setFlags(b1.flags() | QtCore.Qt.ItemIsUserCheckable)
        b11.setCheckState(0, QtCore.Qt.Checked)


        b12=QtWidgets.QTreeWidgetItem(b1, ['Panel Beams', str(len(beams.keys())), '# of Beams around Panels'])
        self.PanelBeamPushbutton=ColorButton(self.city_vtk,'Panel Beams', self.buildings, self.checked_items)
        self.PanelBeamPushbutton.setStyleSheet("background:rgb(0,0,150)")
        self.PanelBeamPushbutton.clicked.connect(self.PanelBeamPushbutton.on_click)
        tw.setItemWidget(b12,3,self.PanelBeamPushbutton)
        b12.setFlags(b1.flags() | QtCore.Qt.ItemIsUserCheckable)
        b12.setCheckState(0, QtCore.Qt.Checked)


        b2=QtWidgets.QTreeWidgetItem(b, ['Walls', str(columns/2), '# of Walls'])
        b2.setFlags(b2.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
        #b1.setCheckState(0, QtCore.Qt.Checked)
        b21=QtWidgets.QTreeWidgetItem(b2, ['Wall Facets', str(walltriangles), '# of triangles on Walls'])
        self.WallFacetPushbutton=ColorButton(self.city_vtk, 'Wall Facets', self.buildings, self.checked_items)
        self.WallFacetPushbutton.setStyleSheet("background:rgb(0,150,100)")
        self.WallFacetPushbutton.clicked.connect(self.WallFacetPushbutton.on_click)
        tw.setItemWidget(b21,3,self.WallFacetPushbutton)
        b21.setFlags(b2.flags() | QtCore.Qt.ItemIsUserCheckable)
        b21.setCheckState(0, QtCore.Qt.Checked)



        b22=QtWidgets.QTreeWidgetItem(b2, ['Wall Columns', str(columns), '# of Columns along Walls'])
        self.WallColumnPushbutton=ColorButton(self.city_vtk, 'Wall Columns', self.buildings, self.checked_items)
        self.WallColumnPushbutton.setStyleSheet("background:rgb(0,150,0)")
        self.WallColumnPushbutton.clicked.connect(self.WallColumnPushbutton.on_click)
        tw.setItemWidget(b22,3,self.WallColumnPushbutton)
        b22.setFlags(b2.flags() | QtCore.Qt.ItemIsUserCheckable)
        b22.setCheckState(0, QtCore.Qt.Checked)

        
        #instead of itemchecked, itemlicked need to be used to avoid recursive effects
        self.treeWidget.itemClicked.connect(self.handleItemChanged)
        tw.expandAll()
        tw.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        tw.header().setStretchLastSection(False)
        tw.show()
        




class OutLog:
    def __init__(self, edit, out=None, color=None):

        self.edit = edit
        self.out = None
        self.color = color

    def write(self, m):
        if self.color:
            tc = self.edit.textColor()
            self.edit.setTextColor(self.color)

        self.edit.moveCursor(QtGui.QTextCursor.End)
        self.edit.insertPlainText( m )

        if self.color:
            self.edit.setTextColor(tc)

        if self.out:
            self.out.write(m)

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    # start application of dark theme
    app.setStyle("Fusion")
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53,53,53))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15,15,15))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53,53,53))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53,53,53))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
         
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142,45,197).lighter())
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)   
    app.setPalette(palette)
    # end application of dark theme
    
    window = Ui()
    window.showMaximized()

    frame = window.tabWidget


    vl=window.vtkLayout
    vtkWidget = QVTKRenderWindowInteractor(frame)
    vl.addWidget(vtkWidget)

    city_vtk, buildings, ground_triangles, vertices, building_blocks, beams, beamsets=city.define_city(vtkWidget)
    window.show_tree_widget(buildings, ground_triangles, city_vtk, vertices, building_blocks, beams, beamsets)
    window.show_table_widget()
    window.EnableSelection_checkBox.stateChanged.connect(window.manage_selection_enablebox)
    #window.facets_pushbutton.clicked.connect(window.manage_selection_box_f)
    window.buildings_pushbutton.clicked.connect(window.manage_selection_box_b)
    window.buildingBlocks_pushbutton.clicked.connect(window.manage_selection_box_bb)

    city_vtk.style = vtk_interaction.MouseInteractorHighLightActor(city_vtk, window)
    city_vtk.style.SetDefaultRenderer(city_vtk.ren)
    city_vtk.iren.SetInteractorStyle(city_vtk.style)


    city_vtk.visualize()
    city_vtk.renWin.Render()
    print("render window is rendered")
    city_vtk.iren.Initialize()
    city_vtk.iren.Start()
    edit=window.textEdit_Log
    sys.stdout = OutLog( edit, sys.stdout)

    app.exec_()
    
    
    
    



import math
import matplotlib.pyplot as plt
import numpy as np

import triangle as tr
import vertices as vertex
from scipy.interpolate import griddata


def constrained_polygon_triangulation(_points):
    N=int(_points.size/2)
    
    #print(N)
    i = np.arange(N)
    seg = np.stack([i, i + 1], axis=1) % N
    #points = np.array([[0, 0], [0, 10], [5, 10], [5, 5], [10, 5], [10, 10],[15, 10], [15, 0]]) 
    A = dict(vertices=_points,segments=seg)
    try:
        B = tr.triangulate(A,'p')
    except: 
        return {},False
    else:
        return B['triangles'],True
    #tr.compare(plt, A, B)
    #print(B['triangles'])
    #plt.show()


def permutation_symbol(i,j,k):
    return (i-j)*(j-k)*(k-i)/2

def cross_product(v1,v2):
    normal=[0.0,0.0,0.0]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                normal[i]+=permutation_symbol(i,j,k)*v1[j]*v2[k]
    return normal

def dot_product(v1, v2):
    return math.sqrt(v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2])

def elevate_floors_mid(ground_vertices, beamsets):
    ground_xy=np.array([]).reshape(0,2)
    ground_z=np.array([]).reshape(0,1)
    beamset_mids=np.array([]).reshape(0,2)
    for v in ground_vertices.values():
        ground_xy=np.vstack([ground_xy,[v.coordsX[0],v.coordsX[1]]])
        ground_z=np.vstack([ground_z,[v.coordsX[2]]])
    for b in beamsets.values():
        beamset_mids=np.vstack([beamset_mids,[b.mid[0],b.mid[1]]])
    #print(ground_xy.shape)
    #print(ground_z.shape)
    #print(beamset_mids.shape)
    interp=griddata(ground_xy, ground_z, beamset_mids, method='linear')
    #print(interp)
    coun=0
    for b in beamsets.values():
        for v in b.vertices:
            v.coordsX[2]=interp.item(coun)
        coun+=1
    #print(coun)


def elevate_floors_corners(ground_vertices, beamsets):
    ground_xy=np.array([]).reshape(0,2)
    ground_z=np.array([]).reshape(0,1)
    beamset_corners=np.array([]).reshape(0,2)
    for v in ground_vertices.values():
        ground_xy=np.vstack([ground_xy,[v.coordsX[0],v.coordsX[1]]])
        ground_z=np.vstack([ground_z,[v.coordsX[2]]])
    for b in beamsets.values():
        for v in b.vertices:
            beamset_corners=np.vstack([beamset_corners,[v.coordsX[0],v.coordsX[1]]])
    #print(ground_xy.shape)
    #print(ground_z.shape)
    #print(beamset_corners.shape)
    interp=griddata(ground_xy, ground_z, beamset_corners, method='linear')
    #print(interp)
    coun=0
    for b in beamsets.values():
        for v in b.vertices:
            v.coordsX[2]=interp.item(coun)
            coun+=1
    #print(coun)
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
import vertices
#import trusses
import beams
import beamsets
import buildings
import xml.etree.ElementTree as ET

def parse_objs(osmfile,_vertices, _beamsets, _beams, _buildings,_origin):
    #osmlines=osmfile.read()
    column_interval=8
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

                        #for nd in current_node_ids: # the start id is twice inside! this may cause problem! 
                        #    _beamsets[current_beamset_id].append_vertex(_vertices[nd])
                        #for ndid in range(len(current_node_ids)-1):
                        #    nd_tip=current_node_ids[ndid]
                        #    nd_tail=current_node_ids[ndid+1]
                        #    _beams[current_beamset_id+delim+nd_tip]=beams.beam(current_beamset_id+delim+nd_tip,[_vertices[nd_tip],_vertices[nd_tail]])
                        #    _beamsets[current_beamset_id].append_beam(_beams[current_beamset_id+delim+nd_tip])
                        _buildings[child.attrib["id"]].append_beamset(_beamsets[current_beamset_id])
            if isbuilding:
                _buildings[child.attrib["id"]].assign_attributes(current_attributes)
                        #print(childofchild.attrib["k"],childofchild.attrib["v"])
import math
import numpy as np



class triangle:
    def __init__(self,_label,_vertices, _id):
        self.label=_label
        self.id=_id
        self.vertices=[]
        self.vertices.append(_vertices[0])
        self.vertices.append(_vertices[1])
        self.vertices.append(_vertices[2])
        
        #old: coords need to be specified, meters or lat long
        #self.all_coords=np.array([]).reshape(0,3)
        #for v in self.vertices:
        #    self.all_coords=np.vstack([self.all_coords,[v.coords[0],v.coords[1],0.0]])
        #self.mid=list(np.mean(self.all_coords,axis=0))
        ##print(self.mid)
    '''
    def check_inside_nonconvex_boundaries(self, _boundaries):
        p1=np.subtract(self.all_coords[1],self.all_coords[0])
        p2=np.subtract(self.all_coords[2],self.all_coords[1])
        p3=np.array([0.0,0.0,1.0])
        cross=np.cross(p1,p2)
        dot=np.dot(cross,p3)
        #print(dot)
        if dot<0:
            return False
        else:
            return True
        #print("check")
        #for b in range(len(_boundaries)-1):
        #    p1=np.array([_boundaries[b].coords[0],_boundaries[b].coords[1],0.0])
        #    p2=np.array([_boundaries[b+1].coords[0],_boundaries[b+1].coords[1],0.0])
        #    p3=np.array([0.0,0.0,1.0])
        #    c_p1=np.subtract(p1,self.mid) 
        #    c_p2=np.subtract(p2,self.mid)
        #    cross=np.cross(c_p1,c_p2)
        #    dot=np.dot(cross,p3)
        #    #print(dot)
        #    if dot<0.0:
        #        return False
        #return True
    '''
            
             
import math



class truss:
    def __init__(self,_id,_vertices):
        self.id=_id
        self.vertices=[]
        self.vertices.append(_vertices[0])
        self.vertices.append(_vertices[1])
        self.dir=[]
        for i in range(3):
            self.dir.append(self.vertices[1].coordsX[i]-self.vertices[0].coordsX[i])
    #def dot_product(self, _anytruss):
    #    return math.sqrt(self.dir[0]*_anytruss.dir[0]+self.dir[1]*_anytruss.dir[1]+self.dir[2]*_anytruss.dir[2])
    #def check_if_beam(self):
    #    returnvalue=False
    #    if self.dir[1]==0.0:
    #        returnvalue=True
    #    return returnvalue
    #def check_if_column(self):
    #    returnvalue=False
    #    if self.dir[0]==0.0 and self.dir[2]==0:
    #        returnvalue=True
    #    return returnvalue
    #def check_if_edge(self):
        

        
             
from geopy.distance import geodesic
import math

class vertex:
    def __init__(self,_id,_coords_lat_long):
        self.id=_id
        self.coords_lat_long=[]
        self.coordsX=[0.0]*3
        self.coords_lat_long.append(float(_coords_lat_long[0]))#lat
        self.coords_lat_long.append(float(_coords_lat_long[1]))#long
        #self.homes=[]
        self.homes=set()
        #self.coords.append(float(_coords[2]))#dummy
        self.facetids=[]
    def append_facetid(self,_id):
        self.facetids.append(_id)

    def convert_lat_long2m(self, _origin):

        x_origin=(self.coords_lat_long[0],_origin[1])
        x_target=(self.coords_lat_long[0],self.coords_lat_long[1])
        self.coordsX[0]=geodesic(x_origin, x_target).meters        

        y_origin=(_origin[0],self.coords_lat_long[1])
        y_target=(self.coords_lat_long[0],self.coords_lat_long[1])
        self.coordsX[1]=geodesic(y_origin, y_target).meters      

    def dist_2_another_vertex_in_m(self, _origin):

        x_origin=(self.coords_lat_long[0],_origin[1])
        x_target=(self.coords_lat_long[0],self.coords_lat_long[1])
        retx=geodesic(x_origin, x_target).meters        

        y_origin=(_origin[0],self.coords_lat_long[1])
        y_target=(self.coords_lat_long[0],self.coords_lat_long[1])
        rety=geodesic(y_origin, y_target).meters      

        return math.sqrt(retx*retx+rety*rety)

    def convert_CoordsX2FemCoordsX(self):
        old_CoordsX_x=self.coordsX[0]
        old_CoordsX_y=self.coordsX[1]
        old_CoordsX_z=self.coordsX[2]

        self.coordsX[0]=old_CoordsX_x
        self.coordsX[1]=old_CoordsX_z
        self.coordsX[2]=-1.0*old_CoordsX_y
import vtk
import trusses
import vertices
import columns
import matplotlib
import math


def mkVtkIdList(it):
    vil = vtk.vtkIdList()
    for i in it:
        vil.InsertNextId(int(i))
    return vil

def rgb(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    r/=255.0
    g/=255.0
    b/=255.0
    
    return r, g, b



class MouseInteractorHighLightActor(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self,vtkinteractor,_window,parent=None):
        self.vtkinteractor=vtkinteractor
        #self.SetDefaultRenderer(self.vtkinteractor.ren)
        self.window=_window
        self.buildings=_window.buildings
        self.ground_triangles=_window.ground_triangles
        self.vertices=_window.vertices
        #homes=[v.homes for v in self.vertices.values()]
        #print(homes)
        self.checked_items=_window.checked_items
        self.spressed=False
        #self.AddObserver("MiddleButtonReleaseEvent",self.middleButtonReleaseEvent)    
        
        self.AddObserver("LeftButtonPressEvent", self.ButtonEvent)
        self.vtkinteractor.iren.AddObserver("KeyPressEvent", self.Keypress)
        self.debugfile=open("debugfile.deb",'w')
 
    def Keypress(self,obj,event):
       
        key = obj.GetKeySym()
        #key = obj.GetKeyCode()
        self.spressed=False
        if key == "c":
            self.spressed=True
        self.OnKeyRelease()
        return

    def ButtonEvent(self,obj,event):
        
        if self.spressed:
            if self.window.buildings_pushbutton.isChecked() or self.window.buildingBlocks_pushbutton.isChecked():
            

                
                self.spressed=False
                clickPos = self.GetInteractor().GetEventPosition()
                picker = vtk.vtkCellPicker()
                #picker.Pick(clickPos[0], clickPos[1], 0, self.vtkinteractor.ren)
                picker.Pick(clickPos[0], clickPos[1], 0, self.GetDefaultRenderer())

                #cellids=picker.GetSubId()
                cellid=picker.GetCellId()

                print("selected cell id: "+str(cellid))

                numberofids=self.vtkinteractor.PolyData_BuildingCells.GetCell(cellid).GetPointIds().GetNumberOfIds()
                pointids=[]
                facetids=[]

                sets=[]
                notground=True
                for p in range(numberofids):
                    pid=self.vtkinteractor.PolyData_BuildingCells.GetCell(cellid).GetPointIds().GetId(p)
                    if self.vtkinteractor.b_VtkPointId2vertexid[pid].startswith("g"):
                        notground=False
                    else:
                        sets.append(self.vertices[self.vtkinteractor.b_VtkPointId2vertexid[pid]].homes)

                if notground:
                    self.building_vertices=set()
                    self.building_facets=set()

                    common_home=[set.intersection(*sets)][0] #in fact this is buggy.but you can not choose really a side wall or bottom triangle with common edge without being able to see it 
                    common_home=list(common_home)[0]
                    self.window.comboboxes['buildings'].addItem(common_home)
                    self.window.comboboxes['buildings'].setCurrentIndex(self.window.comboboxes['buildings'].count() - 1)

                    self.get_building_vertices(common_home)
                    self.get_building_facets(common_home)


                    if self.window.buildingBlocks_pushbutton.isChecked():
                        self.window.comboboxes['building blocks'].addItem(self.buildings[common_home].buildingblock_id)
                        self.window.comboboxes['building blocks'].setCurrentIndex(self.window.comboboxes['building blocks'].count() - 1)
                        for n in self.buildings[common_home].neighbours:
                            self.window.comboboxes['buildings'].addItem(n)
                            self.window.comboboxes['buildings'].setCurrentIndex(self.window.comboboxes['buildings'].count() - 1)
                            for bb in self.buildings[n].beamsets:
                                for v in bb.vertices:
                                    self.building_vertices.add(v.id)

                    self.window.fill_table_widget()


                    for pid in self.building_vertices:
                        pointids.append(self.vtkinteractor.b_vertexId2VtkPointId[pid])

                    for fid in self.building_facets:
                        facetids.append(self.vtkinteractor.b_TriangleId2VtkTriangleid[fid])




                    print("points of selected cell: "+ str(pointids))
                    #for p in pointids:
                    #    self.vtkinteractor.BuildingColors.SetTuple3(p,255,0,0)
                    for f in facetids:
                        self.vtkinteractor.BuildingCellColors.SetTuple3(f,255,0,0)
                    print(self.vtkinteractor.building_triangles.GetNumberOfCells())
                    self.vtkinteractor.PolyData_BuildingCells.GetCellData().SetScalars(self.vtkinteractor.BuildingCellColors)
                    #this update kills! 
                    #self.vtkinteractor.mapper_BuildingCells.Update()
                    #self.vtkinteractor.PolyData_BuildingCells.GetPointData().SetScalars(self.vtkinteractor.BuildingColors)
                    self.vtkinteractor.mapper_BuildingCells.ScalarVisibilityOff()
                    self.vtkinteractor.mapper_BuildingCells.ScalarVisibilityOn()
                    self.vtkinteractor.renWin.Render()
                
        self.OnLeftButtonDown()
        return 
    
    def get_building_vertices(self,_home):
        b=_home
        print("home is selected: "+str(b))
        for bb in range(1,len(self.buildings[b].beamsets)):
            for v in self.buildings[b].beamsets[bb].vertices:
                self.building_vertices.add(v.id)

    def get_building_facets(self,_home):
        b=_home
        print("home is selected: "+str(b))
        for bs in range(1,len(self.buildings[b].basesets)):
            for f in self.buildings[b].basesets[bs].triangles:
                self.building_facets.add(f.id)
        for w in range(1,len(self.buildings[b].walls)):
            for f in self.buildings[b].walls[w].triangles:
                self.building_facets.add(f.id)


class vtk_interactor:
    def __init__(self, vtkWidget, _origin):
        self.outfile=open("debugfile.out",'w')

        self.origin=_origin
        # create a rendering window and renderer
        self.ren = vtk.vtkRenderer()
        #vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        #self.renWin = vtk.vtkRenderWindow()
        self.renWin=vtkWidget.GetRenderWindow()
        self.renWin.AddRenderer(self.ren)

        # create a renderwindowinteractor
        #self.iren = vtk.vtkRenderWindowInteractor()
        self.iren=vtkWidget.GetRenderWindow().GetInteractor()

        #self.iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        self.iren.SetRenderWindow(self.renWin)
        self.PolyData_BuildingCells = vtk.vtkPolyData()
        self.PolyData_GroundCells = vtk.vtkPolyData()
        self.PolyData_Lines = vtk.vtkPolyData()
        
        #self.PolyData=vtk.vtkExtractPolyDataGeometry()
        self.Colors = vtk.vtkUnsignedCharArray()
        self.Colors.SetNumberOfComponents(3)
        self.Colors.SetName("Colors")

        self.BuildingColors = vtk.vtkUnsignedCharArray()
        self.BuildingColors.SetNumberOfComponents(3)
        self.BuildingColors.SetName("BuildingColors")


        self.LineColors = vtk.vtkUnsignedCharArray()
        self.LineColors.SetNumberOfComponents(3)
        self.LineColors.SetName("LineColors")

        self.BuildingCellColors = vtk.vtkUnsignedCharArray()
        self.BuildingCellColors.SetNumberOfComponents(3)
        self.BuildingCellColors.SetName("BuildingCellColors")

        

        

        self.ground_points = vtk.vtkPoints()
        self.ground_triangles = vtk.vtkCellArray()

        self.building_points = vtk.vtkPoints()
        self.building_triangles = vtk.vtkCellArray()


        self.numberoftriangles=0
        self.trusses = vtk.vtkCellArray()
        
        self.mapper_BuildingCells = vtk.vtkPolyDataMapper()
        self.mapper_GroundCells = vtk.vtkPolyDataMapper()
        self.mapper_Lines = vtk.vtkPolyDataMapper()
        
        self.b_vertexId2VtkPointId={}
        self.b_VtkPointId2vertexid={}
        
        self.g_vertexId2VtkPointId={}
        self.g_VtkPointId2vertexid={}
        

        self.b_VtkTriangleId2Triangleid={} 
        self.g_VtkTriangleId2Triangleid={}

        self.b_TriangleId2VtkTriangleid={} 
        self.g_TriangleId2VtkTriangleid={}
        

        self.LineColorLabels={}
        self.LineColorLabels['Panel Beams']=[0,0,150]
        self.LineColorLabels['Wall Columns']=[0,150,0]

        self.BuildingColorLabels={}
        self.BuildingColorLabels['Panel Facets']=[0,100,150]
        self.BuildingColorLabels['Wall Facets']=[0,150,100]
        
        

    def insert_building_vertices(self,_vertices, _colormap=None):
        min_elevation=min([v.coordsX[1] for v in _vertices])
        max_elevation=max([v.coordsX[1] for v in _vertices])
        print("min elevation: "+str(min_elevation))
        print("max elevation: "+str(max_elevation))

        for v in _vertices:
            VtkPointId=self.building_points.InsertNextPoint(v.coordsX[0],v.coordsX[1],v.coordsX[2])
            if _colormap!=None:
                cmap = matplotlib.cm.get_cmap(_colormap)
                val=(v.coordsX[1]-min_elevation)/(max_elevation-min_elevation)
                r,g,b,a = cmap(val)
            else:
                r,g,b=rgb(min_elevation,max_elevation,v.coordsX[1])
            self.BuildingColors.InsertNextTuple3(r*255,g*255,b*255)
            self.b_vertexId2VtkPointId[v.id]=VtkPointId
            self.b_VtkPointId2vertexid[VtkPointId]=v.id



    def insert_ground_vertices(self,_vertices, _colormap=None):
        min_elevation=min([v.coordsX[1] for v in _vertices])
        max_elevation=max([v.coordsX[1] for v in _vertices])
        print("min elevation: "+str(min_elevation))
        print("max elevation: "+str(max_elevation))

        for v in _vertices:
            VtkPointId=self.ground_points.InsertNextPoint(v.coordsX[0],v.coordsX[1],v.coordsX[2])
            if _colormap!=None:
                cmap = matplotlib.cm.get_cmap(_colormap)
                val=(v.coordsX[1]-min_elevation)/(max_elevation-min_elevation)
                #if val<0 and val>-0.01:
                #    val=0
                #if val>0.01 and val<0.2:
                #    val=0.2
                r,g,b,a = cmap(val*3)
            else:
                r,g,b=rgb(min_elevation,max_elevation,v.coordsX[1])
        
            self.Colors.InsertNextTuple3(r*255,g*255,b*255)
            self.g_vertexId2VtkPointId[v.id]=VtkPointId
            self.g_VtkPointId2vertexid[VtkPointId]=v.id


    def insert_truss(self,_truss, _type, _only_colors):
        if not _only_colors:
            self.trusses.InsertNextCell(2)
            self.trusses.InsertCellPoint(self.b_vertexId2VtkPointId[_truss.vertices[0].id])
            self.trusses.InsertCellPoint(self.b_vertexId2VtkPointId[_truss.vertices[1].id])

            if _type=="beam":
                self.LineColors.InsertNextTuple3(self.LineColorLabels['Panel Beams'][0],self.LineColorLabels['Panel Beams'][1],self.LineColorLabels['Panel Beams'][2])
            if _type=="column":
                self.LineColors.InsertNextTuple3(self.LineColorLabels['Wall Columns'][0],self.LineColorLabels['Wall Columns'][1],self.LineColorLabels['Wall Columns'][2])
        else:
            if _type=="beam":
                self.LineColors.InsertNextTuple3(self.LineColorLabels['Panel Beams'][0],self.LineColorLabels['Panel Beams'][1],self.LineColorLabels['Panel Beams'][2])
            if _type=="column":
                self.LineColors.InsertNextTuple3(self.LineColorLabels['Wall Columns'][0],self.LineColorLabels['Wall Columns'][1],self.LineColorLabels['Wall Columns'][2])
        #print(_truss.vertices[0].id)

    #def insert_polygon_as_triangle(self,_beamset):
    #    self.triangles.InsertNextCell(len(_beamset.vertices))
    #    for v in _beamset.vertices:
    #        self.triangles.InsertCellPoint(self.vertexId2VtkPointId[v.id])
    
    def insert_building_triangle(self,_triangle, _type, _only_colors):
        if not _only_colors:
            VtkTriangleId=self.building_triangles.InsertNextCell(3)
            
            self.building_triangles.InsertCellPoint(self.b_vertexId2VtkPointId[_triangle.vertices[0].id])
            self.building_triangles.InsertCellPoint(self.b_vertexId2VtkPointId[_triangle.vertices[1].id])
            self.building_triangles.InsertCellPoint(self.b_vertexId2VtkPointId[_triangle.vertices[2].id])

            #VtkTriangleId=self.building_triangles.InsertNextCell(3,[self.b_vertexId2VtkPointId[_triangle.vertices[0].id],self.b_vertexId2VtkPointId[_triangle.vertices[1].id],self.b_vertexId2VtkPointId[_triangle.vertices[2].id]])
            self.b_VtkTriangleId2Triangleid[VtkTriangleId]=_triangle.id
            self.b_TriangleId2VtkTriangleid[_triangle.id]=VtkTriangleId
            self.numberoftriangles+=1
            if _type=="panel":
                self.BuildingCellColors.InsertNextTuple3(self.BuildingColorLabels['Panel Facets'][0],self.BuildingColorLabels['Panel Facets'][1],self.BuildingColorLabels['Panel Facets'][2])
            if _type=="wall":
                self.BuildingCellColors.InsertNextTuple3(self.BuildingColorLabels['Wall Facets'][0],self.BuildingColorLabels['Wall Facets'][1],self.BuildingColorLabels['Wall Facets'][2])
        else:
            if _type=="panel":
                self.BuildingCellColors.InsertNextTuple3(self.BuildingColorLabels['Panel Facets'][0],self.BuildingColorLabels['Panel Facets'][1],self.BuildingColorLabels['Panel Facets'][2])
            if _type=="wall":
                self.BuildingCellColors.InsertNextTuple3(self.BuildingColorLabels['Wall Facets'][0],self.BuildingColorLabels['Wall Facets'][1],self.BuildingColorLabels['Wall Facets'][2])



    def insert_ground_triangle(self,_triangle):
        
        VtkTriangleId=self.ground_triangles.InsertNextCell(3)
        self.ground_triangles.InsertCellPoint(self.g_vertexId2VtkPointId[_triangle.vertices[0].id])
        self.ground_triangles.InsertCellPoint(self.g_vertexId2VtkPointId[_triangle.vertices[1].id])
        self.ground_triangles.InsertCellPoint(self.g_vertexId2VtkPointId[_triangle.vertices[2].id])
        self.g_VtkTriangleId2Triangleid[VtkTriangleId]=_triangle.id
        #self.numberoftriangles+=1
        #print(self.numberoftriangles)
        #self.outfile.write(str(self.numberoftriangles)+"\n")
        
    def insert_ground_triangles(self, _triangles, _checked_items):
        if _checked_items['Terrain']>0:
            for tri in _triangles:
                self.insert_ground_triangle(tri)    

    def insert_beamset(self,_beamset, _only_colors):
        for t in _beamset.beams:
            self.insert_truss(t, "beam", _only_colors)
    
    def insert_column(self,_column, _only_colors):
        for t in _column.trusses:
            self.insert_truss(t, "column", _only_colors)

    def insert_baseset(self,_baseset,_only_colors):
        for t in _baseset.triangles:
            self.insert_building_triangle(t,"panel",_only_colors)

    def insert_wall(self,_wall,_only_colors):
        for t in _wall.triangles:
            self.insert_building_triangle(t,"wall",_only_colors)


    def insert_building(self,_building, _checked_items, _only_colors):
        if _checked_items['Panel Beams']>0:
            for b in _building.beamsets:
                self.insert_beamset(b, _only_colors)
        if _checked_items['Wall Columns']>0:
            for c in _building.columns:
                self.insert_column(c, _only_colors)
        if _checked_items['Panel Facets']>0:
            for bs in _building.basesets:
                self.insert_baseset(bs,_only_colors)
        if _checked_items['Wall Facets']>0:
            for w in _building.walls:
                self.insert_wall(w,_only_colors)
        #for bb in _building.beamsets:
        #self.insert_polygon_as_triangle(_building.beamsets[0])

    def insert_buildings(self,_buildings,_checked_items, _only_colors=False):
        if _checked_items['Buildings']>0:    
            for b in _buildings.values():
                self.insert_building(b,_checked_items, _only_colors)
            #print(b.name)
            



    '''
    def insert_building_triangle(self,_building):
        
        #for v in _building.vertices:
        #    VtkPointId=self.points.InsertNextPoint(v.coords[0],v.coords[1],v.coords[2])
        #    self.vertexId2VtkPointId[v.id]=VtkPointId

        #print(vertexId2VtkPointId.keys())
        for f in _building.facets:
            triangle = vtk.vtkTriangle()
            for i in range(3):
                triangle.GetPointIds().SetId(i,self.vertexId2VtkPointId[f.vertices[i].id])
            self.triangles.InsertNextCell(triangle)

    def insert_building_truss(self,_building):
        truss_counter=1
        candidate_trusses=[]
        
        for f in _building.facets:
            candidate_trusses.append(trusses.truss(truss_counter,[f.vertices[0],f.vertices[1]]))    
            truss_counter+=1
            candidate_trusses.append(trusses.truss(truss_counter,[f.vertices[1],f.vertices[2]]))
            truss_counter+=1    
            candidate_trusses.append(trusses.truss(truss_counter,[f.vertices[2],f.vertices[1]]))    
            truss_counter+=1
        
        truss_counter=1
        for c in candidate_trusses:
            if c.check_if_beam() or c.check_if_column():
                if not _building.check_truss_contained(c):
                    c.id=truss_counter
                    _building.append_truss(c)
                    truss_counter+=1

        for t in _building.trusses:
            self.trusses.InsertNextCell(2)
            self.trusses.InsertCellPoint(self.vertexId2VtkPointId[t.vertices[0].id])
            self.trusses.InsertCellPoint(self.vertexId2VtkPointId[t.vertices[1].id])

    def insert_buildings_triangle(self,_buildings):
        for b in _buildings:
            self.insert_building_triangle(b)
            #print(b.name)
    '''
    def visualize(self):
        
        _wireframe=True
        if(self.ground_triangles.GetNumberOfCells()==0 and self.building_triangles.GetNumberOfCells()==0):
            _wireframe=False


        # START TRIANGLES OF BUILDINGS
        self.PolyData_BuildingCells.SetPoints(self.building_points)
        self.PolyData_BuildingCells.SetPolys(self.building_triangles)
        #self.PolyData_BuildingCells.GetPointData().SetScalars(self.BuildingColors)
        self.PolyData_BuildingCells.GetCellData().SetScalars(self.BuildingCellColors)
        self.mapper_BuildingCells.SetInputData(self.PolyData_BuildingCells)
        #self.mapper_BuildingCells.ScalarVisibilityOff()
        self.mapper_BuildingCells.Update()
        self.actor_BuildingCells = vtk.vtkActor()
        self.actor_BuildingCells.SetMapper(self.mapper_BuildingCells)
        if not _wireframe:
            self.actor_BuildingCells.GetProperty().SetRepresentationToWireframe()
        # START TRIANGLES OF BUILDINGS
        print("actor of building triangles are finished")


        # START TRIANGLES OF GROUND
        self.PolyData_GroundCells.SetPoints(self.ground_points)
        self.PolyData_GroundCells.SetPolys(self.ground_triangles)
        self.PolyData_GroundCells.GetPointData().SetScalars(self.Colors)
        self.mapper_GroundCells.SetInputData(self.PolyData_GroundCells)
        self.mapper_GroundCells.Update()
        self.actor_GroundCells = vtk.vtkActor()
        self.actor_GroundCells.SetMapper(self.mapper_GroundCells)
        if not _wireframe:
            self.actor_GroundCells.GetProperty().SetRepresentationToWireframe()
        # START TRIANGLES OF GROUND
        print("actor of ground triangles are finished")



        #START BULDING LINES
        self.PolyData_Lines.SetPoints(self.building_points)
        self.PolyData_Lines.SetLines(self.trusses)
        self.PolyData_Lines.GetCellData().SetScalars(self.LineColors)
        self.mapper_Lines.SetInputData(self.PolyData_Lines)
        self.mapper_Lines.Update()
        self.actor_Lines = vtk.vtkActor()
        self.actor_Lines.SetMapper(self.mapper_Lines)
        if not _wireframe:
            self.actor_Lines.GetProperty().SetRepresentationToWireframe()
        #END BUILDING LINES
        print("actor of building lines are finished")


        # assign actor to the renderer
        self.ren.AddActor(self.actor_BuildingCells)
        self.ren.AddActor(self.actor_GroundCells)
        self.ren.AddActor(self.actor_Lines)
        self.axes = vtk.vtkAxesActor()


        xAxisLabel = self.axes.GetXAxisCaptionActor2D()#.GetTextActor().SetTextScaleModeToNone()
        xAxisLabel.GetTextActor().SetTextScaleModeToNone()
        xAxisLabel.GetCaptionTextProperty().SetFontSize(10) 
        yAxisLabel = self.axes.GetYAxisCaptionActor2D()#.GetTextActor().SetTextScaleModeToNone()
        yAxisLabel.GetCaptionTextProperty().SetFontSize(10) #
        yAxisLabel.GetTextActor().SetTextScaleModeToNone()
        
        zAxisLabel = self.axes.GetZAxisCaptionActor2D()#.GetTextActor().SetTextScaleModeToNone()
        zAxisLabel.GetCaptionTextProperty().SetFontSize(10) 
        zAxisLabel.GetTextActor().SetTextScaleModeToNone()
         

        self.axes.SetShaftTypeToLine()
        self.axes.SetTotalLength(100, 100, 100)
        self.axes.SetNormalizedShaftLength(1.0, 1.0, 1.0)
        self.axes.SetNormalizedTipLength(0.05, 0.05, 0.05) 

        transform = vtk.vtkTransform()
        # this is necessary for osm
        transform.Translate(self.origin[0],0.0, -1.0*self.origin[1])
        self.axes.SetUserTransform(transform)
        self.ren.AddActor(self.axes)
        print("all actors are added to renderer")

import vertices
import triangles

class wall:
    def __init__(self,_id):
        self.id=_id
        self.vertices=[]
        self.triangles=[]
    def append_vertex(self,_vertex):
        self.vertices.append(_vertex)
    def append_triangle(self,_triangle):
        self.triangles.append(_triangle)        
    
