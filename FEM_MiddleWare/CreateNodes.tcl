#
#	CREATE NODES
#

if [catch {open [lindex $ainputFilename $numInFile 0] r} inFileID] {
		puts stderr "Cannot open input file for reading ground fix points"
    } else {
      set flag 1
		foreach line [split [read $inFileID] \n] {
			if {[llength $line] == 0} {
				# Blank line --> do nothing
				continue
			} 
			if {$flag == 1} {
				foreach word [split $line] {
					if {[string match $word "#BEAM"] == 1} {
					set flag 0
					break
					}
				}
				if {$flag == 1} {
					foreach word [split $line] {
						if {[string match $word "node"] == 1} {
							set list [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
							set tags ""
							foreach tagstmp [split $list] {
								lappend tags $tagstmp
							}
							set nodeID [lindex $tags 0]
							set X [lindex $tags 1]
							set Y [lindex $tags 2]
							set Z [lindex $tags 3]
							node $nodeID $X $Y $Z;		# actually define node
						}		
						break
					}
				}
			}
		}
	}
	close $inFileID

# ------------------------  Boundary NODES ------------------------------------------------------
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
	
