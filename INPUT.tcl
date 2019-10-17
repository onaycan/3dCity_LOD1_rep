#BUILDING
set BuildingID 1;
#NSTOREY
set NStory 3;			# number of stories above ground level
#NBAY
set NBay 1;				# number of bays in X direction
#NBAYZ
set NBayZ 1;			# number of bays in Z direction
#FREENODE
set FreeNodeID 15;					# ID: free node  to output results
#GROUNDNODES
node 1 0 0 0
node 2 0 0 288
node 3 288 0 288
node 4 288 0 0
#STOREYNODES_first
node 5 0 168 0
node 6 0 168 288
node 7 288 168 288
node 8 288 168 0
#STOREYNODES_second
node 9 0 336 0
node 10 0 336 288
node 11 288 336 288
node 12 288 336 0
#STOREYNODES_third
node 13 0 504 0
node 14 0 504 288
node 15 288 504 288
node 16 288 504 0
#MASTERNODES
node 17 144 168 144 
node 18 144 336 144 
node 19 144 504 144 
#RIGID
rigidDiaphragm 2 17 5 6 7 8
rigidDiaphragm 2 18 9 10 11 12
rigidDiaphragm 2 19 13 14 15 16
#BEAM
element nonlinearBeamColumn 1 6 7 5 2 2
element nonlinearBeamColumn 2 8 5 5 2 2
element nonlinearBeamColumn 3 10 11 5 2 2
element nonlinearBeamColumn 4 12 9 5 2 2
element nonlinearBeamColumn 5 14 15 5 2 2
element nonlinearBeamColumn 6 16 13 5 2 2		
#BEAMLENGTH
set Beamlength_1 288
set Beamlength_2 288
set Beamlength_3 288
set Beamlength_4 288	
set Beamlength_5 288
set Beamlength_6 288
#GIRDER
element nonlinearBeamColumn 7 5 6 5 3 3
element nonlinearBeamColumn 8 7 8 5 3 3
element nonlinearBeamColumn 9 9 10 5 3 3
element nonlinearBeamColumn 10 11 12 5 3 3
element nonlinearBeamColumn 11 13 14 5 3 3
element nonlinearBeamColumn 12 15 16 5 3 3   	
#GIRDERLENGTH
set Beamlength_7 288
set Beamlength_8 288
set Beamlength_9 288
set Beamlength_10 288
set Beamlength_11 288
set Beamlength_12 288
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
set Columnlength_fix 168
#END
