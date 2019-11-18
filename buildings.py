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
        #araclar_tab=_driver.find_element_by_xpath("//a[@title='Araçlar']")
        araclar_tab=_driver.find_element_by_xpath("//a[@title='Çizim']")
        time.sleep(4)
        araclar_tab.click()
        nokta_tab=_driver.find_element_by_xpath("//i[@title='Nokta Çiz']")
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
            if "Yapı" in yapi.text:
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
        self.address="inönü"
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
            


    def build_building(self,_beamsets,_vertices,_trusses,_columns_and_beams,_beams,_numberofbuildingswithheight, _lastvertexid, _origin, _all_triangles):
        triangle_counter=len(_all_triangles.keys())
        columns_and_beams_counter=len(_columns_and_beams.keys())
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
                    for nb in next_beamset.beams:
                        _columns_and_beams[columns_and_beams_counter]=nb
                        nb.femid=columns_and_beams_counter
                        columns_and_beams_counter+=1


                    #next_beamset, _lastvertexid=self.beamsets[0].shift_and_copy_beamset(_vertices,_beams, str(l), [0.0,l*floor_height,0.0], _lastvertexid, _origin)
                    
                    _beamsets[next_beamset.id]=next_beamset
                    self.beamsets.append(next_beamset)
                    


                    
                    #start columns
                    
                    for v in range(len(self.beamsets[l-1].vertices)-1):
                        #this id plus from which stage to which, and the corner counter
                        truss_id=self.name+delim+str(l-1)+delim+str(l)+delim+str(v)
                        current_column=columns.column(self.name, columns_and_beams_counter)
                        current_truss=trusses.truss(truss_id,[self.beamsets[l-1].vertices[v],self.beamsets[l].vertices[v]])
                        _trusses[truss_id]=current_truss
                        current_column.define_truss(current_truss)
                        _columns_and_beams[columns_and_beams_counter]=current_column
                        columns_and_beams_counter+=1
                        self.columns.append(current_column)
                    #end columns

                    #start walls
                    current_wall=walls.wall(self.name+delim+str(l))
                    for v in range(0,len(self.beamsets[l-1].vertices)-1):
                        numberofvertices=len(self.beamsets[l-1].vertices)
                        current_vertices=[self.beamsets[l-1].vertices[v],self.beamsets[l-1].vertices[int((v+1)%numberofvertices)],self.beamsets[l].vertices[int((v+1)%numberofvertices)]]
                        current_triangle=triangles.triangle(self.name+delim+str(l)+delim+str(self.beamsets[l-1].vertices[v].id+delim+"0"),current_vertices,triangle_counter)
                        _all_triangles[triangle_counter]=current_triangle
                        triangle_counter+=1
                        current_wall.append_triangle(current_triangle)
                        current_wall.append_vertex(self.beamsets[l-1].vertices[1])
                        current_wall.append_vertex(self.beamsets[l-1].vertices[int((v+1)%numberofvertices)])
                        current_wall.append_vertex(self.beamsets[l].vertices[int((v+1)%numberofvertices)])

                        current_vertices=[self.beamsets[l-1].vertices[v],self.beamsets[l].vertices[v],self.beamsets[l].vertices[int((v+1)%numberofvertices)]]
                        current_triangle=triangles.triangle(self.name+delim+str(l)+delim+str(self.beamsets[l-1].vertices[v].id+delim+"1"),current_vertices,triangle_counter)
                        _all_triangles[triangle_counter]=current_triangle
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
                        _all_triangles[triangle_counter]=ground_triangles["t"+str(coun)]
                        
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
                            _all_triangles[triangle_counter]=ground_triangles["t"+str(coun)]
                            triangle_counter+=1
                            current_baseset.append_triangle(ground_triangles["t"+str(coun)])
                            coun+=1
                        self.basesets.append(current_baseset)

                    #end basesets
                    
                   
                retval=_numberofbuildingswithheight+1
        return retval, _lastvertexid


    def print_simulation_file(self,_filename):
        meter2inches=39.3701
        self.file=open(_filename,'w')
        self.file.write("#BUILDING ID "+str(self.name)+"\n")
        self.file.write("#GROUND"+"\n")
        for v in self.beamsets[0].vertices:
            self.file.write("node"+"\t"+str(v.id)+"\t"+str(v.coordsX[0]*meter2inches)+"\t"+str(v.coordsX[1]*meter2inches)+"\t"+str(v.coordsX[2]*meter2inches)+"\n")

        for bsi in range(1,len(self.beamsets)):
            bs=self.beamsets[bsi]
            self.file.write("#FLOOR #"+str(bsi)+"\n")
            for v in bs.vertices:
                self.file.write("node"+"\t"+str(v.id)+"\t"+str(v.coordsX[0]*meter2inches)+"\t"+str(v.coordsX[1]*meter2inches)+"\t"+str(v.coordsX[2]*meter2inches)+"\n")


        self.file.close()

    '''    
    
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

        '''