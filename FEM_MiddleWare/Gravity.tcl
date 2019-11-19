# ###################
# GRAVITY -------------------------------------------------------------
# define GRAVITY load applied to beams and columns -- eleLoad applies loads in local coordinate axis

pattern Plain 101 Linear {
for {set numInFile 0} {$numInFile <= [expr $Buildingnum-1]} {incr numInFile 1} {
	for {set i 0} {$i <= [expr [llength [lindex $LCol $numInFile]]-1]} {incr i 1} {
		eleLoad -ele [lindex $LCol $numInFile $i 0] -type -beamUniform 0. 0. -$QdlCol; 	# COLUMNS
	}
	for {set i 0} {$i <= [expr [llength [lindex $LBeam $numInFile]]-1]} {incr i 1} {
		eleLoad -ele [lindex $LBeam $numInFile $i 0]  -type -beamUniform -[lindex $QdlBeam $numInFile $i 1] 0.; 	# BEAMS
	}
	for {set i 0} {$i <= [expr [llength [lindex $LGird $numInFile]]-1]} {incr i 1} {
		eleLoad -ele [lindex $LGird $numInFile $i 0]  -type -beamUniform -$QdlGird 0.;	# GIRDS
	}
}
}; # Pattern plain 101 linear close 

puts goGravity
# Gravity-analysis parameters -- load-controlled static analysis
set Tol 1.0e-8;			# convergence tolerance for test
variable constraintsTypeGravity Plain;		# default;