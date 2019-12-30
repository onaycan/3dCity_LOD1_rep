import os
from PyQt5.QtWidgets import QTreeWidgetItem, QColorDialog, QFileDialog, QTabWidget
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets, uic
from PyQt5 import QtTest
import numpy 
import datetime
import csv
import matplotlib


def setup_Ui_proc(self):
    self.runorloadcheckBox.stateChanged.connect(self.manage_runorload)
    self.showresults_pushButton.clicked.connect(self.show_results)
    self.run_pushButton.clicked.connect(self.runsimulation)
    self.tensorresult_comboBox.addItem("Displacement")        
    self.tensorresult_comboBox.addItem("Stress")
    self.tensorresult_comboBox.addItem("Strain")
    self.tensorresult_comboBox.setCurrentText("Displacement")
    self.set_combobox_post_legend("Displacement")
    self.scalarresult_comboBox.setCurrentText("Displacement Mag")
    self.tensorresult_comboBox.currentTextChanged.connect(self.set_combobox_post_legend)
    self.scalarresult_comboBox.currentTextChanged.connect(self.set_scalar_result)
    self.legend_table=QtWidgets.QTableWidget()
    self.legend_layout.addWidget(self.legend_table)

def manage_acc_buttons(self):
    if self.acc_checkbutton.isChecked():
        self.lat_pushButton.setEnabled(True)
        self.lon_pushButton.setEnabled(True)
        self.loadsscenario_pushButton.setEnabled(False)
    else:
        self.lat_pushButton.setEnabled(False)
        self.lon_pushButton.setEnabled(False)
        self.loadsscenario_pushButton.setEnabled(True)

def selectDirDialogrun(self):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    dirname = QFileDialog.getExistingDirectory(self,"Select Directory", options=options)
    self.load_folder_name=dirname
    self.runfilename_label.setText(os.path.basename(self.load_folder_name))
    

def selectDirDialogload(self):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    dirname = QFileDialog.getExistingDirectory(self,"Select Directory", options=options)
    self.load_folder_name=dirname
    self.loadfilename_label.setText(os.path.basename(self.load_folder_name))
    self.showresults_pushButton.setEnabled(True)

def openFileNameDialoglat(self):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;at2 files (*.at2)", options=options)
    self.latfile=fileName
    self.latfile_label.setText(os.path.basename(fileName))

def openFileNameDialoglon(self):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;at2 files (*.at2)", options=options)
    self.lonfile=fileName
    self.lonfile_label.setText(os.path.basename(fileName))


def proc_write_parameter_file(self, middlewaredir, outputpath, inputpath):
    configfile=open(middlewaredir+"/Paramaters_Input.txt",'w')
    configfile.write("#Input folder path:\n")
    configfile.write(os.path.abspath(inputpath).replace("\\","/")+"\n")
    configfile.write("#Output folder path:\n")
    configfile.write(os.path.abspath(outputpath).replace("\\","/")+"\n")
    configfile.write("#Unit system <Metric> <US>\n")
    configfile.write(str(self.unit_comboBox.currentText()).lower()+"\n")
    configfile.write("#Acceleration recording in lateral direction:\n")
    configfile.write(self.latfile.replace("\\","/")+"\n")
    configfile.write("#Acceleration recording in perpendicular direction:\n")
    configfile.write(self.lonfile.replace("\\","/")+"\n")
    configfile.write("#Simulation type: <Dynamic> or <Static>:\n")
    configfile.write(str(self.simtype_comboBox.currentText())+"\n")
    configfile.write("#Maximum duration for <Dynamic> simulation in seconds:\n")
    configfile.write(str(self.duration_doubleSpinBox.value())+"\n")
    configfile.write("#Time step dt in seconds:\n")
    configfile.write(str(self.dt_doubleSpinBox.value())+"\n")
    configfile.write("#Number of modes in Modal Analysis:\n")
    configfile.write(str(self.mode_spinBox.value())+"\n")
    configfile.write("#RC Section\n")
    if self.rc_checkBox.isChecked():
        configfile.write("True\n")
    else:
        configfile.write("False\n")
    configfile.write("#Square-Column section width in inches:\n")
    configfile.write(str(self.cw_doubleSpinBox.value())+"\n")
    configfile.write("#Beam depth -- perpendicular to bending axis in inches:\n")
    configfile.write(str(self.bd_doubleSpinBox.value())+"\n")
    configfile.write("#Beam width -- parallel to bending axis in inches:\n")
    configfile.write(str(self.bw_doubleSpinBox.value())+"\n")
    configfile.write("#Girder depth -- perpendicular to bending axis in inches:\n")
    configfile.write(str(self.gd_doubleSpinBox.value())+"\n")
    configfile.write("#Girder width -- parallel to bending axis in inches:\n")
    configfile.write(str(self.gw_doubleSpinBox.value())+"\n")
    configfile.write("#W Section\n")
    if self.ws_checkBox.isChecked():
        configfile.write("True\n")
    else:
        configfile.write("False\n")
    configfile.write("#Live Loads (uniformly distributed) on each floor (furniture, etc.) in psf (pounds per square foot):\n")
    configfile.write(str(self.ll_doubleSpinBox.value())+"\n")
    configfile.close()


