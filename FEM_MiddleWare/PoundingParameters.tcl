#
#	POUNDING PARAMETERS
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
#uniaxialMaterial Elastic $matTag $E;
uniaxialMaterial Elastic 6 1.0e2;
uniaxialMaterial Elastic 7 1.0e3;
#
#
