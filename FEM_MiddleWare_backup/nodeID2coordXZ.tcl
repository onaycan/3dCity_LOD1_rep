#
#  NODE ID to COORDINATES X-Z
#
# Argument: NodeIDList -> list of Node ID's
#
# Returns: List of coordinates X and Z for each nodes in NodeIDList
#
#
proc nodeID2coordXZ {NodeIDList iNodeList numInFile}  {
	for {set i 0} {$i <= [expr [llength $NodeIDList]-1]} {incr i 1} {
		for {set j 0} {$j <= [expr [llength [lindex $iNodeList $numInFile]]-1]} {incr j 1} {
			if {[lindex $NodeIDList $i]==[lindex $iNodeList $numInFile $j 0]} {
				set coordX [lindex $iNodeList $numInFile $j 1]
				set coordZ [lindex $iNodeList $numInFile $j 3]
			}
		}
		lappend CoordXZList $coordX
		lappend CoordXZList $coordZ
	}
	return $CoordXZList
}
