# Seperate beam elements (X-Z plane) into Beam and Girder elements
# Overwrite the input file after seperation
import sys
import math
import numpy as np

def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
# Returns the angle in radians between vectors 'v1' and 'v2'::
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def elem_len(inodecoordList,ieltnodeList):
	elemlenList=[]
	for i in range(len(ieltnodeList)):
		elemlenListtmp=[]
		for j in range(len(inodecoordList)):
			if ieltnodeList[i][1]==inodecoordList[j][0]:
				nodeI_X=float(inodecoordList[j][1])
				nodeI_Y=float(inodecoordList[j][2])
				nodeI_Z=float(inodecoordList[j][3])
			if ieltnodeList[i][2]==inodecoordList[j][0]:
				nodeJ_X=float(inodecoordList[j][1])
				nodeJ_Y=float(inodecoordList[j][2])
				nodeJ_Z=float(inodecoordList[j][3])
		elemlenListtmp.append(int(ieltnodeList[i][0]))
		elemlentmp=pow((nodeJ_X-nodeI_X),2)+pow((nodeJ_Y-nodeI_Y),2)+pow((nodeJ_Z-nodeI_Z),2)
		elemlen=math.sqrt(elemlentmp)
		elemlenListtmp.append(elemlen)
		elemlenList.append(elemlenListtmp)
	return elemlenList

def assign_vector_from_eltID(eltID):
	vector_from_eltID=[]
	for i in range(len(elemlenList)):
		if int(eltID) == int(ieltnodeList[i][0]):
			for j in range(len(inodecoordList)):
				if ieltnodeList[i][1]==inodecoordList[j][0]:
					nodeI_X=float(inodecoordList[j][1])
					nodeI_Y=float(inodecoordList[j][2])
					nodeI_Z=float(inodecoordList[j][3])
				if ieltnodeList[i][2]==inodecoordList[j][0]:
					nodeJ_X=float(inodecoordList[j][1])
					nodeJ_Y=float(inodecoordList[j][2])
					nodeJ_Z=float(inodecoordList[j][3])
	vec_X=nodeJ_X-nodeI_X
	vec_Y=nodeJ_Y-nodeI_Y
	vec_Z=nodeJ_Z-nodeI_Z
	vector_from_eltID.append(vec_X)
	vector_from_eltID.append(vec_Y)
	vector_from_eltID.append(vec_Z)
	return vector_from_eltID

