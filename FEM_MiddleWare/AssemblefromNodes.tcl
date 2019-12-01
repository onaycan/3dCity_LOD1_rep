#
#
# Script for calculating:
# 	Node lists for floors, Special Node lists for outputting (for instance "Free Node ID")
# 	
#	by: Serhat Adilak, 2019
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
#
#