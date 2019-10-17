#BUILDING
set BuildingID 1;
#NSTOREY
set NStory 3;			# number of stories above ground level
#NBAY
set NBay 1;				# number of bays in X direction
#NBAYZ
set NBayZ 1;			# number of bays in Z direction
#NODE
node 1 0 0 0
node 2 0 0 1
node 3 1 0 1
node 4 1 0 0
node 5 0 1 0
node 6 0 1 1
node 7 1 1 1
node 8 1 1 0
node 9 0 2 0
node 10 0 2 1
node 11 1 2 1
node 12 1 2 0
node 13 0 3 0
node 14 0 3 1
node 15 1 3 1
node 16 1 3 0
#MASTERNODE
node 17 0.5 0 0.5	
node 18 0.5 1 0.5 
node 19 0.5 2 0.5 
node 20 0.5 3 0.5 
#RIGID
rigidDiaphragm 2 17 1 2 3 4
rigidDiaphragm 2 18 5 6 7 8
rigidDiaphragm 2 19 9 10 11 12
rigidDiaphragm 2 20 13 14 15 16
#BEAM
element nonlinearBeamColumn 1 6 7 5 2 2
element nonlinearBeamColumn 2 8 5 5 2 2
element nonlinearBeamColumn 3 10 11 5 2 2
element nonlinearBeamColumn 4 12 9 5 2 2
element nonlinearBeamColumn 5 14 15 5 2 2
element nonlinearBeamColumn 6 16 13 5 2 2		
#BEAMLENGTH
set Beamlength_1 1
set Beamlength_2 1
set Beamlength_3 1
set Beamlength_4 1	
set Beamlength_5 1
set Beamlength_6 1
#GIRDER
element nonlinearBeamColumn 7 5 6 5 3 3
element nonlinearBeamColumn 8 7 8 5 3 3
element nonlinearBeamColumn 9 9 10 5 3 3
element nonlinearBeamColumn 10 11 12 5 3 3
element nonlinearBeamColumn 11 13 14 5 3 3
element nonlinearBeamColumn 12 15 16 5 3 3   	
#GIRDERLENGTH
set Beamlength_7 1
set Beamlength_8 1
set Beamlength_9 1
set Beamlength_10 1	
set Beamlength_11 1
set Beamlength_12 1
#COLUMN
element nonlinearBeamColumn 13 1 5 5 1 1
element nonlinearBeamColumn 14 2 6 5 1 1
element nonlinearBeamColumn 15 3 7 5 1 1
element nonlinearBeamColumn 16 4 8 5 1 1
element nonlinearBeamColumn 17 5 9 5 1 1
element nonlinearBeamColumn 18 6 10 5 1 1
element nonlinearBeamColumn 19 7 11 5 1 1
element nonlinearBeamColumn 20 8 12 5 1 1
element nonlinearBeamColumn 21 9 13 5 1 1
element nonlinearBeamColumn 22 10 14 5 1 1
element nonlinearBeamColumn 23 11 15 5 1 1
element nonlinearBeamColumn 24 12 16 5 1 1
#COLUMNLENGTH
set Columnlength_fix 1
#
