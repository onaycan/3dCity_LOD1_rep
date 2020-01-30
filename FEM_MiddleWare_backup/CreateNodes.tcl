#
#	Create Nodes
#
for {set m 0} {$m <= [expr [llength [lindex $nodeIDcheckList]]-1]} {incr m 1} {
set NodeList_2 ""
	for {set numInFile 0} {$numInFile <= [expr $Buildingnum-1]} {incr numInFile 1} {
		for {set i 0} {$i <= [expr [llength [lindex $iNodeList $numInFile]]-1]} {incr i 1} {
			if {[lindex $iNodeList $numInFile $i 0] == [lindex $nodeIDcheckList $m]} {
				set nodeID [lindex $iNodeList $numInFile $i 0]
				set X [lindex $iNodeList $numInFile $i 1]
				set Y [lindex $iNodeList $numInFile $i 2]
				set Z [lindex $iNodeList $numInFile $i 3]
			}
		}
	}
	lappend NodeList_2 $nodeID
	lappend NodeList_2 $X
	lappend NodeList_2 $Y
	lappend NodeList_2 $Z
	lappend iNodeList_2 $NodeList_2
}

for {set i 0} {$i <= [expr [llength $iNodeList_2]-1]} {incr i 1} {
	set nodeID [lindex $iNodeList_2 $i 0]	
	set X [lindex $iNodeList_2 $i 1]
	set Y [lindex $iNodeList_2 $i 2]
	set Z [lindex $iNodeList_2 $i 3]

	node $nodeID $X $Y $Z;		# actually define node
}
set SupportNodeIDList $nodeIDcheckList
for {set m 0} {$m <= [expr [llength [lindex $SupportNodeIDList]]-1]} {incr m 1} {
	for {set n 0} {$n <= [expr [llength [lindex $floornodeIDcheckList]]-1]} {incr n 1} {
		set floornodeID [lindex $floornodeIDcheckList $n]
		set idx [lsearch -all $SupportNodeIDList $floornodeID]
		if {$idx!=""} {
			set SupportNodeIDList [lreplace $SupportNodeIDList $idx $idx]; # floornodeIDs are removed from BC node List (ground nodes)	
		}
	}
}
# ------------------------  Boundary NODES ------------------------------------------------------
# determine support nodes where ground motions are input, for multiple-support excitation
for {set i 0} {$i <= [expr [llength $SupportNodeIDList]-1]} {incr i 1} {
	set nodeID [lindex $SupportNodeIDList $i]
	# BOUNDARY CONDITIONS
	fix $nodeID 1 1 1 0 1 0;		# pin all Ground Floor nodes
}

#
#

