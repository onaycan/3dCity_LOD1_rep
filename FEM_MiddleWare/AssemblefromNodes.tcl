# ------------------------  Boundary ------------------------------------------------------
# determine support nodes where ground motions are input, for multiple-support excitation
    if [catch {open [lindex $ainputFilename $numInFile 0] r} inFileID] {
		puts stderr "Cannot open input file for reading ground fix points"
    } else {
      set flag 0
	  set iSupportNodetmp ""
		foreach line [split [read $inFileID] \n] {
			if {[llength $line] == 0} {
				# Blank line --> do nothing
				continue
			} elseif {$flag == 1} {
				foreach word [split $line] {
					if {[string match $word "#FLOOR"] == 1} {
					set flag 0
					break
					}
				}
				if {$flag == 1} {
					set list [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
					foreach word [split $list] {
						# BOUNDARY CONDITIONS
						fix $word 1 1 1 0 1 0;		# pin all Ground Floor nodes
						lappend iSupportNodetmp $word
						break
					}
				}
			} else {
				foreach word [split $line] {
					if {[string match $word "#GROUND"] == 1} {
						set flag 1
						break
					}
				}
			}
		}
	close $inFileID
	}
	lappend iSupportNode $iSupportNodetmp
	

# ----------------------MASTERNODES IDS ------------------------------------------------------

    if [catch {open [lindex $ainputFilename $numInFile 0] r} inFileID] {
      puts stderr "Cannot open input file for reading constrain dofs rather than rigid diaphragm"
    } else {
      set flag 0
	  set iMasterNodetmp ""
      foreach line [split [read $inFileID] \n] {
         if {[llength $line] == 0} {
            # Blank line --> do nothing
            continue
         } elseif {$flag == 1} {
		    foreach word [split $line] {
			   if {[string match $word "#BEAM"] == 1} {set flag 0}
            }
			if {$flag == 1} {
				set list [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
				foreach MasterNodeID [split $list] {
					fix $MasterNodeID 0  1  0  1  0  1;		# constrain other dofs that don't belong to rigid diaphragm control
					lappend iMasterNodetmp $MasterNodeID
					break
				}
			}
         } else {
            foreach word [split $line] {
               if {$flag == 1} {
                  break
               }
               if {[string match $word "#MASTERNODES"] == 1} {set flag 1}
            }
         }
      }
      close $inFileID
   }
  lappend iMasterNode $iMasterNodetmp

# ------------------------ Floor Node IDs  ------------------------------------------------------
if [catch {open [lindex $ainputFilename $numInFile 0] r} inFileID] {
	puts stderr "Cannot open input file for reading nodal weights"
} else {
  set flag 1
	set floorcounter 0
	set nodecounttmp 0
	set floornodes ""
	set nodecount ""
	foreach line [split [read $inFileID] \n] {
		if {[llength $line] == 0} {
			# Blank line --> do nothing
			continue
		} 
		if {$flag == 1} {
			foreach word [split $line] {
				if {[string match $word "#BUILDING"] == 1} {
					break
				}
				if {[string match $word "#GROUND"] == 1} {
					set flag2 1
					break
				}
				if {[string match $word "#FLOOR"] == 1 || [string match $word "#MASTERNODES"] == 1} {
					set flag2 0
					if {$floorcounter>0} {
						lappend floornodes $ifloornodestmp
						lappend nodecount $nodecounttmp
						set ifloornodestmp ""
						set nodecounttmp 0
					}
					set floorcounter [expr $floorcounter+1]
					
					if {[string match $word "#MASTERNODES"] == 1} {
						set flag2 1
					} 
					break
				} else {
				  if {$flag2 == 0} {
					set list [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
					foreach word [split $list] {
						lappend ifloornodestmp $list
						set nodecounttmp [expr $nodecounttmp+1]
						break
					}
					break
				  }
				}
			}; #end of split line 
		}
	}; #end of line read 
	close $inFileID
	}
	lappend ifloornodes $floornodes
	
# ------------------------  Free Node ID for OUTPUT ---------- Better to take a node defined??????  Take all nodes
	if [catch {open [lindex $ainputFilename $numInFile 0] r} inFileID] {
		puts stderr "Cannot open input file for reading free node ID"
	} else {
	set flag 1
	set FreeNodeIDtmp ""
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
				if {[string match $word "#GROUND"] == 1 || [string match $word "#FLOOR"] == 1} {
					break
				} else {
					set list [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
					foreach word [split $list] {
					set FreeNodeIDtmp $word;	# ID: free node  to output results	
					break
					}
				}
			}
		}
	}
	close $inFileID
	}
	lappend FreeNodeID $FreeNodeIDtmp

# ------------------------------  Exterior Node IDs ----------------------------------------
set exteriorGirdernodesID ""
set exteriornodesID ""
set exteriorGirdernodesID ""
set exteriorBeamnodesID ""	
set aNBayZ ""
set aNFrame ""
for {set k 0} {$k <= [expr [lindex $NStory $numInFile]-1]} {incr k 1} {
	set maxX 0.0
	set maxZ 0.0
	set exteriornodestmp2 ""
	set exteriornodesIDtmp ""
	set exteriorGirdernodesIDtmp ""
	set exteriorBeamnodesIDtmp ""
	lappend exteriornodestmp2 [lindex $ifloornodes $numInFile $k]
	for {set i 0} {$i <= [expr [lindex $nodecount $k]-1]} {incr i 1} {
		if {$maxX <= [lindex $exteriornodestmp2 $numInFile $i 1]} {
			set maxX [lindex $exteriornodestmp2 $numInFile $i 1]
		}
		if {$maxZ <= [lindex $exteriornodestmp2 $numInFile $i 3]} {
			set maxZ [lindex $exteriornodestmp2 $numInFile $i 3]
		}		
	}
	set minX [lindex $exteriornodestmp2 $numInFile 0 1]
	set minZ [lindex $exteriornodestmp2 $numInFile 0 3]
	for {set i 0} {$i <= [expr [lindex $nodecount $k]-1]} {incr i 1} {
		if {$minX > [lindex $exteriornodestmp2 $numInFile $i 1]} {
			set minX [lindex $exteriornodestmp2 $numInFile $i 1]
		}
		if {$minZ > [lindex $exteriornodestmp2 $numInFile $i 3]} {
			set minZ [lindex $exteriornodestmp2 $numInFile $i 3]
		}		
	}
	for {set i 0} {$i <= [expr [lindex $nodecount $k]-1]} {incr i 1} {
		if {$minX == [lindex $exteriornodestmp2 $numInFile $i 1]} {
			lappend exteriornodesIDtmp [lindex $exteriornodestmp2 $numInFile $i 0]
			lappend exteriorGirdernodesIDtmp [lindex $exteriornodestmp2 $numInFile $i 0]
		}
		if {$maxX == [lindex $exteriornodestmp2 $numInFile $i 1]} {
			lappend exteriornodesIDtmp [lindex $exteriornodestmp2 $numInFile $i 0]
			lappend exteriorGirdernodesIDtmp [lindex $exteriornodestmp2 $numInFile $i 0]
		}
		if {$minZ == [lindex $exteriornodestmp2 $numInFile $i 3]} {
			if {$minX != [lindex $exteriornodestmp2 $numInFile $i 1] && $maxX != [lindex $exteriornodestmp2 $numInFile $i 1]} {
				lappend exteriornodesIDtmp [lindex $exteriornodestmp2 $numInFile $i 0]
			}
			lappend exteriorBeamnodesIDtmp [lindex $exteriornodestmp2 $numInFile $i 0]
		}
		if {$maxZ == [lindex $exteriornodestmp2 $numInFile $i 3]} {
			if {$minX != [lindex $exteriornodestmp2 $numInFile $i 1] && $maxX != [lindex $exteriornodestmp2 $numInFile $i 1]} {
				lappend exteriornodesIDtmp [lindex $exteriornodestmp2 $numInFile $i 0]
			}
			lappend exteriorBeamnodesIDtmp [lindex $exteriornodestmp2 $numInFile $i 0]
		}
	}
	lappend exteriornodesID $exteriornodesIDtmp
	lappend exteriorGirdernodesID $exteriorGirdernodesIDtmp
	lappend exteriorBeamnodesID $exteriorBeamnodesIDtmp	
	lappend aNBayZ [expr [llength [lindex $exteriorGirdernodesID $k]]/2-1]
	lappend aNFrame [expr [llength [lindex $exteriorGirdernodesID $k]]/2]
}
	lappend iexteriornodesID $exteriornodesID; # outermost nodes per floor each building
	lappend iexteriorGirdernodesID $exteriorGirdernodesID
	lappend iexteriorBeamnodesID $exteriorBeamnodesID
	lappend NBayZ $aNBayZ; #NBAYZ		# number of bays in Z direction
	lappend NFrame $aNFrame;	# actually deal with frames in Z direction, as this is an easy extension of the 2d model
#
# ------------------------  rigidDiaphragm ------------------------------------------------------	
for {set k 0} {$k <= [expr [lindex $NStory $numInFile]-1]} {incr k 1} {
	for {set i 0} {$i <= [expr [llength [lindex $ifloornodes $numInFile $k]]-1]} {incr i 1} {
		rigidDiaphragm 2 [lindex $iMasterNode $numInFile $k] [lindex $ifloornodes $numInFile $k $i 0]
	}
}
#
#