def runsimulation(self):
    
    self.showresults_pushButton.setEnabled(False)
    bs=set()
    bbs=set()
    middlewaredir=".\\FEM_MiddleWare"
    root=self.load_folder_name
    for i in range(self.comboboxes['Buildings'].count()):
        current_building_id=self.comboboxes['Buildings'].itemText(i)
        if current_building_id!="None":
            bs.add(current_building_id)
    for b in bs:
        if not self.buildings[b].pounding_building:
            inputpath=root+"/inputs/b_"+str(b)
            outputpath=root+"/outputs/b_"+str(b)
            os.makedirs(inputpath, exist_ok=True)
            self.buildings[b].print_simulation_file(inputpath+"/"+"INPUT_1.tcl")
            self.write_parameter_file(middlewaredir, outputpath, inputpath)
            os.chdir(middlewaredir)
            os.system("OpenSees.exe ./StartSimulation.tcl "+"b_"+str(b))
            os.chdir("..")
            
    for i in range(self.comboboxes['Building Blocks'].count()):
        current_bb_id=self.comboboxes['Building Blocks'].itemText(i)
        if current_bb_id!="None" and len(self.building_blocks[current_bb_id].buildings)>1:
            bbs.add(current_bb_id)
    
    for bb in bbs:
        inputpath=root+"/inputs/"+str(bb)
        outputpath=root+"/outputs/"+str(bb)
        os.makedirs(inputpath, exist_ok=True)
        self.building_blocks[bb].print_pounding_file(inputpath)
        self.write_parameter_file(middlewaredir, outputpath, inputpath)
        os.chdir(middlewaredir)
        os.system("OpenSees.exe ./StartSimulation.tcl "+str(b))
        os.chdir("..")
        
    outputpath=root+"/outputs/"
    self.showresults_pushButton.setEnabled(True)

def manage_simparams(self):
    self.load_folder_name=os.path.abspath(".\\FEM_MiddleWare\\outputs")
    self.runfilename_label.setText(os.path.basename(self.load_folder_name))
    self.loadfilename_label.setText(os.path.basename(self.load_folder_name))
    self.acc_checkbutton.stateChanged.connect(self.manage_acc_buttons)
    self.lat_pushButton.clicked.connect(self.openFileNameDialoglat)
    self.lon_pushButton.clicked.connect(self.openFileNameDialoglon)
    self.lonfile_label.setText(os.path.basename(".\\FEM_MiddleWare\\GMfiles\\H-E12140.at2"))
    self.latfile_label.setText(os.path.basename(".\\FEM_MiddleWare\\GMfiles\\H-E01140.at2"))
    self.latfile=os.path.abspath(".\\FEM_MiddleWare\\GMfiles\\H-E12140.at2")
    self.lonfile=os.path.abspath(".\\FEM_MiddleWare\\GMfiles\\H-E01140.at2")
    self.runsimulation_pushButton.clicked.connect(self.selectDirDialogrun)
    self.loadsimulation_pushButton.clicked.connect(self.selectDirDialogload)

def configure_simulation(self):
    self.preeq_post_tabwidget.setCurrentWidget(self.posttab)

