import objparser
import osmparser
import pprint
import vtk_interaction
import os
import time
import requests
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import DesiredCapabilities




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
osmparser.parse_objs(osmfile,vertices,beamsets,trusses,buildings)




'''
necessary_information=["building:levels","height"]
for b in buildings.values():
    b.set_feasibility(necessary_information)
'''

counter=0
buildings_dic={}
buildings_dic[mahalle]={}
prev_file=open("map_kadiköy_caferaga.json",'r', encoding='utf-8')
start_time = time.time()
buildings_dic=json.load(prev_file)
elapsed_time = time.time() - start_time
print("json load needs: "+str(elapsed_time))

last_key=list(buildings_dic[mahalle].keys())[-1]
#print(last_key)

#print(buildings_dic[mahalle].keys())

'''

#start: data crawling part
f=open(osmfilename.split(".osm")[0]+".json", 'w', encoding='utf-8')
options = Options()
options.binary_location = "C:/Users/can/AppData/Local/Google/Chrome/Application/chrome.exe"
options.headless = True
driver = webdriver.Chrome(chrome_options=options, executable_path="C:/PZI_16292/CAN/PersDev/EQ/01_OBJ2VTK/release_2/chromedriver_win32/chromedriver.exe")
driver.set_window_size(1400, 900)
driver.get(page)
driver.implicitly_wait(5)
action = ActionChains(driver)
time.sleep(5)
restarted=False

gcounter=0
truncation_loc_found=False
for bi,b in buildings.items():
    gcounter+=1
    if bi==last_key:
        truncation_loc_found=True
    
    #if bi not in buildings_dic[mahalle].keys():# and gcounter==1:
    if truncation_loc_found:
        print("trying for building number "+str(gcounter)+" with name: "+bi)
        restarted=b.get_address_and_level(buildings_dic[mahalle],driver,action,mahalle,counter,restarted)
        if restarted:
            print("ATTEMPT RESTART")
            driver.close()
            time.sleep(10)
            options = Options()
            options.binary_location = "C:/Users/can/AppData/Local/Google/Chrome/Application/chrome.exe"
            options.headless = True
            driver = webdriver.Chrome(chrome_options=options, executable_path="C:/PZI_16292/CAN/PersDev/EQ/01_OBJ2VTK/release_2/chromedriver_win32/chromedriver.exe")
            driver.set_window_size(1400, 900)
            driver.get(page)
            driver.implicitly_wait(5)
            action = ActionChains(driver)
            restarted=True
            print("RESTARTED")
            time.sleep(5)

        if(int(counter%20)==0):
            f=open(osmfilename.split(".osm")[0]+".json", 'w', encoding='utf-8')
            json.dump(buildings_dic, f, ensure_ascii=False, indent=4)
            f.close()
        counter+=1
        #b.build_building(beamsets,vertices,trusses)
f=open(osmfilename.split(".osm")[0]+".json", 'w', encoding='utf-8')
json.dump(buildings_dic, f, ensure_ascii=False, indent=4)
print("FINISHED")

#end: data crawling part







'''
for bk in buildings_dic[mahalle].keys():
    buildings[bk].levels=buildings_dic[mahalle][bk]["numberoflevels"]
#start wo crawling

#end wo crawling

start_time = time.time()
last_vertex_id=max([int(v) for v in vertices.keys()])
numberofbuildingswithheight=0
for b in buildings.values():
    numberofbuildingswithheight,last_vertex_id=b.build_building(beamsets,vertices,trusses,numberofbuildingswithheight,last_vertex_id)
elapsed_time = time.time() - start_time
print("building needs: "+str(elapsed_time))

print("number of buildings with height: "+str(numberofbuildingswithheight))



triangle_or_truss=True
wireframe=False
start_time = time.time()
vtk_interactor=vtk_interaction.vtk_interactor()
elapsed_time = time.time() - start_time
print("interactor needs: "+str(elapsed_time))

vtk_interactor.insert_all_vertices(vertices.values())
vtk_interactor.insert_buildings(buildings)
#    
vtk_interactor.visualize(triangle_or_truss, wireframe)
