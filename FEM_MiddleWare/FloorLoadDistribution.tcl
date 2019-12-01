#
#	DEAD LOAD DISTRIBUTION ON FLOOR FRAMES
#
# 	Floor weight is distributed among beams as Dead Loads
#	Unknown interior Frames and irregular shapes make slab geometries unknown
#	This script takes the whole floor area to find out the total weight and distribute it among surrounding beams/girders 
#	In case of interior columns, surface area is divided into sub-areas and recursively the process is repeated on sub-areas (not implemented yet)
#		An Interior Frame (Column-Beam creation) algorithm should be implemented and will definitely change the algorithms in this script!!!!!
#	by: Serhat Adilak, 2019
#

# --------------------------  Exterior Node IDs  ----------------------------------------  IGNORE HERE!!!!!!!! FAULT
set exteriornodesID ""
for {set k 0} {$k <= [expr [lindex $NStory $numInFile]-1]} {incr k 1} {;	#first exterior search !!! [lindex $ifloornodes $numInFile $i $j 1]
	set maxX 0.0
	set maxZ 0.0
	set exteriornodesIDtmp ""
	set maxX [lindex $ifloornodes $numInFile $k 0 1]
	set maxZ [lindex $ifloornodes $numInFile $k 0 3]
	for {set i 0} {$i <= [expr [lindex $nodecount $k]-1]} {incr i 1} {
		if {$maxX <= [lindex $ifloornodes $numInFile $k $i 1]} {
			set maxX [lindex $ifloornodes $numInFile $k $i 1]; 	# max coordinate in X 
		}
		if {$maxZ <= [lindex $ifloornodes $numInFile $k $i 3]} {
			set maxZ [lindex $ifloornodes $numInFile $k $i 3];		# max coordinate in Z
		}	
	}
	set minX [lindex $ifloornodes $numInFile $k 0 1]
	set minZ [lindex $ifloornodes $numInFile $k 0 3]
	for {set i 0} {$i <= [expr [lindex $nodecount $k]-1]} {incr i 1} {
		if {$minX > [lindex $ifloornodes $numInFile $k $i 1]} {
			set minX [lindex $ifloornodes $numInFile $k $i 1]; 	# min coordinate in X
		}
		if {$minZ > [lindex $ifloornodes $numInFile $k $i 3]} {
			set minZ [lindex $ifloornodes $numInFile $k $i 3]; 	# min coordinate in Z
		}
	}
	for {set i 0} {$i <= [expr [lindex $nodecount $k]-1]} {incr i 1} {;	# give me those node id's for min/max coordinates
		if {$minX == [lindex $ifloornodes $numInFile $k $i 1]} {
			set exteriornodesIDtmp [lindex $ifloornodes $numInFile $k $i 0]
		}
		if {$maxX == [lindex $ifloornodes $numInFile $k $i 1]} {
			set exteriornodesIDtmp [lindex $ifloornodes $numInFile $k $i 0]
		}
		if {$minZ == [lindex $ifloornodes $numInFile $k $i 3]} {
			set exteriornodesIDtmp [lindex $ifloornodes $numInFile $k $i 0]
		}
		if {$maxZ == [lindex $ifloornodes $numInFile $k $i 3]} {
			set exteriornodesIDtmp [lindex $ifloornodes $numInFile $k $i 0]
		}
	}
	lappend exteriornodesID $exteriornodesIDtmp
}; # End of main loop	
lappend iexteriornodesID $exteriornodesID; # outermost nodes per floor each building