def manage_runorload(self):
    if self.runorloadcheckBox.isChecked():
        self.groupBox_7.setEnabled(True)
        self.groupBox_8.setEnabled(True)
        self.groupBox_9.setEnabled(True)
        self.run_pushButton.setEnabled(True)
        self.loadsimulation_pushButton.setEnabled(False)
        self.runfilename_label.setEnabled(True)
        self.loadfilename_label.setEnabled(False)
        self.runsimulation_pushButton.setEnabled(True)
    else:
        self.groupBox_7.setEnabled(False)
        self.groupBox_8.setEnabled(False)
        self.groupBox_9.setEnabled(False)
        self.runsimulation_pushButton.setEnabled(False)
        self.loadsimulation_pushButton.setEnabled(True)
        self.run_pushButton.setEnabled(False)
        self.runfilename_label.setEnabled(False)
        self.loadfilename_label.setEnabled(True)

def set_timelabel(self):
    self.time_label.setText("Time: "+str(self.dial.value()*0.01)+" sc.")
    if not self.Start_Animation_Push_Button.isChecked():
        self.animatewindow()


   
def animatewindow(self):
    
    if self.Start_Animation_Push_Button.isChecked():
        self.Start_Animation_Push_Button.setText("Stop Animation")
        self.dial.setEnabled(False)
    else:
        self.Start_Animation_Push_Button.setText("Start Animation")
        self.dial.setEnabled(True)
    print("animation started:")
    start=datetime.datetime.now()
    f=self.dial.value()
    if f==self.numberoftimeintervals-1:
        f=0
    broken=False
    while f<int(self.numberoftimeintervals):
        startf=datetime.datetime.now()
        self.dial.setValue(f)
        self.post_eq_city.vtk_interactor.animate_displacement(self.post_eq_city.vertices.values(),f,self.modified_vertices,self.scalefact_doubleSpinBox.value())
        QtTest.QTest.qWait(0.0)
        #brak it right here, so that the set_timelabel renders at least once.
        if not self.Start_Animation_Push_Button.isChecked():
            broken=True
            break
        endf=datetime.datetime.now()
        deltaf=(endf-startf).total_seconds()
        f+=int(deltaf/self.dT)
        
    if not broken:
        self.dial.setValue(self.numberoftimeintervals-1)
        self.post_eq_city.vtk_interactor.animate_displacement(self.post_eq_city.vertices.values(),self.numberoftimeintervals-1,self.modified_vertices,self.scalefact_doubleSpinBox.value())
        QtTest.QTest.qWait(0.0)    
        self.Start_Animation_Push_Button.setChecked(False)
        self.Start_Animation_Push_Button.setText("Start Animation")
        self.dial.setEnabled(True)
        
    end=datetime.datetime.now()
    delta=end-start
    print("end animation")
    print("took "+str(delta.total_seconds()))



def set_combobox_post_legend(self, value):
    
    if value=="Displacement":
        self.scalarresult_comboBox.clear()
        self.scalarresult_comboBox.addItem("Displacement X")
        self.scalarresult_comboBox.addItem("Displacement Y")
        self.scalarresult_comboBox.addItem("Displacement Z")
        self.scalarresult_comboBox.addItem("Displacement Mag")
    if value=="Stress":
        self.scalarresult_comboBox.clear()
        self.scalarresult_comboBox.addItem("Axial Stress in Reinf.")
        self.scalarresult_comboBox.addItem("Axial Stress in Conc.")
        
    if value=="Strain":
        self.scalarresult_comboBox.clear()
        self.scalarresult_comboBox.addItem("Axial Strain in Reinf.")
        self.scalarresult_comboBox.addItem("Axial Strain in Conc.")
    
