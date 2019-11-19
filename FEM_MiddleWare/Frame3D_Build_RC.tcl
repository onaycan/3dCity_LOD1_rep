#
#		Model of each buildings
#
# ------------------------  Number of Storeys ------------------------------------------------------
set NStorytmp 0
	if [catch {open [lindex $ainputFilename $numInFile 0] r} inFileID] {
		puts stderr "Cannot open input file for reading number of storeys"
	} else {
	set flag 1
		foreach line [split [read $inFileID] \n] {
			if {[llength $line] == 0} {
				# Blank line --> do nothing
				continue
			} elseif {$flag == 1} {
				foreach word [split $line] {
					if {[string match $word "#MASTERNODES"] == 1} {
						set flag 0
						break
					}
				}
				if {$flag == 1} {
					foreach word [split $line] {
						if {[string match $word "#FLOOR"] == 1} {
							set NStorytmp [expr $NStorytmp+1];	 # number of stories above ground level
							break
						}
					}
				}
			} else {break}
		}
	lappend NStory $NStorytmp
	close $inFileID
	}


# --------- CREATE MODEL from input files -----------------------------------------------------
	source Transformation_Vectors.tcl;				# for Transformation purposes
	source CreateNodes.tcl;							# Creates nodes
	source CreateElements.tcl;						# Creates elements
	source AssemblefromNodes.tcl; 					# Do some work from the Node info from INPUT file
	source AssemblefromElements.tcl;				# Do some work from the Element info from INPUT file

	
#
# --------------------- FLOOR HEIGHTs ---------------------------------------------------------  
#
  	if [catch {open [lindex $ainputFilename $numInFile 0] r} inFileID] {
		puts stderr "Cannot open input file for reading Floor Heights"
	} else {
	set flag 1
	set floorlevel 0
	set incr 0
	set aFloorHeighttmp "";    # distance between two neighbor floors for each building
 	for {set i 1} {$i <= [lindex $NStory $numInFile]} {incr i 1} {
		lappend aFloorHeighttmp 0
	}
	lappend aFloorHeight $aFloorHeighttmp
	
	set FloorHeighttmp "";    # Distance from each floor to the ground for each building
 	for {set i 1} {$i <= [lindex $NStory $numInFile]} {incr i 1} {
		lappend FloorHeighttmp 0
	}
	lappend FloorHeight $FloorHeighttmp

	foreach line [split [read $inFileID] \n] {
		if {[llength $line] == 0} {
			# Blank line --> do nothing
			continue
		} 
		if {$flag == 1} {
			foreach word [split $line] {
				if {[string match $word "#MASTERNODES"] == 1} {
					set flag 0
					break
				}
				if {[string match $word "#BUILDING"] == 1} {
					break
				}
				if {[string match $word "#GROUND"] == 1} {
					break
				}
				if {[string match $word "#FLOOR"] == 1} {
					set floorlevel [expr $floorlevel+1]
					break
				} else {
					if {$flag == 1} {
						if {$floorlevel > $incr} {
							set list [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
							foreach word [split $list] {
								for {set i 0} {$i <= [expr [llength [lindex $LCol $numInFile]]-1]} {incr i 1} {
									if {[lindex $elidcolumnnodes $numInFile $i 1] == $word || [lindex $elidcolumnnodes $numInFile $i 2] == $word} {
										lset aFloorHeight $numInFile [expr $floorlevel-1] [lindex $LCol $numInFile $i 1];  # assuming all colums same length!!!
										set incr [expr $incr+1]
										break
									}
								}
							break
							}
						}
					}
				}
			}
		}
	}
	close $inFileID
	}
    set FloorHeighttmp 0
	for {set i 1} {$i <= [lindex $NStory $numInFile]} {incr i 1} {
		set FloorHeighttmp [expr $FloorHeighttmp + [lindex $aFloorHeight $numInFile [expr $i-1]]]
		lset FloorHeight $numInFile [expr $i-1] $FloorHeighttmp
	}
	
#
	puts "Number of Stories in Y: $NStorytmp and Number of Frames in each floor: $NFrame"
#
#