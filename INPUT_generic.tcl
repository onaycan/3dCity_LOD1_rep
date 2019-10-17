#BUILDING    .... building ID
set BuildingID ID;
#NSTOREY
set NStory n;			# number of stories above ground level
#NBAY
set NBay n;				# number of bays in X direction
#NBAYZ
set NBayZ n;			# number of bays in Z direction
#NODE
node NodeID X Y Z	.... corners on Ground Level including Bays
node NodeID X Y Z
node NodeID X Y Z
node NodeID X Y Z
node NodeID X Y Z	.... corners on 1st Floor Ground including Bays
node NodeID X Y Z
node NodeID X Y Z
node NodeID X Y Z
node NodeID X Y Z	.... corners on 2nd Floor Ground including Bays
node NodeID X Y Z
node NodeID X Y Z
node NodeID X Y Z
node NodeID X Y Z  .... corners on the Roof plane
node NodeID X Y Z
node NodeID X Y Z
node NodeID X Y Z
#MASTERNODE     .... Geometrically center node on each Storey
node MasterNodeID X Y Z	.... Ground Level 
node MasterNodeID X Y Z	.... 1st Floor
node MasterNodeID X Y Z	.... 2nd Floor
node MasterNodeID X Y Z	.... Roof Plane
#RIGID   	.... rigidDiaphragm (MASTERNODE ID's and other NODE ID's on the same storey plane)
rigidDiaphragm 2 MasterNodeID NodeID NodeID NodeID NodeID     .... Ground Level 
rigidDiaphragm 2 MasterNodeID NodeID NodeID NodeID NodeID      .... 1st Floor
rigidDiaphragm 2 MasterNodeID NodeID NodeID NodeID NodeID      .... 2nd Floor
rigidDiaphragm 2 MasterNodeID NodeID NodeID NodeID NodeID      .... Roof Plane
#BEAM  -- parallel to x axis
element nonlinearBeamColumn ElementID NodeID NodeID 5 2 2  .... 1st Floor
element nonlinearBeamColumn ElementID NodeID NodeID 5 2 2 
element nonlinearBeamColumn ElementID NodeID NodeID 5 2 2 .... 2nd Floor
element nonlinearBeamColumn ElementID NodeID NodeID 5 2 2
element nonlinearBeamColumn ElementID NodeID NodeID 5 2 2 .... Roof Plane
element nonlinearBeamColumn ElementID NodeID NodeID 5 2 2
#BEAMLENGTH
  ElementID LENGTH
  ElementID LENGTH
  ElementID LENGTH
  ElementID LENGTH
  ElementID LENGTH
  ElementID LENGTH
#GIRDER  -- parallel to z axis
element nonlinearBeamColumn ElementID NodeID NodeID 5 3 3  .... 1st Floor
element nonlinearBeamColumn ElementID NodeID NodeID 5 3 3
element nonlinearBeamColumn ElementID NodeID NodeID 5 3 3  .... 2nd Floor
element nonlinearBeamColumn ElementID NodeID NodeID 5 3 3
element nonlinearBeamColumn ElementID NodeID NodeID 5 3 3 .... Roof Plane
element nonlinearBeamColumn ElementID NodeID NodeID 5 3 3
*GIRDERLENGTH
  ElementID LENGTH
  ElementID LENGTH
  ElementID LENGTH
  ElementID LENGTH
  ElementID LENGTH
  ElementID LENGTH
# COLUMN   -- parallel to y axis
# 5 is number of Gauss integration points for nonlinear curvature distribution, 1's are unique Tags
element nonlinearBeamColumn ElementID NodeID NodeID 5 1 1 .... 1st Floor 
element nonlinearBeamColumn ElementID NodeID NodeID 5 1 1	 
element nonlinearBeamColumn ElementID NodeID NodeID 5 1 1 .... 2nd Floor
element nonlinearBeamColumn ElementID NodeID NodeID 5 1 1
element nonlinearBeamColumn ElementID NodeID NodeID 5 1 1 .... Roof Plane
element nonlinearBeamColumn ElementID NodeID NodeID 5 1 1
#COLUMNLENGTH
  FixColumnLength
#