def set_scalar_result(self,value):
    
    if value!='':
        print("INSIDE!")
        val2key={"Displacement X":"dX0",
                 "Displacement Y":"dX1",
                 "Displacement Z":"dX2",
                 "Displacement Mag":"dXmag",
                 "Axial Stress in Reinf.":"StressReinfMean",
                 "Axial Stress in Conc.":"StressConcMean",
                 "Axial Strain in Reinf.":"StrainReinfMean",
                 "Axial Strain in Conc.":"StrainConcMean"
        }
        for b in self.results.keys():
            #for vid in self.results[b]["Displacements"].keys():
            current_femvertexids=set()
            if b.startswith("b_"):
                current_femvertexids=self.buildings[b.split("_")[1]].femvertexids
            else:
                current_femvertexids=self.building_blocks[b].femvertexids
            for vid in current_femvertexids:
                current_vertex_id=self.post_eq_city.femid2vertexid[str(vid)]
                self.post_eq_city.vertices[current_vertex_id].rColorMap_activ=self.post_eq_city.vertices[current_vertex_id].rColorMaps[val2key[value]]
        rows = 9
        columns=2
        self.legend_table.setColumnCount(columns)
        self.legend_table.setRowCount(rows)
        self.legend_table.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Colour"))
        self.legend_table.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("Value"))
        print(self.resultmaxmins[val2key[value]][0])
        print(self.resultmaxmins[val2key[value]][1])
        for i in range(rows):
            current_value=i/(rows-1)
            current_color_button=QtWidgets.QPushButton()
            if i==0:
                current_color_button.setText("Min:")
            if i==rows-1:
                current_color_button.setText("Max:")
            color_vals=self.cmap(current_value)
            current_style="background:rgb("+str(int(color_vals[0]*255))+","+str(int(color_vals[1]*255))+","+str(int(color_vals[2]*255))+")"
            print(current_style)
            current_color_button.setStyleSheet(current_style)
            self.legend_table.setCellWidget(i,0,current_color_button)
            print_value=current_value*(self.resultmaxmins[val2key[value]][1]-self.resultmaxmins[val2key[value]][0])+self.resultmaxmins[val2key[value]][0]
            self.legend_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(round(print_value, 5))))
        #stop animation and show colors
        self.Start_Animation_Push_Button.setChecked(False)
        self.set_timelabel()
        

