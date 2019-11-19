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

	
