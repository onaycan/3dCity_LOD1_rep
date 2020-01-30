#
#		CREATE THE BUILDING MODELs
#	Element, Nodes and many other definitions:
#	Properties of the building (height, BiD, number of Storeys, elt's-nodes @each floor
#
# ------------------------  Building ID's  ------------------------------------------------------
	if [catch {open [lindex $ainputFilename $numInFile 0] r} inFileID] {
		puts stderr "Cannot open input file for reading number of storeys"
	} else {
		foreach line [split [read $inFileID] \n] {
			if {[llength $line] == 0} {
				# Blank line --> do nothing
				continue
			} else {
				foreach word [split $line] {
					if {[string match $word "#BUILDING"] == 1} {
						set bidtmp [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
						lappend BID $bidtmp
						break
					}
				}
			break
			}
		}
	close $inFileID
	}

# ---------------------------------------------------------------------------------------------
	set tclfilename "/"
	append tclfilename "CreateElements.tcl";						# Creates elements
	set tclfile2source ""
	append tclfile2source $tclfilesdir $tclfilename
	source $tclfile2source
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
									if {[lindex $iColumnConnect $numInFile $i 1] == $word || [lindex $iColumnConnect $numInFile $i 2] == $word} {
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
#
#