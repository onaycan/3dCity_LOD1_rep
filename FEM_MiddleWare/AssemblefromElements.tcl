# define structure-geometry paramters
# ------------------------  BEAM LENGTHs ------------------------------------------------------
    if [catch {open [lindex $ainputFilename $numInFile 0] r} inFileID] {
		puts stderr "Cannot open input file for reading ground fix points"
    } else {
      set flag 0
		set LBeamtmp2 ""
		foreach line [split [read $inFileID] \n] {
			if {[llength $line] == 0} {
				# Blank line --> do nothing
				continue
			} elseif {$flag == 1} {
				foreach word [split $line] {
					if {[string match $word "#GIRDER"] == 1} {
					set flag 0
					break
					}
				}
				if {$flag == 1} {
					set list [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
					
					set LBeamtmp1 ""
					foreach word [split $list] {
						lappend LBeamtmp1 $word
					}
					lappend LBeamtmp2 $LBeamtmp1 
				}
			} else {
				foreach word [split $line] {
					if {[string match $word "#BEAMLENGTH"] == 1} {
						set flag 1
						break
					}
				}
			}
		}
	close $inFileID
	}
	lappend LBeam $LBeamtmp2;	# beam length (parallel to X axis)
  
# ------------------------  GIRDER LENGTHs ------------------------------------------------------
    if [catch {open [lindex $ainputFilename $numInFile 0] r} inFileID] {
		puts stderr "Cannot open input file for reading ground fix points"
    } else {
      set flag 0
		set LGirdtmp2 ""
		foreach line [split [read $inFileID] \n] {
			if {[llength $line] == 0} {
				# Blank line --> do nothing
				continue
			} elseif {$flag == 1} {
				foreach word [split $line] {
					if {[string match $word "#COLUMN"] == 1} {
					set flag 0
					break
					}
				}
				if {$flag == 1} {
					set list [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]

					set LGirdtmp1 ""
					foreach word [split $list] {
						lappend LGirdtmp1 $word
					}
					lappend LGirdtmp2 $LGirdtmp1 
				}
			} else {
				foreach word [split $line] {
					if {[string match $word "#GIRDERLENGTH"] == 1} {
						set flag 1
						break
					}
				}
			}
		}
	close $inFileID
	}
	lappend LGird $LGirdtmp2;	# girder length (parallel to Z axis) 

	
# ------------------------  COLUMN LENGTHs ------------------------------------------------------
    if [catch {open [lindex $ainputFilename $numInFile 0] r} inFileID] {
		puts stderr "Cannot open input file for reading ground fix points"
    } else {
      set flag 0
	  set LColtmp2 ""
		foreach line [split [read $inFileID] \n] {
			if {[llength $line] == 0} {
				# Blank line --> do nothing
				continue
			} elseif {$flag == 1} {
				foreach word [split $line] {
					if {[string match $word "#END"] == 1} {
					set flag 0
					break
					}
				}
				if {$flag == 1} {
					set list [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
					set LColtmp1 ""
					foreach word [split $list] {
						lappend LColtmp1 $word
					}
					lappend LColtmp2 $LColtmp1
				}
			} else {
				foreach word [split $line] {
					if {[string match $word "#COLUMNLENGTH"] == 1} {
						set flag 1
						break
					}
				}
			}
		}
	close $inFileID
	}
	lappend LCol $LColtmp2;  # column height (parallel to Y axis)

# ----- Element IDs for Gravity Loads or other purposes  -------------------------------------------------------
# ------------------------- CREATE Column IDs with connectivity nodes ---------------------------------------------------

   if [catch {open [lindex $ainputFilename $numInFile 0] r} inFileID] {
      puts stderr "Cannot open input file for reading column elements IDs with its connectivity"
   } else {
      set flag 0
	  set elidcolumnnodestmp ""
      foreach line [split [read $inFileID] \n] {
         if {[llength $line] == 0} {
            # Blank line --> do nothing
            continue
         } elseif {$flag == 1} {
		    foreach word [split $line] {
			   if {[string match $word "#COLUMNLENGTH"] == 1} {set flag 0}
            }
			if {$flag == 1} {
				set elemID [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
				lappend elidcolumnnodestmp $elemID
			}
         } else {
            foreach word [split $line] {
               if {$flag == 1} {
                  break
               }
               if {[string match $word "#COLUMN"] == 1} {set flag 1}
            }
         }
      }
      close $inFileID
   }
   lappend elidcolumnnodes $elidcolumnnodestmp
	
# beams -- parallel to X-axis
# -----------------------   CREATE BEAM IDs  -------------------------------------------------
   if [catch {open [lindex $ainputFilename $numInFile 0] r} inFileID] {
      puts stderr "Cannot open input file for reading beam elements IDs with its connectivity"
   } else {
      set flag 0
	  set elidbeamnodestmp ""
      foreach line [split [read $inFileID] \n] {
         if {[llength $line] == 0} {
            # Blank line --> do nothing
            continue
         } elseif {$flag == 1} {
		    foreach word [split $line] {
			   if {[string match $word "#BEAMLENGTH"] == 1} {set flag 0}
            }
			if {$flag == 1} {
				set elemID [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
				lappend elidbeamnodestmp $elemID
			}
         } else {
            foreach word [split $line] {
               if {$flag == 1} {
                  break
               }
               if {[string match $word "#BEAM"] == 1} {set flag 1}
            }
         }
      }
      close $inFileID
   }
   lappend elidbeamnodes $elidbeamnodestmp

# girders -- parallel to Y-axis
# ----------------------  CREATE Gird IDs  ------------------------------------------------------
   if [catch {open [lindex $ainputFilename $numInFile 0] r} inFileID] {
      puts stderr "Cannot open input file for reading girder elements IDs with its connectivity"
   } else {
      set flag 0
	  set elidgirdnodestmp ""
      foreach line [split [read $inFileID] \n] {
         if {[llength $line] == 0} {
            # Blank line --> do nothing
            continue
         } elseif {$flag == 1} {
		    foreach word [split $line] {
			   if {[string match $word "#GIRDERLENGTH"] == 1} {set flag 0}
            }
			if {$flag == 1} {
				set elemID [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
				lappend elidgirdnodestmp $elemID
			}
         } else {
            foreach word [split $line] {
               if {$flag == 1} {
                  break
               }
               if {[string match $word "#GIRDER"] == 1} {set flag 1}
            }
         }
      }
      close $inFileID
   }
   lappend elidgirdnodes $elidgirdnodestmp