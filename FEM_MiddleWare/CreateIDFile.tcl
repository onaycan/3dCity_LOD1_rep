#
#	Puts the node ID'S in a file for evaluation process
#
#
#
set outFileFloorNodeIDName $dataDir/NodeIDs.out
#set outFileNodeIDName $dataDir/NodeIDs.out
set outFileEltIDName $dataDir/ElementIDs.out
set outFileBeamEltIDName $dataDir/BeamElementIDs.out
set outFileGirderEltIDName $dataDir/GirderElementIDs.out
set outFileColumnEltIDName $dataDir/ColumnElementIDs.out

	set outFileFloorNodeID [open $outFileFloorNodeIDName w]
#    set outFileNodeID [open $outFileNodeIDName w]
	set outFileEltID [open $outFileEltIDName w]
    set outFileBeamEltID [open $outFileBeamEltIDName w]
    set outFileGirderEltID [open $outFileGirderEltIDName w]
    set outFileColumnEltID [open $outFileColumnEltIDName w]
	
for {set numInFile 0} {$numInFile <= [expr $Buildingnum-1]} {incr numInFile 1} {
	for {set i 0} {$i <= [expr [lindex $NStory $numInFile]-1]} {incr i 1} {
		for {set j 0} {$j <= [expr [lindex $nodecount $i]-1]} {incr j 1} {
		puts [lindex $ifloornodes $numInFile $i $j 0]
			puts $outFileFloorNodeID [lindex $ifloornodes $numInFile $i $j 0]
		}
	}

#	for {set i 0} {$i <= [expr [llength [lindex $iNodeList $numInFile]]-1]} {incr i 1} {	
#		puts $outFileNodeID [lindex $iNodeList $numInFile $i 0]
#	}

	for {set i 0} {$i <= [expr [llength [lindex $iElementwColumns $numInFile]]-1]} {incr i 1} {	
		puts $outFileEltID [lindex $iElementwColumns $numInFile $i 0]
	}
	
	for {set i 0} {$i <= [expr [llength [lindex $iBeamConnect $numInFile]]-1]} {incr i 1} {	
		puts $outFileBeamEltID [lindex $iBeamConnect $numInFile $i 0]
	}
	
	for {set i 0} {$i <= [expr [llength [lindex $iGirderConnect $numInFile]]-1]} {incr i 1} {	
		puts $outFileGirderEltID [lindex $iGirderConnect $numInFile $i 0]
	}
	
	for {set i 0} {$i <= [expr [llength [lindex $iColumnConnect $numInFile]]-1]} {incr i 1} {	
		puts $outFileColumnEltID [lindex $iColumnConnect $numInFile $i 0]
	}
}
	close $outFileFloorNodeID
#    close $outFileNodeID
	close $outFileEltID
    close $outFileBeamEltID
    close $outFileGirderEltID
    close $outFileColumnEltID
                                                                                                                                  #
