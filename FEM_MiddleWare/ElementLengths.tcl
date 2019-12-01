#
# Length of each Beam element
#
# Argument: ElementID to be investigated
#			NodeIDList -> list of Node ID's
#			iElementConnect -> List of Element ID's and their connectivities
#
# Returns: Length of the Element
#
#
proc ElementLengths {elementid iNodeList iElementConnect numInFile}  {
	for {set k 0} {$k <= [expr [llength [lindex $iElementConnect $numInFile]]-1]} {incr k 1} {
		if {$elementid == [lindex $iElementConnect $numInFile $k 0]} {
			set Node1 [lindex $iElementConnect $numInFile $k 1]
			set Node2 [lindex $iElementConnect $numInFile $k 2]
		} 
	}
	for {set m 0} {$m <= [expr [llength [lindex $iNodeList $numInFile]]-1]} {incr m 1} {
		if {$Node1==[lindex $iNodeList $numInFile $m 0]} {
			set vecxztmp1x [lindex $iNodeList $numInFile $m 1]; # Node coordinates
			set vecxztmp1y [lindex $iNodeList $numInFile $m 2]
			set vecxztmp1z [lindex $iNodeList $numInFile $m 3]
		}
		if {$Node2==[lindex $iNodeList $numInFile $m 0]} {
			set vecxztmp2x [lindex $iNodeList $numInFile $m 1]; # Node coordinates
			set vecxztmp2y [lindex $iNodeList $numInFile $m 2]
			set vecxztmp2z [lindex $iNodeList $numInFile $m 3]
		}
	}
	set tmpelementlength [expr pow(($vecxztmp2x-$vecxztmp1x),2)+pow(($vecxztmp2y-$vecxztmp1y),2)+pow(($vecxztmp2z-$vecxztmp1z),2)]
	set elementlength [expr sqrt($tmpelementlength)]
	set LenElt $elementlength

	return $LenElt
}
#
# 	Total sum length of elements (List) on each floor each building for distribution of weight proportional to lengths of elements to total sum
set TotalLenElts ""
for {set i 0} {$i <= [expr [lindex $NStory $numInFile]-1]} {incr i 1} {
	set TotalLenEltstmp 0.0
	for {set j 0} {$j <= [expr [llength [lindex $iElements_Floor $numInFile $i]]-1]} {incr j 1} {
		set elementid [lindex $iElements_Floor $numInFile $i $j]
		set aLenElt [ElementLengths $elementid $iNodeList $iElementConnect $numInFile]
		set TotalLenEltstmp [expr $TotalLenEltstmp+$aLenElt]
	}
	lappend TotalLenElts $TotalLenEltstmp
}
lappend iTotalLenElts $TotalLenElts
#
# Percent % of element lengths to the total length of an element on that floor
#
proc  PercentEltLength {elementid NStory iElements_Floor iTotalLenElts iNodeList iElementConnect numInFile}  {
	for {set i 0} {$i <= [expr [lindex $NStory $numInFile]-1]} {incr i 1} {
		for {set j 0} {$j <= [expr [llength [lindex $iElements_Floor $numInFile $i]]-1]} {incr j 1} {
			if {$elementid == [lindex $iElements_Floor $numInFile $i $j]} {
				#set aLenElt [ElementLengths $elementid $iNodeList $iElementConnect $numInFile]
				set aLenElt2TotalLenElts [expr 1/[lindex $iTotalLenElts $numInFile $i]]
			}			
		}
	}
	return $aLenElt2TotalLenElts
}
	
	
	