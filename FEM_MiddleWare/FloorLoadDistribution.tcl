#
#	DEAD LOAD DISTRIBUTION ON FLOOR FRAMES
#
# 	Floor weight is distributed among beams as Dead Loads
#	Unknown interior Frames and irregular shapes make slab geometries unknown
#	This script takes the whole floor area to find out the total weight and distribute it among surrounding beams/girders 
#	In case of interior columns, surface area is divided into sub-areas and recursively the process is repeated on sub-areas
# 	
#	by: Serhat Adilak, 2019
#

# ------------------------------  Exterior Node IDs  ----------------------------------------
# ----------------------  NFrame Calculation  -----------------


#set anglebtw [angle_btw_vec_from_EID $EID1 $EID2 $iBeamConnect $iGirderConnect $ifloornodes $numInFile]


set exteriorGirdernodesID ""
set exteriornodesID ""
set exteriorGirdernodesID ""
set exteriorBeamnodesID ""	
set aNBayZ ""
set aNFrame ""
for {set k 0} {$k <= [expr [lindex $NStory $numInFile]-1]} {incr k 1} {;	#first find the seed for exterior search !!! [lindex $ifloornodes $numInFile $i $j 1]
	set maxX 0.0
	set maxZ 0.0
	set exteriornodestmp2 ""
	set exteriornodesIDtmp ""
	set maxX [lindex $ifloornodes $numInFile 0 1]
	set maxZ [lindex $ifloornodes $numInFile 0 3]
	for {set i 0} {$i <= [expr [lindex $nodecount $k]-1]} {incr i 1} {
		if {$maxX <= [lindex $ifloornodes $numInFile $i 1]} {
			set maxX [lindex $ifloornodes $numInFile $i 1]
		}
		if {$maxZ <= [lindex $ifloornodes $numInFile $i 3]} {
			set maxZ [lindex $ifloornodes $numInFile $i 3]
		}		
	}
	set minX [lindex $ifloornodes $numInFile 0 1]
	set minZ [lindex $ifloornodes $numInFile 0 3]
	for {set i 0} {$i <= [expr [lindex $nodecount $k]-1]} {incr i 1} {
		if {$minX > [lindex $ifloornodes $numInFile $i 1]} {
			set minX [lindex $ifloornodes $numInFile $i 1]
		}
		if {$minZ > [lindex $ifloornodes $numInFile $i 3]} {
			set minZ [lindex $ifloornodes $numInFile $i 3]
		}
	}
	for {set i 0} {$i <= [expr [lindex $nodecount $k]-1]} {incr i 1} {
		if {$minX == [lindex $ifloornodes $numInFile $i 1]} {
			set exteriornodesIDtmp [lindex $ifloornodes $numInFile $i 0]
		}
		if {$maxX == [lindex $ifloornodes $numInFile $i 1]} {
			set exteriornodesIDtmp [lindex $ifloornodes $numInFile $i 0]
		}
		if {$minZ == [lindex $ifloornodes $numInFile $i 3]} {
			set exteriornodesIDtmp [lindex $ifloornodes $numInFile $i 0]
		}
		if {$maxZ == [lindex $ifloornodes $numInFile $i 3]} {
			set exteriornodesIDtmp [lindex $ifloornodes $numInFile $i 0]
		}
	}
	for {set i 0} {$i <= [expr [lindex $nodecount $k]-1]} {incr i 1} {; 	#search loop for exterior elements
		for {set j 0} {$j <= [expr [llength [lindex $iBeamConnect $numInFile]]-1]} {incr j 1} {
			for {set k 0} {$k <= [expr [llength [lindex $iGirderConnect $numInFile]]-1]} {incr k 1} {
				if {$exteriornodesIDtmp == [lindex $iBeamConnect $numInFile $j 1]} {
					lappend beamnode1 [lindex $iBeamConnect $numInFile $i 1]
					set beamnode2 [lindex $iBeamConnect $numInFile $i 2]
					set checkbeam 1
				} elseif {$exteriornodesIDtmp == [lindex $iGirderConnect $numInFile $j 1]} {
					set beamnode1 [lindex $iGirderConnect $numInFile $i 1]
					set beamnode2 [lindex $iGirderConnect $numInFile $i 2]
					set checkbeam 1
				}
				if {$exteriornodesIDtmp == [lindex $iBeamConnect $numInFile $j 2]} {
					set beamnode1 [lindex $iBeamConnect $numInFile $i 1]
					set beamnode2 [lindex $iBeamConnect $numInFile $i 2]
					set checkbeam 1
				} elseif {$exteriornodesIDtmp == [lindex $iGirderConnect $numInFile $j 2]} {
					set beamnode1 [lindex $iGirderConnect $numInFile $i 1]
					set beamnode2 [lindex $iGirderConnect $numInFile $i 2]
					set checkbeam 1
				}
			}
		}
	}
	lappend exteriornodesID $exteriornodesIDtmp
	lappend aNBayZ [expr [llength [lindex $exteriorGirdernodesID $k]]/2-1]
	#lappend aNFrame [expr [llength [lindex $exteriorGirdernodesID $k]]/2]
	lappend aNFrame 2.0
	puts aNFrame$aNFrame
}
lappend iexteriornodesID $exteriornodesID; # outermost nodes per floor each building
lappend iexteriorGirdernodesID $exteriorGirdernodesID
lappend iexteriorBeamnodesID $exteriorBeamnodesID
lappend NBayZ $aNBayZ; #NBAYZ		# number of bays in Z direction
lappend NFrame $aNFrame;	# actually deal with frames in Z direction, as this is an easy extension of the 2d model

#set NFrame {{2 2 2}}


# -----------------  Floor Slabs Total Weight ------------------------------------------------------
#
#if [catch {open [lindex $ainputFilename $numInFile 0] r} inFileID] {
#	puts stderr "Cannot open input file for reading nodal weights"
#} else {
#  set flag 1
#	set floorcounter 0
#	set nodecounttmp 0
#	set floornodes ""
#	set nodecount ""
#	foreach line [split [read $inFileID] \n] {
#		if {[llength $line] == 0} {
#			# Blank line --> do nothing
#			continue
#		} 
#		if {$flag == 1} {
#			foreach word [split $line] {
#				if {[string match $word "#BUILDING"] == 1} {
#					break
#				}
#				if {[string match $word "#GROUND"] == 1} {
#					set flag2 1
#					break
#				}
#				if {[string match $word "#FLOOR"] == 1 || [string match $word "#MASTERNODES"] == 1} {
#					set flag2 0
#					if {$floorcounter>0} {
#						lappend floornodes $ifloornodestmp
#						lappend nodecount $nodecounttmp
#						set ifloornodestmp ""
#						set nodecounttmp 0
#					}
#					set floorcounter [expr $floorcounter+1]
#					
#					if {[string match $word "#MASTERNODES"] == 1} {
#						set flag2 1
#					} 
#					break
#				} else {
#				  if {$flag2 == 0} {
#					set list [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
#					foreach word [split $list] {
#						lappend ifloornodestmp $list
#						set nodecounttmp [expr $nodecounttmp+1]
#						break
#					}
#					break
#				  }
#				}
#			}; #end of split line 
#		}
#	}; #end of line read 
#	close $inFileID
#	}
#	lappend ifloornodes $floornodes



# Driver program to test above function 
#set coords {-1 0 0 1 0 -1 1 0 0 0}

#puts Polygonarea[polygonArea $coords]