def calculate_colormap_values(self):
    
    for i in range(3):
        self.resultmaxmins["dX"+str(i)].append(numpy.amin([numpy.amin(v.dXT[:,i]) for v in self.post_eq_city.vertices.values()]))
        self.resultmaxmins["dX"+str(i)].append(numpy.amax([numpy.amax(v.dXT[:,i]) for v in self.post_eq_city.vertices.values()]))
        for b in self.results.keys():
            for vid in self.femvertexids[b]:
                current_vertex_id=self.post_eq_city.femid2vertexid[str(vid)]
                vals=numpy.multiply(self.post_eq_city.vertices[current_vertex_id].dXT[:,i]-self.resultmaxmins["dX"+str(i)][0],1.0/(self.resultmaxmins["dX"+str(i)][1]-self.resultmaxmins["dX"+str(i)][0]))
                self.post_eq_city.vertices[current_vertex_id].rColorMaps["dX"+str(i)]=numpy.multiply(self.cmap(vals)[:,0:3],255)
    
    self.resultmaxmins["dXmag"].append(numpy.amin([numpy.amin(v.dXmag[:,0]) for v in self.post_eq_city.vertices.values()]))
    self.resultmaxmins["dXmag"].append(numpy.amax([numpy.amax(v.dXmag[:,0]) for v in self.post_eq_city.vertices.values()]))
    for b in self.results.keys():
        for vid in self.femvertexids[b]:
            current_vertex_id=self.post_eq_city.femid2vertexid[str(vid)]
            vals=numpy.multiply(self.post_eq_city.vertices[current_vertex_id].dXmag[:,0]-self.resultmaxmins["dXmag"][0],1.0/(self.resultmaxmins["dXmag"][1]-self.resultmaxmins["dXmag"][0]))
            self.post_eq_city.vertices[current_vertex_id].rColorMaps["dXmag"]=numpy.multiply(self.cmap(vals)[:,0:3],255)
    
    self.resultmaxmins["StressReinfMean"].append(numpy.amin([numpy.amin(v.StressReinfMean) for v in self.post_eq_city.vertices.values()]))
    self.resultmaxmins["StressReinfMean"].append(numpy.amax([numpy.amax(v.StressReinfMean) for v in self.post_eq_city.vertices.values()]))
    for b in self.results.keys():
        for vid in self.femvertexids[b]:
            current_vertex_id=self.post_eq_city.femid2vertexid[str(vid)]
            vals=numpy.multiply(self.post_eq_city.vertices[current_vertex_id].StressReinfMean-self.resultmaxmins["StressReinfMean"][0],1.0/(self.resultmaxmins["StressReinfMean"][1]-self.resultmaxmins["StressReinfMean"][0]))
            self.post_eq_city.vertices[current_vertex_id].rColorMaps["StressReinfMean"]=numpy.multiply(self.cmap(vals)[:,0:3],255)
    
    self.resultmaxmins["StressConcMean"].append(numpy.amin([numpy.amin(v.StressConcMean) for v in self.post_eq_city.vertices.values()]))
    self.resultmaxmins["StressConcMean"].append(numpy.amax([numpy.amax(v.StressConcMean) for v in self.post_eq_city.vertices.values()]))
    for b in self.results.keys():
        for vid in self.femvertexids[b]:
            current_vertex_id=self.post_eq_city.femid2vertexid[str(vid)]
            vals=numpy.multiply(self.post_eq_city.vertices[current_vertex_id].StressConcMean-self.resultmaxmins["StressConcMean"][0],1.0/(self.resultmaxmins["StressConcMean"][1]-self.resultmaxmins["StressConcMean"][0]))
            self.post_eq_city.vertices[current_vertex_id].rColorMaps["StressConcMean"]=numpy.multiply(self.cmap(vals)[:,0:3],255)
    
    self.resultmaxmins["StrainReinfMean"].append(numpy.amin([numpy.amin(v.StrainReinfMean) for v in self.post_eq_city.vertices.values()]))
    self.resultmaxmins["StrainReinfMean"].append(numpy.amax([numpy.amax(v.StrainReinfMean) for v in self.post_eq_city.vertices.values()]))
    for b in self.results.keys():
        for vid in self.femvertexids[b]:
            current_vertex_id=self.post_eq_city.femid2vertexid[str(vid)]
            vals=numpy.multiply(self.post_eq_city.vertices[current_vertex_id].StrainReinfMean-self.resultmaxmins["StrainReinfMean"][0],1.0/(self.resultmaxmins["StrainReinfMean"][1]-self.resultmaxmins["StrainReinfMean"][0]))
            self.post_eq_city.vertices[current_vertex_id].rColorMaps["StrainReinfMean"]=numpy.multiply(self.cmap(vals)[:,0:3],255)
    
    self.resultmaxmins["StrainConcMean"].append(numpy.amin([numpy.amin(v.StrainConcMean) for v in self.post_eq_city.vertices.values()]))
    self.resultmaxmins["StrainConcMean"].append(numpy.amax([numpy.amax(v.StrainConcMean) for v in self.post_eq_city.vertices.values()]))
    for b in self.results.keys():
        for vid in self.femvertexids[b]:
            current_vertex_id=self.post_eq_city.femid2vertexid[str(vid)]
            vals=numpy.multiply(self.post_eq_city.vertices[current_vertex_id].StrainConcMean-self.resultmaxmins["StrainConcMean"][0],1.0/(self.resultmaxmins["StrainConcMean"][1]-self.resultmaxmins["StrainConcMean"][0]))
            self.post_eq_city.vertices[current_vertex_id].rColorMaps["StrainConcMean"]=numpy.multiply(self.cmap(vals)[:,0:3],255)


