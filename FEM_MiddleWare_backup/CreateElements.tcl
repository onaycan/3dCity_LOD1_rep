#
#	CREATE ELEMENTS
#

for {set k 0} {$k <= [expr [llength [lindex $iBeamConnect $numInFile]]-1]} {incr k 1} {;	# For Beams
	set elemID [lindex $iBeamConnect $numInFile $k 0]
	set nodeI [lindex $iBeamConnect $numInFile $k 1]
	set nodeJ [lindex $iBeamConnect $numInFile $k 2]
	element nonlinearBeamColumn $elemID $nodeI $nodeJ $numIntgrPts $BeamSecTag $elemID;	# beams
}


for {set k 0} {$k <= [expr [llength [lindex $iGirderConnect $numInFile]]-1]} {incr k 1} {;	# For Girds
	set elemID [lindex $iGirderConnect $numInFile $k 0]
	set nodeI [lindex $iGirderConnect $numInFile $k 1]
	set nodeJ [lindex $iGirderConnect $numInFile $k 2]
	element nonlinearBeamColumn $elemID $nodeI $nodeJ $numIntgrPts $GirdSecTag $elemID;		# Girds
}
	
	
for {set k 0} {$k <= [expr [llength [lindex $iColumnConnect $numInFile]]-1]} {incr k 1} {;	# For columns
	set elemID [lindex $iColumnConnect $numInFile $k 0]
	set nodeI [lindex $iColumnConnect $numInFile $k 1]
	set nodeJ [lindex $iColumnConnect $numInFile $k 2]
	element nonlinearBeamColumn $elemID $nodeI $nodeJ $numIntgrPts $ColSecTag $elemID;		# columns
}
# ------------------------  rigidDiaphragm ------------------------------------------------------	
for {set k 0} {$k <= [expr [lindex $NStory $numInFile]-1]} {incr k 1} {
	for {set i 0} {$i <= [expr [llength [lindex $ifloornodes $numInFile $k]]-1]} {incr i 1} {
		rigidDiaphragm 2 [lindex $iMasterNode $numInFile $k] [lindex $ifloornodes $numInFile $k $i 0]
	}
}