# ------------------------- NFRAME -------------------------
# Assumptions:  Take the number of Frames on a floor with respect to the number of Girders [((Total#Girder/2)+1]
# 				Since there is no information on the interior frames now, an easy way to calculate the NFrame is to consider Girder numbers
#				Total Girder number is divided into 2 even an asymmetric #girder distribution on irregular floor. 
# NOTE: This algorithm may be changed if an algorithm for interior will be implemented!!! 
set aNFrame ""
for {set i 0} {$i <= [expr [lindex $NStory $numInFile]-1]} {incr i 1} {
	set GirderCounttmp ""
	set NFrametmp ""
	for {set j 0} {$j <= [expr [llength [lindex $iGirders_Floor $numInFile $i]]-1]} {incr j 1} {
		set GirderCounttmp [expr $GirderCounttmp+1]; 	# Calculate the total Girder numbers at each Floor
	}

	set NFrametmp [expr ($GirderCounttmp/2)+1];	# NFrame formula with assumptions above mentioned
	lappend aNFrame $NFrametmp
}
lappend NFrame $aNFrame

# -----------------  Floor Total Weight------------------------------------------------------
# Assumptions:  No actual slab division since irregularities are considered without any interior elements information
#				Therefore the total floor weight is the total Area X thickness
#				The total area is found by shoelace polygon area formula considering exterior nodes 
#
# NOTE:		In case of interior information, a new algorithm will be implemented, to find sub-areas their weights to distribute it to sub-area surrounding elements.
#
set Tslab [expr 6*$in];			# 6-inch slab
#
set TotalAreaFloor ""
set ListElts_Floor ""
for {set i 0} {$i <= [expr [lindex $NStory $numInFile]-1]} {incr i 1} {
	for {set j 0} {$j <= [expr [llength [lindex $iElements_Floor $numInFile $i]]-1]} {incr j 1} {
		lappend ListElts_Floor [lindex $iElements_Floor $numInFile $i $j];	# Make a list of all elements on all floors
	}
}
set NodeList_ordered ""
for {set i 0} {$i <= [expr [lindex $NStory $numInFile]-1]} {incr i 1} {
	set aNode [lindex $iElements_Nodes_Floor $numInFile $i 0 1]; #set a seed node
	set aNodeList_ordered ""
	lappend NodeList_ordered $aNode
	lappend aNodeList_ordered $aNode
	for {set j 0} {$j <= [expr [llength [lindex $iElements_Nodes_Floor $numInFile $i]]-1]} {incr j 1} {
		if {[lindex $iElements_Nodes_Floor $numInFile $i $j 1]==$aNode} {
			set idx [lsearch -all $ListElts_Floor [lindex $iElements_Nodes_Floor $numInFile $i $j 0]]
			if {$idx!=""} {
				set aNode [lindex $iElements_Nodes_Floor $numInFile $i $j 2]
				set ListElts_Floor [lreplace $ListElts_Floor $idx $idx]
			}
		}
		if {[lindex $iElements_Nodes_Floor $numInFile $i $j 2]==$aNode} {
			set idx [lsearch -all $ListElts_Floor [lindex $iElements_Nodes_Floor $numInFile $i $j 0]]
			if {$idx!=""} {
				set aNode [lindex $iElements_Nodes_Floor $numInFile $i $j 1]
				set ListElts_Floor [lreplace $ListElts_Floor $idx $idx]
			}	
		}
		if {[lsearch -all $NodeList_ordered $aNode]==""} {
			lappend NodeList_ordered $aNode
			lappend aNodeList_ordered $aNode
		} 		
	}
	set coords [nodeID2coordXZ $aNodeList_ordered $iNodeList $numInFile]
	lappend TotalAreaFloor [polygonArea $coords]
}
lappend iTotalAreaFloor $TotalAreaFloor