def assign_element_type(inodecoordList,ieltnodeList,elemlenList):
	# element types are BEAMS and GIRDERS
	# types depend on vector orientations to a Base
	# Base is inital BEAM element 
	maxlength=0.0
	Beam_elt_List=[]
	Girder_elt_List=[]
	for  i in range(len(elemlenList)):
		if maxlength < elemlenList[i][1]:
			maxlength = elemlenList[i][1]
			maxlength_eltID = elemlenList[i][0]
			_index=i
	init_Beam_elt=maxlength_eltID
	# Take the element with max length as base for angle calculations to ensure variety of types
	vector_from_eltID_init = assign_vector_from_eltID(init_Beam_elt)
	Beam_elt_Listtmp=[]
	Girder_elt_Listtmp=[]
	for i in range(len(elemlenList)):
		Beam_elt = elemlenList[i][0]
		vector_from_eltID = assign_vector_from_eltID(Beam_elt)
		anglebtw=angle_between(vector_from_eltID_init, vector_from_eltID)
		if ((anglebtw > 0.785398) or math.isclose(anglebtw, 0.785398, abs_tol = 0.04)) and ((anglebtw < 2.35619) or math.isclose(anglebtw, 2.35619, abs_tol = 0.04)):
			Girder_elt_Listtmp.append(ieltnodeList[i][0])
			Girder_elt_Listtmp.append(ieltnodeList[i][1])
			Girder_elt_Listtmp.append(ieltnodeList[i][2])
			Girder_elt_List.append(Girder_elt_Listtmp)
			Girder_elt_Listtmp=[]
		elif ((anglebtw > 3.92699) or math.isclose(anglebtw, 3.92699, abs_tol = 0.04)) and ((anglebtw < 5.49779) or math.isclose(anglebtw, 5.49779, abs_tol = 0.04)):
			Girder_elt_Listtmp.append(ieltnodeList[i][0])
			Girder_elt_Listtmp.append(ieltnodeList[i][1])
			Girder_elt_Listtmp.append(ieltnodeList[i][2])
			Girder_elt_List.append(Girder_elt_Listtmp)
			Girder_elt_Listtmp=[]
		elif (anglebtw == 0.0) or math.isclose(anglebtw, 0.0, abs_tol = 0.04):
			Beam_elt_Listtmp.append(ieltnodeList[i][0])
			Beam_elt_Listtmp.append(ieltnodeList[i][1])
			Beam_elt_Listtmp.append(ieltnodeList[i][2])
			Beam_elt_List.append(Beam_elt_Listtmp)
			Beam_elt_Listtmp=[]
		elif (anglebtw == 3.14159) or math.isclose(anglebtw, 3.14159, abs_tol = 0.04):
			Beam_elt_Listtmp.append(ieltnodeList[i][0])
			Beam_elt_Listtmp.append(ieltnodeList[i][1])
			Beam_elt_Listtmp.append(ieltnodeList[i][2])
			Beam_elt_List.append(Beam_elt_Listtmp)
			Beam_elt_Listtmp=[]
		else:
			Beam_elt_Listtmp.append(ieltnodeList[i][0])
			Beam_elt_Listtmp.append(ieltnodeList[i][1])
			Beam_elt_Listtmp.append(ieltnodeList[i][2])
			Beam_elt_List.append(Beam_elt_Listtmp)
			Beam_elt_Listtmp=[]
	return Beam_elt_List, Girder_elt_List

def read_initial(inputfile):
	filepath = open(inputfile,'r')	
	with filepath as f:
		line=1
		inodecoordList=[]
		ieltnodeList=[]
		while line:
			nodecoordList=[]
			eltnodeList=[]
			line=f.readline()
			word=line.split()
			if "node" in word:
				nodeid=word[1]
				coordX=word[2]
				coordY=word[3]
				coordZ=word[4]
				nodecoordList=[nodeid, coordX, coordY, coordZ]
				inodecoordList.append(nodecoordList)
			if "beam" in word:
				eltid=word[1]
				nodeI=word[2]
				nodeJ=word[3]
				eltnodeList=[eltid, nodeI, nodeJ]
				ieltnodeList.append(eltnodeList)
	filepath.close()
	return inodecoordList, ieltnodeList

def write_input(inputfile, outputfile,elemlenList, Beam_elt_List, Girder_elt_List):
	outfile = open(outputfile,"w+")
	filepath = open(inputfile,'r')
	with filepath as f:
		line=1
		checkcomment=1
		while line:
			line=f.readline()
			word=line.split()
			if "beam" in word:
				check=1
				for j in range(len(elemlenList)):
					for i in range(len(Beam_elt_List)):
						if word[1]==Beam_elt_List[i][0] and check==1:
							outfile.write("beam\t")
							for element in Beam_elt_List[i]:
								outfile.write(element)
								outfile.write("\t")
							outfile.write('\n')
							check=0
				check=1
				for j in range(len(elemlenList)):
					for i in range(len(Girder_elt_List)):
						if word[1]==Girder_elt_List[i][0] and check==1:
							if checkcomment==1:
								outfile.write("#GIRDER")
								outfile.write('\n')
								checkcomment=0
							outfile.write("girder\t")
							for element in Girder_elt_List[i]:
								outfile.write(element)
								outfile.write("\t")
							outfile.write('\n')
							check=0
			else:
				outfile.write(line)
	outfile.close()
	filepath.close()

if __name__ == '__main__':
    inodecoordList,ieltnodeList = read_initial(*sys.argv[1:2])
    elemlenList = elem_len(inodecoordList,ieltnodeList)
    Beam_elt_List,Girder_elt_List = assign_element_type(inodecoordList,ieltnodeList,elemlenList)
    write_input(*sys.argv[1:],elemlenList, Beam_elt_List, Girder_elt_List)