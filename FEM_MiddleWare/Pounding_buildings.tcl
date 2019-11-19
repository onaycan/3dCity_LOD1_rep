#
#	DIKKAT BU DAHA BI BASLANGIC; 
#
# ################################################# implementation of zeroLengthImpact3D with nodes in 3DOF domain:
model BasicBuilder -ndm 3 -ndf 3
node 30110122	576.0	336.0	0.0
node 30110222	576.0	336.0	288.0
node 30110131	576.0	336.0	0.0
node 30110231	576.0	336.0	288.0
node 20110122	576.0	168.0	0.0
node 20110222	576.0	168.0	288.0
node 20110131	576.0	168.0	0.0
node 20110231	576.0	168.0	288.0
model BasicBuilder -ndm 3 -ndf 6
equalDOF 30000122 30110122 1 2 3
equalDOF 30000222 30110222 1 2 3
equalDOF 30000131 30110131 1 2 3
equalDOF 30000231 30110231 1 2 3
equalDOF 20000122 20110122 1 2 3
equalDOF 20000222 20110222 1 2 3
equalDOF 20000131 20110131 1 2 3
equalDOF 20000231 20110231 1 2 3
#
set direction 1; # direction of normal of contact surface
set initGap 0.01; # initial gap  5cm = 1.97 inch
set frictionRatio 0.3; # friction ratio 
set mu 0.3; # friction coefficient 
set Kt 1.6e12; # penalty stiffness for tangential directions 		
set Kn 1.6e12; # penalty stiffness for normal direction		 
set Kn2 [expr $Kn * 0.1]; # penalty stiffness after yielding, based on Hertz impact model 
set Delta_y 0.1; # yield displacement based on Hertz impact model 	  
set cohesion 0; # cohesion
#
element zeroLengthImpact3D 3 30110131 30110122 $direction $initGap $frictionRatio $Kt $Kn $Kn2 $Delta_y $cohesion;
element zeroLengthImpact3D 4 30110231 30110222 $direction $initGap $frictionRatio $Kt $Kn $Kn2 $Delta_y $cohesion;
element zeroLengthImpact3D 5 20110131 20110122 $direction $initGap $frictionRatio $Kt $Kn $Kn2 $Delta_y $cohesion;
element zeroLengthImpact3D 6 20110231 20110222 $direction $initGap $frictionRatio $Kt $Kn $Kn2 $Delta_y $cohesion;
#
#uniaxialMaterial Elastic $matTag $E;
uniaxialMaterial Elastic 6 1.0e2;
uniaxialMaterial Elastic 7 1.0e3;
#element zeroLength $eleTag $iNode $jNode -mat $matTag1 $matTag2 ... -dir $dir1 $dir2 ... <-orient $x1 $x2 $x3 $yp1 $yp2 $yp3> <-doRayleigh $rFlag>
element zeroLength 30000 30110122 30110131 -mat 6 7 6 -dir 1 2 3; # springs with very low stiffness for convergance of Newton-Raphson method 
element zeroLength 40000 30110222 30110231 -mat 6 7 6 -dir 1 2 3; # springs with very low stiffness for convergance of Newton-Raphson method 
element zeroLength 50000 20110122 20110131 -mat 6 7 6 -dir 1 2 3; # springs with very low stiffness for convergance of Newton-Raphson method 
element zeroLength 60000 20110222 20110231 -mat 6 7 6 -dir 1 2 3; # springs with very low stiffness for convergance of Newton-Raphson method 
#
#
