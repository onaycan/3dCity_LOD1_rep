#
#
# Script for:
# 	Node lists for floors, Special Node lists for outputting (for instance "Free Node ID") etc
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
# --------- Take all Node ID's with their coordinates from INPUT FILE ---------						
   if [catch {open [lindex $ainputFilename $numInFile 0] r} inFileID] {
      puts stderr "Cannot open input file"
   } else {
      set flag 0
	  set NodeList ""
      foreach line [split [read $inFileID] \n] {
         if {[llength $line] == 0} {
            # Blank line --> do nothing
            continue
         } elseif {$flag == 1} {
		    foreach word [split $line] {
			   if {[string match $word "#MASTERNODES"] == 1} {set flag 0}
            }
			if {$flag == 1} {
				foreach word [split $line] {
					if {[string match $word "node"] == 1} {
						set list [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
						set NodeListtmp ""
						foreach NodeListtmp2 [split $list] {
							lappend NodeListtmp $NodeListtmp2
						}
						lappend NodeList $NodeListtmp
					}
				}
			}
         } else {
            foreach word [split $line] {
               if {$flag == 1} {
                  break
               }
               if {[string match $word "#GROUND"] == 1} {set flag 1}
            }
         }
	  }
      close $inFileID
   }
lappend iNodeList $NodeList

for {set i 0} {$i <= [expr [llength [lindex $iNodeList $numInFile]]-1]} {incr i 1} {
	set nodeID [lindex $iNodeList $numInFile $i 0]
	lappend nodeIDcheckList $nodeID
	if {$numInFile > 0 } {
		set idx [lsearch -all $nodeIDcheckList $nodeID]
		if {[llength $idx]>1} {
			set idx [lindex $idx [expr [llength $idx]-1]]
			set nodeIDcheckList [lreplace $nodeIDcheckList $idx $idx]; # same IDs from other buildings will be removed
		}
	} 
}

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
#
for {set i 0} {$i <= [expr [llength [lindex $ifloornodes $numInFile]]-1]} {incr i 1} {
	for {set j 0} {$j <= [expr [llength [lindex $ifloornodes $numInFile $i]]-1]} {incr j 1} {
		set nodeID [lindex $ifloornodes $numInFile $i $j 0]
		lappend floornodeIDcheckList $nodeID
	}
}
#
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
#
# 
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
	lappend iSupportNode $iSupportNodetmp; # SUPPORT NODE IDS
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
				set MasterNodetags ""
				foreach word [split $list] {
					lappend MasterNodetags $word
				}
				set nodeID [lindex $MasterNodetags 0]	
				set X [lindex $MasterNodetags 1]
				set Y [lindex $MasterNodetags 2]
				set Z [lindex $MasterNodetags 3]
				
				node $nodeID $X $Y $Z;	# actually define node
				fix $nodeID 0  1  0  1  0  1;		# constrain other dofs that don't belong to rigid diaphragm control
				lappend iMasterNodetmp $nodeID
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
#
#	
