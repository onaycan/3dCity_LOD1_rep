import geocoder
import numpy as np
import time

import geopy
from geopy.geocoders import Nominatim
from geopy.geocoders import GeocodeFarm
from geopy.exc import GeocoderTimedOut
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class building:
    def __init__(self,_name):
        self.name=_name
        self.beamsets=[]
        self.attributes={}
        self.osm_feasible=False
        self.levels="NotFound"

        self.buildingname=''
        self.sitename=''
        self.groundarea=0.0
        #self.facets=[]
        #self.vertices=[]
        #self.trusses=[]
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
    
    def get_building_level(self,_driver,_action):
        time.sleep(5)
        araclar_tab=_driver.find_element_by_xpath("//a[@title='Araçlar']")
        araclar_tab.click()
        option=araclar_tab.find_element_by_xpath("//option[@data-i18n='COGRAFI - ED50']")
        option.click()
        #they wrote the fields wrong
        y_coord_field=araclar_tab.find_element_by_xpath("//input[@id='_pskgoXCoord']")
        y_coord_field.clear()
        y_coord_field.send_keys(str(self.lon))
        x_coord_field=araclar_tab.find_element_by_xpath("//input[@id='_pskgoYCoord']")
        x_coord_field.clear()
        x_coord_field.send_keys(str(self.lat))
        
        git=araclar_tab.find_element_by_xpath("//a[@data-i18n='araclar.git']")
        time.sleep(2)
        git.click()


        nokta_bilgisi=git=araclar_tab.find_element_by_xpath("//i[@class='icon-nokta-bilgisi']")
        nokta_bilgisi.click()
        time.sleep(2)

        target=araclar_tab.find_element_by_xpath("//div[@class='ol-overlay-container ol-selectable']")
        time.sleep(2)
        #_action.move_to_element(target).perform()
        target.click()

        drob_down_menu=_driver.find_element_by_xpath("//i[@class='icon-arama-sonuclari']")
        time.sleep(2)
        yapi_cand=drob_down_menu.find_elements_by_xpath("//div[@class='_ncresult-list-title']")
        time.sleep(2)

        for yapi in yapi_cand:
            if "Yapi" in yapi.text:
                yapi.click()
                break
            
            
        _driver.switch_to_default_content()
        mainframe=_driver.find_element_by_xpath("//iframe[@autoresize='1']")
        _driver.switch_to.frame(mainframe)
        names=_driver.find_elements_by_id("string")
        #print("Kat: "+names[2].text)
        self.buildingname=names[0].text
        self.sitename=names[1].text
        self.levels=names[2].text
        self.groundarea=names[3].text

        _driver.switch_to_default_content()
        time.sleep(2)
        _driver.find_element_by_xpath("//i[@class='icon-temizle']").click()




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
        except GeocoderTimedOut:
            pass
        
        try:
            if _restarted<3:
                self.get_building_level(_driver,_action)
            else:
                pass
        except:
            #pass
            _driver.close()
            options = Options()
            options.binary_location = "C:/Users/can/AppData/Local/Google/Chrome/Application/chrome.exe"
            options.headless = True
            _driver = webdriver.Chrome(chrome_options=options, executable_path="C:/PZI_16292/CAN/PersDev/EQ/01_OBJ2VTK/release_2/chromedriver_win32/chromedriver.exe", )
            _driver.get("https://keos.kucukcekmece.bel.tr/keos/")
            _driver.implicitly_wait(5)
            _action = ActionChains(_driver)
            _restarted+=1
            self.get_address_and_level(_buildings_dic_m,_driver,_action, _mahalle, _building_counter, _restarted)


        else:
            _restarted=0
            _buildings_dic_m[self.name]={}
            _buildings_dic_m[self.name]["mid_lat"]=self.lat
            _buildings_dic_m[self.name]["mid_lon"]=self.lon
            _buildings_dic_m[self.name]["address"]=str(self.address)
            _buildings_dic_m[self.name]["numberoflevels"]=self.levels
            _buildings_dic_m[self.name]["buildingname"]=self.buildingname
            _buildings_dic_m[self.name]["sitename"]=self.sitename
            _buildings_dic_m[self.name]["groundarea"]=self.groundarea
            print("finished: "+str(self.address)+" levels: "+self.levels+" coords: "+str([self.lat,self.lon]))
            #print(self.levels)
            #print(self.lat)
            #print(self.lon)

            if _building_counter==0:
                checkboxes=_driver.find_elements_by_xpath("//input[@type='checkbox']")
                time.sleep(2)
                for cb in checkboxes:
                    try:
                        cb.click()
                        print("clicked for simplification")
                    except:
                        pass
                        print("passed bec. not possible to click")
                    time.sleep(1)
        
            


    def build_building(self,_beamsets,_vertices,_trusses):
        floor_height=16.0/5.0
        if self.osm_feasible:
            if "height" in self.attributes.keys():
                if "building:levels" in self.attributes.keys():
                    floor_height=float(self.attributes["height"].split()[0].strip())/float(self.attributes["building:levels"])
                    numberoflevels=int(self.attributes["building:levels"])
                else:
                    numberoflevels=int(float(self.attributes["height"])/floor_height)
                    print("numberoflevels:"+str(numberoflevels))
                
            else:
                numberoflevels=int(self.attributes["building:levels"])
            for l in range(1,numberoflevels):
                next_beamset=self.beamsets[0].shift_and_copy_beamset(_vertices,_trusses, str(l), [0.0,0.0,l*floor_height/111000.0])
                _beamsets[next_beamset.id]=next_beamset
                self.beamsets.append(next_beamset)

