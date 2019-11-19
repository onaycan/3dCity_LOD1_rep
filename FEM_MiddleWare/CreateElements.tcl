#
#	CREATE ELEMENTS
#
    if [catch {open [lindex $ainputFilename $numInFile 0] r} inFileID] {
		puts stderr "Cannot open input file for reading ground fix points"
    } else {
      set flag 0
		foreach line [split [read $inFileID] \n] {
			if {[llength $line] == 0} {
				# Blank line --> do nothing
				continue
			} elseif {$flag == 1} {
				foreach word [split $line] {
					if {[string match $word "#BEAMLENGTH"] == 1} {
					set flag 0
					break
					}
				}
				if {$flag == 1} {
					set list [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
					set tags ""
					foreach tagstmp [split $list] {
						lappend tags $tagstmp
					}
					set elemID [lindex $tags 0]
					set nodeI [lindex $tags 1]
					set nodeJ [lindex $tags 2]
					element nonlinearBeamColumn $elemID $nodeI $nodeJ $numIntgrPts $BeamSecTag $elemID;	# beams
				}
			} else {
				foreach word [split $line] {
					if {[string match $word "#BEAM"] == 1} {
						set flag 1
						break
					}
				}
			}
		}
	close $inFileID
	}
	
   if [catch {open [lindex $ainputFilename $numInFile 0] r} inFileID] {
		puts stderr "Cannot open input file for reading ground fix points"
    } else {
      set flag 0
		foreach line [split [read $inFileID] \n] {
			if {[llength $line] == 0} {
				# Blank line --> do nothing
				continue
			} elseif {$flag == 1} {
				foreach word [split $line] {
					if {[string match $word "#GIRDERLENGTH"] == 1} {
					set flag 0
					break
					}
				}
				if {$flag == 1} {
					set list [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
					set tags ""
					foreach tagstmp [split $list] {
						lappend tags $tagstmp
					}
					set elemID [lindex $tags 0]
					set nodeI [lindex $tags 1]
					set nodeJ [lindex $tags 2]
					element nonlinearBeamColumn $elemID $nodeI $nodeJ $numIntgrPts $GirdSecTag $elemID;		# Girds
				}
			} else {
				foreach word [split $line] {
					if {[string match $word "#GIRDER"] == 1} {
						set flag 1
						break
					}
				}
			}
		}
	close $inFileID
	}

   if [catch {open [lindex $ainputFilename $numInFile 0] r} inFileID] {
		puts stderr "Cannot open input file for reading ground fix points"
    } else {
      set flag 0
		foreach line [split [read $inFileID] \n] {
			if {[llength $line] == 0} {
				# Blank line --> do nothing
				continue
			} elseif {$flag == 1} {
				foreach word [split $line] {
					if {[string match $word "#COLUMNLENGTH"] == 1} {
					set flag 0
					break
					}
				}
				if {$flag == 1} {
					set list [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
					set tags ""
					foreach tagstmp [split $list] {
						lappend tags $tagstmp
					}
					set elemID [lindex $tags 0]
					set nodeI [lindex $tags 1]
					set nodeJ [lindex $tags 2]
					element nonlinearBeamColumn $elemID $nodeI $nodeJ $numIntgrPts $ColSecTag $elemID;		# columns
				}
			} else {
				foreach word [split $line] {
					if {[string match $word "#COLUMN"] == 1} {
						set flag 1
						break
					}
				}
			}
		}
	close $inFileID
	}
	