def show_results(self):
    inches2meter=1.0/39.3701
    
    self.param_tabWidget.setCurrentWidget(self.postprocessing_tab)
    self.Postprocessing_tabwidget.setCurrentWidget(self.tab_postcity)
    self.Start_Animation_Push_Button.setEnabled(True)
    self.result_path=self.load_folder_name
    bulding_paths={}
    self.results={}
    self.femvertexids={}
    print("start searching result files")
    start=datetime.datetime.now()
    for root, dirs, files in os.walk(self.result_path, topdown=False):
        for name in dirs:
            if name.startswith("b_") or name.startswith("bb_"):
                necessaryfile=os.path.abspath(root+"\\"+name+"\\"+"NodeIDs.out")
                if(os.path.isfile(necessaryfile)):
                    bulding_paths[name]=os.path.abspath(root+"\\"+name)
                    self.results[name]={}
                    self.results[name]["Displacements"]={}
                    self.results[name]["StressReinf"]={}
                    self.results[name]["StrainReinf"]={}
                    self.results[name]["StressConc"]={}
                    self.results[name]["StrainConc"]={}

                    current_femvertexids=set()
                    if name.startswith("b_"):
                        current_femvertexids=self.buildings[name.split("_")[1]].femvertexids
                    else:
                        current_femvertexids=self.building_blocks[name].femvertexids
                    self.femvertexids[name]=current_femvertexids

    #pprint.pprint(bulding_paths)
    last_b=0
    last_v=0
    for b,bp in bulding_paths.items():
        #START DISPLACEMENT READING
        idfilename=bp+"\\"+"NodeIDs.out"
        idfile=open(idfilename,'r')
        dispfilename=bp+"\\"+"Displacement_AllNodes.out"
        dispfile=open(dispfilename,'r')
        ids=list(csv.reader(idfile))
        disps=list(csv.reader(dispfile,delimiter=" "))
        ndisps = numpy.array(disps, dtype=numpy.float)
        deltaT=ndisps.item((12,0))-ndisps.item((11,0))
        startr=10
        if b.startswith("bb_"):
            startr=0
        counter=0
        for _id in ids:
            last_v=_id[0]
            self.results[b]["Displacements"][_id[0]]=ndisps[startr:,counter*3+1:counter*3+3+1]*inches2meter
            counter+=1
        #END DISPLACEMENT READING
        #START STRESS STRAIN Reinforcement READING
        idfilename=bp+"\\"+"ColumnElementIDs.out"
        idfile=open(idfilename,'r')
        sfilename=bp+"\\"+"StressStrain_AllColumnElements_reinfEle_sec_1.out"
        sfile=open(sfilename,'r')
        ids=list(csv.reader(idfile))
        ss=list(csv.reader(sfile,delimiter=" "))
        nss = numpy.array(ss, dtype=numpy.float)
        counter=0
        
        for _id in ids:
            self.results[b]["StressReinf"][_id[0]]=nss[startr:,counter*2+1]-nss[startr,counter*2+1]
            self.results[b]["StrainReinf"][_id[0]]=nss[startr:,counter*2+2]-nss[startr,counter*2+2]
            counter+=1
        #END STRESS STRAIN Reinforcement READING
        #START STRESS STRAIN Concrete READING
        idfilename=bp+"\\"+"ColumnElementIDs.out"
        idfile=open(idfilename,'r')
        sfilename=bp+"\\"+"StressStrain_AllColumnElements_concEle_sec_1.out"
        sfile=open(sfilename,'r')
        ids=list(csv.reader(idfile))
        ss=list(csv.reader(sfile,delimiter=" "))
        nss = numpy.array(ss, dtype=numpy.float)
        counter=0
        for _id in ids:
            self.results[b]["StressConc"][_id[0]]=nss[startr:,counter*2+1]-nss[startr,counter*2+1]
            self.results[b]["StrainConc"][_id[0]]=nss[startr:,counter*2+2]-nss[startr,counter*2+2]
            counter+=1
        #END STRESS STRAIN Concrete READING
        last_b=b
    end=datetime.datetime.now()
    delta=end-start
    print("end searching result files")
    print("took "+str(delta.total_seconds()))
    
    self.numberoftimeintervals=self.results[last_b]["Displacements"][last_v].shape[0]
    self.dT=deltaT
    self.numberofframes_ina_second=1.0/self.dT
    self.totaltime=self.dT*self.numberoftimeintervals
    
    print("delta t, the total time and number of frames in a second:")
    print(self.dT,self.totaltime,self.numberofframes_ina_second)
    print("setting np coords as reference")
    start=datetime.datetime.now()
    dx_zero = numpy.array([[0.0,0.0,0.0]])
    dc_zero = numpy.array([[0.0,0.0,0.0]])
    dval_zero = numpy.array([[0.0]])
    result_flags=["dX0","dX1","dX2","dXmag","StressReinfMean","StressConcMean","StrainReinfMean","StrainConcMean"]
    self.resultmaxmins={}
    for k in result_flags:
        self.resultmaxmins[k]=[]
    for v in self.post_eq_city.vertices.values():
        x = numpy.array([[v.coordsX[0],v.coordsX[1],v.coordsX[2]]])
        v.coordsx=numpy.repeat(x, repeats=self.numberoftimeintervals, axis=0)
        v.coordsXT=numpy.repeat(x, repeats=self.numberoftimeintervals, axis=0)
        v.dXT=numpy.repeat(dx_zero, repeats=self.numberoftimeintervals, axis=0)
        v.dXmag=numpy.repeat(dval_zero, repeats=self.numberoftimeintervals, axis=0)
        v.StressReinfMean=numpy.repeat(dval_zero, repeats=self.numberoftimeintervals, axis=0)
        v.StressConcMean=numpy.repeat(dval_zero, repeats=self.numberoftimeintervals, axis=0)
        v.StrainReinfMean=numpy.repeat(dval_zero, repeats=self.numberoftimeintervals, axis=0)
        v.StrainConcMean=numpy.repeat(dval_zero, repeats=self.numberoftimeintervals, axis=0)
        for k in result_flags:
            v.rColorMaps[k]=numpy.repeat(dc_zero, repeats=self.numberoftimeintervals, axis=0)
        v.rColorMap_activ=numpy.repeat(dc_zero, repeats=self.numberoftimeintervals, axis=0)
    end=datetime.datetime.now()
    delta=end-start
    print("np coords set as reference")
    print("took "+str(delta.total_seconds()))
    
    print("updating np dX coords")
    start=datetime.datetime.now()
    self.modified_vertices=[]
    for b in self.results.keys():
        for vid in self.results[b]["Displacements"].keys():
            current_vertex_id=self.post_eq_city.femid2vertexid[str(vid)]
            self.post_eq_city.vertices[current_vertex_id].dXT=self.results[b]["Displacements"][vid]
            self.post_eq_city.vertices[current_vertex_id].dXmag[:,0]=numpy.linalg.norm(self.post_eq_city.vertices[current_vertex_id].dXT[:,0:3],axis=1)
        
        for vid in self.femvertexids[b]:
            current_vertex_id=self.post_eq_city.femid2vertexid[str(vid)]
            self.modified_vertices.append(current_vertex_id)
            node_vals=numpy.array([self.results[b]["StressReinf"][str(cid)] for cid in self.post_eq_city.vertices[current_vertex_id].home_columns])
            self.post_eq_city.vertices[current_vertex_id].StressReinfMean=numpy.mean(node_vals, axis=0)
            node_vals=numpy.array([self.results[b]["StressConc"][str(cid)] for cid in self.post_eq_city.vertices[current_vertex_id].home_columns])
            self.post_eq_city.vertices[current_vertex_id].StressConcMean=numpy.mean(node_vals, axis=0)
            node_vals=numpy.array([self.results[b]["StrainReinf"][str(cid)] for cid in self.post_eq_city.vertices[current_vertex_id].home_columns])
            self.post_eq_city.vertices[current_vertex_id].StrainReinfMean=numpy.mean(node_vals, axis=0)
            node_vals=numpy.array([self.results[b]["StrainConc"][str(cid)] for cid in self.post_eq_city.vertices[current_vertex_id].home_columns])
            self.post_eq_city.vertices[current_vertex_id].StrainConcMean=numpy.mean(node_vals, axis=0)
            
    end=datetime.datetime.now()
    delta=end-start
    print("np dX coords updated")
    print("took "+str(delta.total_seconds()))

    print("setting initial color map")
    start=datetime.datetime.now()
    self.cmap = matplotlib.cm.get_cmap("rainbow")
    self.calculate_colormap_values()
    self.set_scalar_result("Displacement Mag") # initial result
    end=datetime.datetime.now()
    delta=end-start
    print("initial color values are set")
    print("took "+str(delta.total_seconds()))

    print(self.numberoftimeintervals)
    self.dial.setMaximum(self.numberoftimeintervals)
    self.dial.setSingleStep(self.dT)
    self.dial.valueChanged.connect(self.set_timelabel)
    self.Start_Animation_Push_Button.clicked.connect(self.animatewindow)
    print("result reading finished")