#	Calculate the individual slab-like weights' lateral load distribution to the elements 
puts iBeams_Floor$iBeams_Floor
set QBeamSlab ""
set QGirderSlab ""
for {set i 0} {$i <= [expr [lindex $NStory $numInFile]-1]} {incr i 1} {
	set afloorarea [lindex $iTotalAreaFloor $numInFile $i]
	set QGirderSlabtmp ""
	set QBeamSlabtmp ""
	for {set j 0} {$j <= [expr [llength [lindex $iBeams_Floor $numInFile $i]]-1]} {incr j 1} {
		set elementid [lindex $iBeams_Floor $numInFile $i $j]
		set percentdistrib [PercentEltLength $elementid $NStory $iElements_Floor $iTotalLenElts $iNodeList $iElementConnect $numInFile]
		set selfload [expr $GammaConcrete*$Tslab*$afloorarea]
		set totalload [expr $LiveLoad + $selfload]; # Add live loads to floor weight, i.e. furniture etc.  --> Ib/ft2
		set totalloadperlength [expr $percentdistrib*$totalload]
		lappend QBeamSlabtmp $totalloadperlength; # Distribute the Floor weight w.r.t. exterior Beam Lengths
	}
	for {set j 0} {$j <= [expr [llength [lindex $iGirders_Floor $numInFile $i]]-1]} {incr j 1} {
		set elementid [lindex $iGirders_Floor $numInFile $i $j]
		set percentdistrib [PercentEltLength $elementid $NStory $iElements_Floor $iTotalLenElts $iNodeList $iElementConnect $numInFile]
		set selfload [expr $GammaConcrete*$Tslab*$afloorarea]
		set totalload [expr $LiveLoad + $selfload]; # Add live loads to floor weight, i.e. furniture etc. --> Ib/ft2
		set totalloadperlength [expr $percentdistrib*$totalload]
		lappend QGirderSlabtmp $totalloadperlength; # Distribute the Floor weight w.r.t. exterior Girder Lengths
	}
	lappend QBeamSlab $QBeamSlabtmp
	lappend QGirderSlab $QGirderSlabtmp
}
lappend iQBeamSlab $QBeamSlab
lappend iQGirderSlab $QGirderSlab

# Interior division case: search algorithm above will be reorganized with angle detect function below:
#set anglebtw [angle_btw_vec_from_EID $EID1 $EID2 $iBeamConnect $iGirderConnect $ifloornodes $numInFile]


	# give me all elements connected to those nodes:  in our case now, every elements on each floor are connected to those nodes since no interior.. ignore here
#	for {set i 0} {$i <= [expr [lindex $nodecount $k]-1]} {incr i 1} {; 	#search loop for exterior elements 
#		for {set j 0} {$j <= [expr [llength [lindex $iBeamConnect $numInFile]]-1]} {incr j 1} {
#			for {set k 0} {$k <= [expr [llength [lindex $iGirderConnect $numInFile]]-1]} {incr k 1} {
#				if {$exteriornodesIDtmp == [lindex $iBeamConnect $numInFile $j 1]} {
#					lappend beamnode1 [lindex $iBeamConnect $numInFile $i 1]
#					set beamnode2 [lindex $iBeamConnect $numInFile $i 2]
#					set checkbeam 1
#				} elseif {$exteriornodesIDtmp == [lindex $iGirderConnect $numInFile $j 1]} {
#					set beamnode1 [lindex $iGirderConnect $numInFile $i 1]
#					set beamnode2 [lindex $iGirderConnect $numInFile $i 2]
#					set checkbeam 1
#				}
#				if {$exteriornodesIDtmp == [lindex $iBeamConnect $numInFile $j 2]} {
#					set beamnode1 [lindex $iBeamConnect $numInFile $i 1]
#					set beamnode2 [lindex $iBeamConnect $numInFile $i 2]
#					set checkbeam 1
#				} elseif {$exteriornodesIDtmp == [lindex $iGirderConnect $numInFile $j 2]} {
#					set beamnode1 [lindex $iGirderConnect $numInFile $i 1]
#					set beamnode2 [lindex $iGirderConnect $numInFile $i 2]
#					set checkbeam 1
#				}
#			}
#		}
#	};# here the end of loop: the loop will find exterior nodes in a case which has interior nodes also.. now this loop is omitted.
#
