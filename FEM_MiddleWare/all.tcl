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
proc BuildRCrectSection {id HSec BSec coverH coverB coreID coverID steelID numBarsTop barAreaTop numBarsBot barAreaBot numBarsIntTot barAreaInt nfCoreY nfCoreZ nfCoverY nfCoverZ} {
	################################################
	# BuildRCrectSection $id $HSec $BSec $coverH $coverB $coreID $coverID $steelID $numBarsTop $barAreaTop $numBarsBot $barAreaBot $numBarsIntTot $barAreaInt $nfCoreY $nfCoreZ $nfCoverY $nfCoverZ
	################################################
	# Build fiber rectangular RC section, 1 steel layer top, 1 bot, 1 skin, confined core
	# Define a procedure which generates a rectangular reinforced concrete section
	# with one layer of steel at the top & bottom, skin reinforcement and a 
	# confined core.
	#		by: Silvia Mazzoni, 2006
	#			adapted from Michael H. Scott, 2003
	# 
	# Formal arguments
	#    id - tag for the section that is generated by this procedure
	#    HSec - depth of section, along local-y axis
	#    BSec - width of section, along local-z axis
	#    cH - distance from section boundary to neutral axis of reinforcement
	#    cB - distance from section boundary to side of reinforcement
	#    coreID - material tag for the core patch
	#    coverID - material tag for the cover patches
	#    steelID - material tag for the reinforcing steel
	#    numBarsTop - number of reinforcing bars in the top layer
	#    numBarsBot - number of reinforcing bars in the bottom layer
	#    numBarsIntTot - TOTAL number of reinforcing bars on the intermediate layers, symmetric about z axis and 2 bars per layer-- needs to be an even integer
	#    barAreaTop - cross-sectional area of each reinforcing bar in top layer
	#    barAreaBot - cross-sectional area of each reinforcing bar in bottom layer
	#    barAreaInt - cross-sectional area of each reinforcing bar in intermediate layer 
	#    nfCoreY - number of fibers in the core patch in the y direction
	#    nfCoreZ - number of fibers in the core patch in the z direction
	#    nfCoverY - number of fibers in the cover patches with long sides in the y direction
	#    nfCoverZ - number of fibers in the cover patches with long sides in the z direction
	#    
	#                        y
	#                        ^
	#                        |     
	#             ---------------------    --   --
	#             |   o     o     o    |     |    -- coverH
	#             |                      |     |
	#             |   o            o    |     |
	#    z <--- |          +          |     HSec
	#             |   o            o    |     |
	#             |                      |     |
	#             |   o o o o o o    |     |    -- coverH
	#             ---------------------    --   --
	#             |-------Bsec------|
	#             |---| coverB  |---|
	#
	#                       y
	#                       ^
	#                       |    
	#             ---------------------
	#             |\      cover        /|
	#             | \------Top------/ |
	#             |c|                   |c|
	#             |o|                   |o|
	#  z <-----|v|       core      |v|  HSec
	#             |e|                   |e|
	#             |r|                    |r|
	#             | /-------Bot------\ |
	#             |/      cover        \|
	#             ---------------------
	#                       Bsec
	#    
	#
	# Notes
	#    The core concrete ends at the NA of the reinforcement
	#    The center of the section is at (0,0) in the local axis system
	# 
	set coverY [expr $HSec/2.0];		# The distance from the section z-axis to the edge of the cover concrete -- outer edge of cover concrete
	set coverZ [expr $BSec/2.0];		# The distance from the section y-axis to the edge of the cover concrete -- outer edge of cover concrete
	set coreY [expr $coverY-$coverH];		# The distance from the section z-axis to the edge of the core concrete --  edge of the core concrete/inner edge of cover concrete
	set coreZ [expr $coverZ-$coverB];		# The distance from the section y-axis to the edge of the core concrete --  edge of the core concrete/inner edge of cover concrete
	set numBarsInt [expr $numBarsIntTot/2];	# number of intermediate bars per side

	# Define the fiber section
	section fiberSec $id {
		# Define the core patch
		patch quadr $coreID $nfCoreZ $nfCoreY -$coreY $coreZ -$coreY -$coreZ $coreY -$coreZ $coreY $coreZ
	   
		# Define the four cover patches
		patch quadr $coverID 2 $nfCoverY -$coverY $coverZ -$coreY $coreZ $coreY $coreZ $coverY $coverZ
		patch quadr $coverID 2 $nfCoverY -$coreY -$coreZ -$coverY -$coverZ $coverY -$coverZ $coreY -$coreZ
		patch quadr $coverID $nfCoverZ 2 -$coverY $coverZ -$coverY -$coverZ -$coreY -$coreZ -$coreY $coreZ
		patch quadr $coverID $nfCoverZ 2 $coreY $coreZ $coreY -$coreZ $coverY -$coverZ $coverY $coverZ	

		# define reinforcing layers
		layer straight $steelID $numBarsInt $barAreaInt  -$coreY $coreZ $coreY $coreZ;	# intermediate skin reinf. +z
		layer straight $steelID $numBarsInt $barAreaInt  -$coreY -$coreZ $coreY -$coreZ;	# intermediate skin reinf. -z
		layer straight $steelID $numBarsTop $barAreaTop $coreY $coreZ $coreY -$coreZ;	# top layer reinfocement
		layer straight $steelID $numBarsBot $barAreaBot  -$coreY $coreZ  -$coreY -$coreZ;	# bottom layer reinforcement

	};	# end of fibersection definition
};		# end of procedure

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

	
proc DisplayModel3D { {ShapeType nill} {dAmp 5}  {xLoc 0} {yLoc 0} {xPixels 0} {yPixels 0} {nEigen 1} } {
	######################################################################################
	## DisplayModel3D $ShapeType $dAmp $xLoc $yLoc $xPixels $yPixels $nEigen
	######################################################################################
	## display Node Numbers, Deformed or Mode Shape in all 3 planes
	##			Silvia Mazzoni & Frank McKenna, 2006
	##
	## 	ShapeType : 	type of shape to display. # options: ModeShape , NodeNumbers , DeformedShape 
	## 	dAmp : 		relative amplification factor for deformations
	## 	xLoc,yLoc  : 	horizontal & vertical location in pixels of graphical window (0,0=upper left-most corner)
	## 	xPixels,yPixels :	width & height of graphical window in pixels
	## 	nEigen : 		if nEigen not=0, show mode shape for nEigen eigenvalue
	##	
	#######################################################################################
	global TunitTXT ;					# load global unit variable
	global ScreenResolutionX ScreenResolutionY;	# read global values for screen resolution

	if {  [info exists TunitTXT] != 1} {set TunitTXT ""};		# set blank if it has not been defined previously.

	if {  [info exists ScreenResolutionX] != 1} {set ScreenResolutionX 1024};		# set default if it has not been defined previously.
	if {  [info exists ScreenResolutionY] != 1} {set ScreenResolutionY 1068};		# set default if it has not been defined previously.

	if {$xPixels == 0} {
		set xPixels [expr int($ScreenResolutionX/1)];		
		set yPixels [expr int($ScreenResolutionY/1)]
		set xLoc 0
		set yLoc -350
	}
	if {$ShapeType == "nill"} {
		puts ""; puts ""; puts "------------------"
		puts "View the Model? (N)odes, (D)eformedShape, anyMode(1),(2),(#). Press enter for NO."
		gets stdin answer
		if {[llength $answer]>0 } { 
			if {$answer != "N" & $answer != "n"} {
				puts "Modify View Scaling Factor=$dAmp? Type factor, or press enter for NO."
				gets stdin answerdAmp
				if {[llength $answerdAmp]>0 } { 
					set dAmp $answerdAmp
				}
			}
			if {[string index $answer 0] == "N" || [string index $answer 0] == "n"} {
				set ShapeType NodeNumbers
			} elseif {[string index $answer 0] == "D" ||[string index $answer 0] == "d" } {
				set ShapeType DeformedShape
			} else {
				set ShapeType ModeShape
				set nEigen $answer
			}
		} else {
			return
		}
	}

	if {$ShapeType ==  "ModeShape" } {
		set lambdaN [eigen $nEigen];		# perform eigenvalue analysis for ModeShape
		set lambda [lindex $lambdaN [expr $nEigen-1]];
		set omega [expr pow($lambda,0.5)]
		set PI 	[expr 2*asin(1.0)];		# define constant
		set Tperiod [expr 2*$PI/$omega];	   	# period
		set fmt1 "Mode Shape, Mode=%.1i Period=%.3f %s  "
		set windowTitle [format $fmt1 $nEigen $Tperiod $TunitTXT ]
	} elseif  {$ShapeType ==  "NodeNumbers" } {
		set windowTitle "Node Numbers"
	} elseif  {$ShapeType ==  "DeformedShape" } {
		set windowTitle0 "Deformed Shape "
	}

	if {$ShapeType ==  "DeformedShape" } {
		set xPixels [expr int($xPixels/2)]
		set yPixels [expr int($yPixels/2)]
		set xLoc1 [expr $xLoc+$xPixels]
		set yLoc1 [expr $yLoc+$yPixels]
		set planeTXT "-Plane"

#		set viewPlane XY
#		set windowTitle $windowTitle0$viewPlane$planeTXT
#		recorder display $windowTitle $xLoc1 $yLoc $xPixels $yPixels  -wipe ; # display recorder
#		DisplayPlane $ShapeType $dAmp $viewPlane 
#		set viewPlane ZY
#		set windowTitle $windowTitle0$viewPlane$planeTXT
#		recorder display $windowTitle $xLoc $yLoc $xPixels $yPixels  -wipe ; # display recorder
#		DisplayPlane $ShapeType $dAmp $viewPlane 
		set viewPlane ZX
		set windowTitle $windowTitle0$viewPlane$planeTXT
		recorder display $windowTitle $xLoc $yLoc1 $xPixels $yPixels  -wipe ; # display recorder
		DisplayPlane $ShapeType $dAmp $viewPlane 
		set viewPlane 3D
		set windowTitle $windowTitle0$viewPlane
		recorder display $windowTitle $xLoc1 $yLoc1 $xPixels $yPixels  -wipe ; # display recorder
		DisplayPlane $ShapeType $dAmp $viewPlane 
	} else {
		recorder display $windowTitle $xLoc $yLoc $xPixels $yPixels -nowipe; # display recorder
		set viewPlane XY
		DisplayPlane $ShapeType $dAmp $viewPlane $nEigen 1
		set viewPlane ZY
		DisplayPlane $ShapeType $dAmp $viewPlane $nEigen 2
		set viewPlane ZX
		DisplayPlane $ShapeType $dAmp $viewPlane $nEigen 3
		set viewPlane 3D
		DisplayPlane $ShapeType $dAmp $viewPlane $nEigen 4
	}
}

proc DisplayPlane {ShapeType dAmp viewPlane {nEigen 0}  {quadrant 0}} {
	######################################################################################
	## DisplayPlane $ShapeType $dAmp $viewPlane $nEigen $quadrant
	######################################################################################
	## setup display parameters for specified viewPlane and display
	## 			Silvia Mazzoni & Frank McKenna, 2006
	##
	## 	ShapeType : 	type of shape to display. # options: ModeShape , NodeNumbers , DeformedShape 
	## 	dAmp : 		relative amplification factor for deformations
	## 	viewPlane :	set local xy axes in global coordinates (XY,YX,XZ,ZX,YZ,ZY)
	## 	nEigen : 		if nEigen not=0, show mode shape for nEigen eigenvalue
	##	quadrant:		quadrant where to show this figure (0=full figure)
	##	
	######################################################################################

	set Xmin [lindex [nodeBounds] 0];	# view bounds in global coords -  will add padding on the sides
	set Ymin [lindex [nodeBounds] 1];
	set Zmin [lindex [nodeBounds] 2];
	set Xmax [lindex [nodeBounds] 3];
	set Ymax [lindex [nodeBounds] 4];
	set Zmax [lindex [nodeBounds] 5];

	set Xo 0;	# center of local viewing system
	set Yo 0;
	set Zo 0;

	set uLocal [string index $viewPlane 0];	# viewPlane local-x axis in global coordinates
	set vLocal [string index $viewPlane 1];	# viewPlane local-y axis in global coordinates


	if  {$viewPlane =="3D" } {
		set uMin $Zmin+$Xmin
		set uMax $Zmax+$Xmax
		set vMin $Ymin
		set vMax $Ymax
		set wMin -10000
		set wMax 10000
		vup 0 1 0; # dirn defining up direction of view plane
	} else {
		set keyAxisMin "X $Xmin Y $Ymin Z $Zmin"
		set keyAxisMax "X $Xmax Y $Ymax Z $Zmax"
		set axisU [string index $viewPlane 0];
		set axisV [string index $viewPlane 1];
		set uMin [string map $keyAxisMin $axisU]
		set uMax [string map $keyAxisMax $axisU]
		set vMin [string map $keyAxisMin $axisV]
		set vMax [string map $keyAxisMax $axisV]
		if {$viewPlane =="YZ" || $viewPlane =="ZY" } {
			set wMin $Xmin
			set wMax $Xmax
		} elseif  {$viewPlane =="XY" || $viewPlane =="YX" } {
			set wMin $Zmin
			set wMax $Zmax
		} elseif  {$viewPlane =="XZ" || $viewPlane =="ZX" } {
			set wMin $Ymin
			set wMax $Ymax
		} else {
		return -1
		}
	}

	set epsilon 1e-3;	# make windows width or height not zero when the Max and Min values of a coordinate are the same

	set uWide [expr $uMax - $uMin+$epsilon];
	set vWide [expr $vMax - $vMin+$epsilon];
	set uSide [expr 0.25*$uWide];
	set vSide [expr 0.25*$vWide];
	set uMin [expr $uMin - $uSide];
	set uMax [expr $uMax + $uSide];
	set vMin [expr $vMin - $vSide];
	set vMax [expr $vMax + 2*$vSide];	# pad a little more on top, because of window title
	set uWide [expr $uMax - $uMin+$epsilon];
	set vWide [expr $vMax - $vMin+$epsilon];
	set uMid [expr ($uMin+$uMax)/2];
	set vMid [expr ($vMin+$vMax)/2];

	# keep the following general, as change the X and Y and Z for each view plane
	# next three commmands define viewing system, all values in global coords
	vrp $Xo $Yo $Zo;    # point on the view plane in global coord, center of local viewing system
	if {$vLocal == "X"} {
		vup 1 0 0; # dirn defining up direction of view plane
	} elseif {$vLocal == "Y"} {
		vup 0 1 0; # dirn defining up direction of view plane
	} elseif {$vLocal == "Z"} {
		vup 0 0 1; # dirn defining up direction of view plane
	}
	if {$viewPlane =="YZ" } {
		vpn 1 0 0; # direction of outward normal to view plane
		prp 10000. $uMid $vMid ; # eye location in local coord sys defined by viewing system
		plane 10000 -10000; # distance to front and back clipping planes from eye
	} elseif  {$viewPlane =="ZY" } {
		vpn -1 0 0; # direction of outward normal to view plane
		prp -10000. $vMid $uMid ; # eye location in local coord sys defined by viewing system
		plane 10000 -10000; # distance to front and back clipping planes from eye
	} elseif  {$viewPlane =="XY"  } {
		vpn 0 0 1; # direction of outward normal to view plane
		prp $uMid $vMid 10000; # eye location in local coord sys defined by viewing system
		plane 10000 -10000; # distance to front and back clipping planes from eye
	} elseif  {$viewPlane =="YX" } {
		vpn 0 0 -1; # direction of outward normal to view plane
		prp $uMid $vMid -10000; # eye location in local coord sys defined by viewing system
		plane 10000 -10000; # distance to front and back clipping planes from eye
	} elseif  {$viewPlane =="XZ" } {
		vpn 0 -1 0; # direction of outward normal to view plane
		prp $uMid -10000 $vMid ; # eye location in local coord sys defined by viewing system
		plane 10000 -10000; # distance to front and back clipping planes from eye
	} elseif  {$viewPlane =="ZX" } {
		vpn 0 1 0; # direction of outward normal to view plane
		prp $uMid 10000 $vMid ; # eye location in local coord sys defined by viewing system
		plane 10000 -10000; # distance to front and back clipping planes from eye
	} elseif  {$viewPlane =="3D" } {
		vpn 1 0.25 1.25; # direction of outward normal to view plane
		prp -100 $vMid 10000; # eye location in local coord sys defined by viewing system
		plane 10000 -10000; # distance to front and back clipping planes from eye
	}  else {
		return -1
	}
	# next three commands define view, all values in local coord system
	if  {$viewPlane =="3D" } {
		viewWindow [expr $uMin-$uWide/4] [expr $uMax/2] [expr $vMin-0.25*$vWide] [expr $vMax] 
	} else {
		viewWindow $uMin $uMax $vMin $vMax
	}
	projection 1; 	# projection mode, 0:prespective, 1: parallel
	fill 1; 		# fill mode; needed only for solid elements

	if {$quadrant == 0} {
		port -1 1 -1 1 	# area of window that will be drawn into (uMin,uMax,vMin,vMax);
	} elseif {$quadrant == 1} {
		port 0 1 0 1 	# area of window that will be drawn into (uMin,uMax,vMin,vMax);
	} elseif {$quadrant == 2} {
		port -1 0 0 1 	# area of window that will be drawn into (uMin,uMax,vMin,vMax);
	} elseif {$quadrant == 3} {
		port -1 0 -1 0 	# area of window that will be drawn into (uMin,uMax,vMin,vMax);
	} elseif {$quadrant == 4} {
		port 0 1 -1 0 	# area of window that will be drawn into (uMin,uMax,vMin,vMax);
	}

	if {$ShapeType ==  "ModeShape" } {
		display -$nEigen 0  [expr 5.*$dAmp]; 	# display mode shape for mode $nEigen
		# create display  for mode shapes
		#---------------------------------
		#                 $windowTitle $xLoc $yLoc $xPixels $yPixels
		#recorder display "Mode Shape 1"  10    10     500      500     -wipe  
		#prp $h $h 1;        # projection reference point (prp); defines the center of projection (viewer eye)
		#vup  0  1 0;                                         # view-up vector (vup) 
		#vpn  0  0 1;                                         # view-plane normal (vpn)     
		#viewWindow -200 200 -200 200;                        # coordiantes of the window relative to prp  
		#display -1 5 20;                                     # the 1st arg. is the tag for display mode (ex. -1 is for the first mode shape)
		# the 2nd arg. is magnification factor for nodes, the 3rd arg. is magnif. factor of deformed shape
		#recorder display "Mode Shape 2" 10 510 500 500 -wipe
		#prp $h $h 1;
		#vup  0  1 0;
		#vpn  0  0 1;
		#viewWindow -200 200 -200 200
		#display -2 5 20

		# get values of eigenvectors for translational DOFs
		#---------------------------------------------------
		#set f11 [nodeEigenvector 3 1 1]
		#set f21 [nodeEigenvector 5 1 1]
		#set f12 [nodeEigenvector 3 2 1]
		#set f22 [nodeEigenvector 5 2 1]
		#puts "eigenvector 1: [list [expr {$f11/$f21}] [expr {$f21/$f21}] ]"
		#puts "eigenvector 2: [list [expr {$f12/$f22}] [expr {$f22/$f22}] ]"

	} elseif  {$ShapeType ==  "NodeNumbers" } {
		display 1 -1 0  ; 		# display node numbers
	} elseif  {$ShapeType ==  "DeformedShape" }  {
		display 1 2 $dAmp; 		# display deformed shape  the 2 makes the nodes small
	}
};                                                                                                                                                          #
######################################################################################

# --------------------------------------------------------------------------------------------------
# Example 8. Bidirectional Uniform Eartquake Excitation
#                             Silvia Mazzoni & Frank McKenna, 2006
# execute this file after you have built the model, and after you apply gravity
#
puts " -------------Uniaxial Inelastic Section, Nonlinear Model -------------"
puts " -------------Uniform Earthquake Excitation -------------"

# source in procedures
source ReadSMDfile.tcl;		# procedure for reading GM file and converting it to proper format

# Bidirectional Uniform Earthquake ground motion (uniform acceleration input at all support nodes)
set iGMfile "H-E01140 H-E12140" ;		# ground-motion filenames, should be different files
set iGMdirection "1 3";			# ground-motion direction
set iGMfact "1.5 0.75";			# ground-motion scaling factor
set dtInput 0.00500 ;		    # DT

# ------------  SET UP -------------------------------------------------------------------------
wipe;				# clear memory of all past model definitions
model BasicBuilder -ndm 3 -ndf 6;	# Define the model builder, ndm=#dimension, ndf=#dofs

puts "Enter the folder name inside the input folder which includes simulation include files: "
gets stdin inputFoldername
set inputFilename "inputs/$inputFoldername/INPUT_"
set InputDir inputs/$inputFoldername;			# set up name of input directory
set FileExt ".tcl"
set outputFilename $inputFoldername
set dataDir outputs/$outputFilename;			# set up name of data directory
file mkdir "$dataDir"; 			# create data directory
set GMdir "GMfiles";		# ground-motion file directory
source LibUnits.tcl;			# define units (kip-in-sec)
source DisplayPlane.tcl;		# procedure for displaying a plane in model
source DisplayModel3D.tcl;		# procedure for displaying 3D perspectives of model
source BuildRCrectSection.tcl;		# procedure for definining RC fiber section

set numModes 3; # decide the number of Modes in total for Modal Analysis
#
# Define SECTIONS -------------------------------------------------------------
set SectionType FiberSection;		# options: Elastic FiberSection
#
set RigidDiaphragm ON ;		# options: ON, OFF. specify this before the analysis parameters are set the constraints are handled differently.
set perpDirn 2;				# perpendicular to plane of rigid diaphragm
set numIntgrPts 5;
# define section tags:
set ColSecTag 1
set BeamSecTag 2
set GirdSecTag 3
set ColSecTagFiber 4
set BeamSecTagFiber 5
set GirdSecTagFiber 6
set SecTagTorsion 70
# ---------------------- Define SECTIONs --------------------------------
source SectionProperties.tcl
#
# ---------------------   INPUT DATA from FILE  -----------------------------------------------------
set Buildingnum 0; # initialize the total number of buildings
set ainputFilename ""
source split_inputFileNames.tcl; # take file names, define number of buildings and take the building IDs
#
# ---------------------   CREATE THE MODEL  ----------------------------------------------------------
for {set numInFile 0} {$numInFile <= [expr $Buildingnum-1]} {incr numInFile 1} {
 source Frame3D_Build_RC.tcl ;  			#inputing many building parameters
 source Loads_Weights_Masses.tcl; 		#Gravity, Nodal Weights, Lateral Loads, Masses
}
if {$Buildingnum>1} {
	source Pounding_buildings.tcl
}
puts "Model Built"
#
# -------------------------  MODAL ANALYSIS  ---------------------------------------------------
source ModalAnalysis.tcl
#
# ---------------------   CREATE OUTPUT FILES  -----------------------------------------------------
for {set numInFile 0} {$numInFile <= [expr $Buildingnum-1]} {incr numInFile 1} {
	source Recorder_outputs.tcl
}
# Define DISPLAY -------------------------------------------------------------
DisplayModel3D DeformedShape ;	 # options: DeformedShape NodeNumbers ModeShape
#
# ---------------------  GRAVITY LOADS  -----------------------------------------------------
source Gravity.tcl
#
if {  [info exists RigidDiaphragm] == 1} {
	if {$RigidDiaphragm=="ON"} {
		variable constraintsTypeGravity Lagrange;	#  large model: try Transformation
	};	# if rigid diaphragm is on
};	# if rigid diaphragm exists
constraints $constraintsTypeGravity ;     		# how it handles boundary conditions
numberer RCM;			# renumber dof's to minimize band-width (optimization), if you want to
system BandGeneral ;		# how to store and solve the system of equations in the analysis (large model: try UmfPack)
test EnergyIncr $Tol 6 ; 		# determine if convergence has been achieved at the end of an iteration step
algorithm Newton;			# use Newton's solution algorithm: updates tangent stiffness at every iteration
set NstepGravity 10;  		# apply gravity in 10 steps
set DGravity [expr 1./$NstepGravity]; 	# first load increment;
integrator LoadControl $DGravity;	# determine the next time step for an analysis
analysis Static;			# define type of analysis static or transient
analyze $NstepGravity;		# apply gravity

# ------------------------------------------------- maintain constant gravity loads and reset time to zero
loadConst -time 0.0

# Plot displacements -------------------------------------------------------------
recorder plot $dataDir/Disp_FreeNodes$_aBID.out DisplDOF[lindex $iGMdirection 0] 1100 10 400 400 -columns  1 [expr 1+[lindex $iGMdirection 0]] ; # a window to plot the nodal displacements versus time
recorder plot $dataDir/Disp_FreeNodes$_aBID.out DisplDOF[lindex $iGMdirection 1] 1100 410 400 400 -columns 1 [expr 1+[lindex $iGMdirection 1]] ; # a window to plot the nodal displacements versus time

# set up ground-motion-analysis parameters
set DtAnalysis	[expr 0.01*$sec];	# time-step Dt for lateral analysis
set TmaxAnalysis	[expr 10. *$sec];	# maximum duration of ground-motion analysis -- should be 50*$sec

# ----------- set up analysis parameters
source LibAnalysisDynamicParameters.tcl;	# constraintsHandler,DOFnumberer,system-ofequations,convergenceTest,solutionAlgorithm,integrator

# ------------ define & apply damping
# RAYLEIGH damping parameters, Where to put M/K-prop damping, switches (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/1099.htm)
#          D=$alphaM*M + $betaKcurr*Kcurrent + $betaKcomm*KlastCommit + $beatKinit*$Kinitial
set xDamp 0.02;					# damping ratio
set MpropSwitch 1.0;
set KcurrSwitch 0.0;
set KcommSwitch 1.0;
set KinitSwitch 0.0;
set nEigenI 1;		# mode 1
set nEigenJ 3;		# mode 3
set lambdaN [eigen [expr $nEigenJ]];			# eigenvalue analysis for nEigenJ modes
set lambdaI [lindex $lambdaN [expr $nEigenI-1]]; 		# eigenvalue mode i
set lambdaJ [lindex $lambdaN [expr $nEigenJ-1]]; 	# eigenvalue mode j
set omegaI [expr pow($lambdaI,0.5)];
set omegaJ [expr pow($lambdaJ,0.5)];
set alphaM [expr $MpropSwitch*$xDamp*(2*$omegaI*$omegaJ)/($omegaI+$omegaJ)];	# M-prop. damping; D = alphaM*M
set betaKcurr [expr $KcurrSwitch*2.*$xDamp/($omegaI+$omegaJ)];         		# current-K;      +beatKcurr*KCurrent
set betaKcomm [expr $KcommSwitch*2.*$xDamp/($omegaI+$omegaJ)];   		# last-committed K;   +betaKcomm*KlastCommitt
set betaKinit [expr $KinitSwitch*2.*$xDamp/($omegaI+$omegaJ)];         			# initial-K;     +beatKinit*Kini
rayleigh $alphaM $betaKcurr $betaKinit $betaKcomm; 				# RAYLEIGH damping

#  ---------------------------------    perform Dynamic Ground-Motion Analysis
# the following commands are unique to the Uniform Earthquake excitation
set IDloadTag 400;	# for uniformSupport excitation
# Uniform EXCITATION: acceleration input
foreach GMdirection $iGMdirection GMfile $iGMfile GMfact $iGMfact {
	incr IDloadTag;
	set inFile $GMdir/$GMfile.at2
	set outFile $GMdir/$GMfile.g3;			# set variable holding new filename (PEER files have .at2/dt2 extension)
	ReadSMDFile $inFile $outFile dt;			# call procedure to convert the ground-motion file
	set GMfatt [expr $g*$GMfact];			# data in input file is in g Unifts -- ACCELERATION TH
	set AccelSeries "Series -dt $dtInput -filePath $outFile -factor  $GMfatt";		# time series information
	pattern UniformExcitation  $IDloadTag  $GMdirection -accel  $AccelSeries  ;	# create Unifform excitation
}

set Nsteps [expr int($TmaxAnalysis/$DtAnalysis)];
set ok [analyze $Nsteps $DtAnalysis];			# actually perform analysis; returns ok=0 if analysis was successful

if {$ok != 0} {      ;					# analysis was not successful.
	# --------------------------------------------------------------------------------------------------
	# change some analysis parameters to achieve convergence
	# performance is slower inside this loop
	#    Time-controlled analysis
	set ok 0;
	set controlTime [getTime];
	while {$controlTime < $TmaxAnalysis && $ok == 0} {
		set controlTime [getTime]
		set ok [analyze 1 $DtAnalysis]
		if {$ok != 0} {
			puts "Trying Newton with Initial Tangent .."
			test NormDispIncr   $Tol 1000  0
			algorithm Newton -initial
			set ok [analyze 1 $DtAnalysis]
			test $testTypeDynamic $TolDynamic $maxNumIterDynamic  0
			algorithm $algorithmTypeDynamic
		}
		if {$ok != 0} {
			puts "Trying Broyden .."
			algorithm Broyden 8
			set ok [analyze 1 $DtAnalysis]
			algorithm $algorithmTypeDynamic
		}
		if {$ok != 0} {
			puts "Trying NewtonWithLineSearch .."
			algorithm NewtonLineSearch .8
			set ok [analyze 1 $DtAnalysis]
			algorithm $algorithmTypeDynamic
		}
	}
};      # end if ok !0

puts "Ground Motion Done. End Time: [getTime]"
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
# ###################
# GRAVITY -------------------------------------------------------------
# define GRAVITY load applied to beams and columns -- eleLoad applies loads in local coordinate axis

pattern Plain 101 Linear {
for {set numInFile 0} {$numInFile <= [expr $Buildingnum-1]} {incr numInFile 1} {
	for {set i 0} {$i <= [expr [llength [lindex $LCol $numInFile]]-1]} {incr i 1} {
		eleLoad -ele [lindex $LCol $numInFile $i 0] -type -beamUniform 0. 0. -$QdlCol; 	# COLUMNS
	}
	for {set i 0} {$i <= [expr [llength [lindex $LBeam $numInFile]]-1]} {incr i 1} {
		eleLoad -ele [lindex $LBeam $numInFile $i 0]  -type -beamUniform -[lindex $QdlBeam $numInFile $i 1] 0.; 	# BEAMS
	}
	for {set i 0} {$i <= [expr [llength [lindex $LGird $numInFile]]-1]} {incr i 1} {
		eleLoad -ele [lindex $LGird $numInFile $i 0]  -type -beamUniform -$QdlGird 0.;	# GIRDS
	}
}
}; # Pattern plain 101 linear close 

puts goGravity
# Gravity-analysis parameters -- load-controlled static analysis
set Tol 1.0e-8;			# convergence tolerance for test
variable constraintsTypeGravity Plain;		# default;
# --------------------------------------------------------------------------------------------------
# dynamic-analysis parameters
# I am setting all these variables as global variables (using variable rather than set command)
#    so that these variables can be uploaded by a procedure
#                                 Silvia Mazzoni & Frank McKenna, 2006


# Set up Analysis Parameters ---------------------------------------------
# CONSTRAINTS handler -- Determines how the constraint equations are enforced in the analysis (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/617.htm)
#          Plain Constraints -- Removes constrained degrees of freedom from the system of equations 
#          Lagrange Multipliers -- Uses the method of Lagrange multipliers to enforce constraints 
#          Penalty Method -- Uses penalty numbers to enforce constraints 
#          Transformation Method -- Performs a condensation of constrained degrees of freedom 
variable constraintsTypeDynamic Transformation;
constraints $constraintsTypeDynamic ; 


# DOF NUMBERER (number the degrees of freedom in the domain): (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/366.htm)
#   determines the mapping between equation numbers and degrees-of-freedom
#          Plain -- Uses the numbering provided by the user 
#          RCM -- Renumbers the DOF to minimize the matrix band-width using the Reverse Cuthill-McKee algorithm 
variable numbererTypeDynamic RCM
numberer $numbererTypeDynamic 

# SYSTEM (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/371.htm)
#   Linear Equation Solvers (how to store and solve the system of equations in the analysis)
#   -- provide the solution of the linear system of equations Ku = P. Each solver is tailored to a specific matrix topology. 
#          ProfileSPD -- Direct profile solver for symmetric positive definite matrices 
#          BandGeneral -- Direct solver for banded unsymmetric matrices 
#          BandSPD -- Direct solver for banded symmetric positive definite matrices 
#          SparseGeneral -- Direct solver for unsymmetric sparse matrices (-piv option)
#          SparseSPD -- Direct solver for symmetric sparse matrices 
#          UmfPack -- Direct UmfPack solver for unsymmetric matrices 
variable systemTypeDynamic BandGeneral;	# try UmfPack for large problems
system $systemTypeDynamic 

# TEST: # convergence test to 
# Convergence TEST (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/360.htm)
#   -- Accept the current state of the domain as being on the converged solution path 
#   -- determine if convergence has been achieved at the end of an iteration step
#          NormUnbalance -- Specifies a tolerance on the norm of the unbalanced load at the current iteration 
#          NormDispIncr -- Specifies a tolerance on the norm of the displacement increments at the current iteration 
#          EnergyIncr-- Specifies a tolerance on the inner product of the unbalanced load and displacement increments at the current iteration 
#          RelativeNormUnbalance --
#          RelativeNormDispIncr --
#          RelativeEnergyIncr --
variable TolDynamic 1.e-8;                        # Convergence Test: tolerance
variable maxNumIterDynamic 10;                # Convergence Test: maximum number of iterations that will be performed before "failure to converge" is returned
variable printFlagDynamic 0;                # Convergence Test: flag used to print information on convergence (optional)        # 1: print information on each step; 
variable testTypeDynamic EnergyIncr;	# Convergence-test type
test $testTypeDynamic $TolDynamic $maxNumIterDynamic $printFlagDynamic;
# for improved-convergence procedure:
	variable maxNumIterConvergeDynamic 2000;	
	variable printFlagConvergeDynamic 0;	

# Solution ALGORITHM: -- Iterate from the last time step to the current (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/682.htm)
#          Linear -- Uses the solution at the first iteration and continues 
#          Newton -- Uses the tangent at the current iteration to iterate to convergence 
#          ModifiedNewton -- Uses the tangent at the first iteration to iterate to convergence 
#          NewtonLineSearch -- 
#          KrylovNewton -- 
#          BFGS -- 
#          Broyden -- 
variable algorithmTypeDynamic ModifiedNewton 
algorithm $algorithmTypeDynamic;        

# Static INTEGRATOR: -- determine the next time step for an analysis  (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/689.htm)
#          LoadControl -- Specifies the incremental load factor to be applied to the loads in the domain 
#          DisplacementControl -- Specifies the incremental displacement at a specified DOF in the domain 
#          Minimum Unbalanced Displacement Norm -- Specifies the incremental load factor such that the residual displacement norm in minimized 
#          Arc Length -- Specifies the incremental arc-length of the load-displacement path 
# Transient INTEGRATOR: -- determine the next time step for an analysis including inertial effects 
#          Newmark -- The two parameter time-stepping method developed by Newmark 
#          HHT -- The three parameter Hilbert-Hughes-Taylor time-stepping method 
#          Central Difference -- Approximates velocity and acceleration by centered finite differences of displacement 
variable NewmarkGamma 0.5;	# Newmark-integrator gamma parameter (also HHT)
variable NewmarkBeta 0.25;	# Newmark-integrator beta parameter
variable integratorTypeDynamic Newmark;
integrator $integratorTypeDynamic $NewmarkGamma $NewmarkBeta

# ANALYSIS  -- defines what type of analysis is to be performed (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/324.htm)
#          Static Analysis -- solves the KU=R problem, without the mass or damping matrices. 
#          Transient Analysis -- solves the time-dependent analysis. The time step in this type of analysis is constant. The time step in the output is also constant. 
#          variableTransient Analysis -- performs the same analysis type as the Transient Analysis object. The time step, however, is variable. This method is used when 
#                 there are convergence problems with the Transient Analysis object at a peak or when the time step is too small. The time step in the output is also variable.
variable analysisTypeDynamic Transient
analysis $analysisTypeDynamic 
##########################################################
# LibMaterialsRC.tcl:  define a library of Reinforced-Concrete materials
#			Silvia Mazzoni & Frank McKenna, 2006
##########################################################

# General Material parameters
set G $Ubig;		# make stiff shear modulus
set J 1.0;			# torsional section stiffness (G makes GJ large)
set GJ [expr $G*$J];

# -----------------------------------------------------------------------------------------------------# confined and unconfined CONCRETE
# nominal concrete compressive strength
set fc 		[expr -4.0*$ksi];		# CONCRETE Compressive Strength, ksi   (+Tension, -Compression)
set Ec 		[expr 57*$ksi*sqrt(-$fc/$psi)];	# Concrete Elastic Modulus
set nu 0.2;
set Gc [expr $Ec/2./[expr 1+$nu]];  	# Torsional stiffness Modulus

# confined concrete
set Kfc 1.3;			# ratio of confined to unconfined concrete strength
set Kres 0.2;			# ratio of residual/ultimate to maximum stress
set fc1C [expr $Kfc*$fc];		# CONFINED concrete (mander model), maximum stress
set eps1C [expr 2.*$fc1C/$Ec];	# strain at maximum stress 
set fc2C [expr $Kres*$fc1C];		# ultimate stress
set eps2C  [expr 20*$eps1C];		# strain at ultimate stress 
set lambda 0.1;			# ratio between unloading slope at $eps2 and initial slope $Ec
# unconfined concrete
set fc1U  $fc;			# UNCONFINED concrete (todeschini parabolic model), maximum stress
set eps1U -0.003;			# strain at maximum strength of unconfined concrete
set fc2U [expr $Kres*$fc1U];		# ultimate stress
set eps2U -0.01;			# strain at ultimate stress

# tensile-strength properties
set ftC [expr -0.14*$fc1C];		# tensile strength +tension
set ftU [expr -0.14*$fc1U];		# tensile strength +tension
set Ets [expr $ftU/0.002];		# tension softening stiffness

# set up library of materials
if {  [info exists imat ] != 1} {set imat 0};		# set value only if it has not been defined previously.
set IDconcCore 1
set IDconcCover 2
uniaxialMaterial Concrete02 $IDconcCore $fc1C $eps1C $fc2C $eps2C $lambda $ftC $Ets;	# Core concrete (confined)
uniaxialMaterial Concrete02 $IDconcCover $fc1U $eps1U $fc2U $eps2U $lambda $ftU $Ets;	# Cover concrete (unconfined)

# -----------------------------------------------------------------------------------------------------# REINFORCING STEEL parameters
#
set Fy [expr 66.8*$ksi];		# STEEL yield stress
set Es [expr 29000.*$ksi];		# modulus of steel
set Bs 0.01;			# strain-hardening ratio 
set R0 18;			# control the transition from elastic to plastic branches
set cR1 0.925;			# control the transition from elastic to plastic branches
set cR2 0.15;			# control the transition from elastic to plastic branches

set IDSteel 3
uniaxialMaterial Steel02 $IDSteel  $Fy $Es $Bs $R0 $cR1 $cR2
# --------------------------------------------------------------------------------------------------
# LibUnits.tcl -- define system of units
#		Silvia Mazzoni & Frank McKenna, 2006
#

# define UNITS ----------------------------------------------------------------------------
set in 1.; 				# define basic units -- output units
set kip 1.; 			# define basic units -- output units
set sec 1.; 			# define basic units -- output units
set LunitTXT "inch";			# define basic-unit text for output
set FunitTXT "kip";			# define basic-unit text for output
set TunitTXT "sec";			# define basic-unit text for output
set ft [expr 12.*$in]; 		# define engineering units
set ksi [expr $kip/pow($in,2)];
set psi [expr $ksi/1000.];
set lbf [expr $psi*$in*$in];		# pounds force
set pcf [expr $lbf/pow($ft,3)];		# pounds per cubic foot
set psf [expr $lbf/pow($ft,3)];		# pounds per square foot
set in2 [expr $in*$in]; 		# inch^2
set in4 [expr $in*$in*$in*$in]; 		# inch^4
set cm [expr $in/2.54];		# centimeter, needed for displacement input in MultipleSupport excitation
set PI [expr 2*asin(1.0)]; 		# define constants
set g [expr 32.2*$ft/pow($sec,2)]; 	# gravitational acceleration
set Ubig 1.e10; 			# a really large number
set Usmall [expr 1/$Ubig]; 		# a really small number


#set in 0.394; 				# in --> cm      1 Zoll = 2.54 cm
#set kip 2.2046; 				# kip --> ton    1 kip = 0.4536 ton
# --------------------------------------------------------------------------------------------------------------------------------
# Define GRAVITY LOADS, weight and masses
# calculate dead load of frame, assume this to be an internal frame (do LL in a similar manner)
# calculate distributed weight along the beam length
#set GammaConcrete [expr 150*$pcf];   		# Reinforced-Concrete floor slabs, defined above
set Tslab [expr 6*$in];			# 6-inch slab
set DLfactor 1.0;				# scale dead load up a little
set QdlGird $QGird; 			# dead load distributed along girder
#
# ---------- Column Weights -----------------------
	set WeightColtmp ""
	set WeightColtmp2 ""
	lappend WeightColtmp 0
	lappend WeightColtmp 0
	for {set i 0} {$i <= [expr [llength [lindex $LCol $numInFile]]-1]} {incr i 1} {
		lappend WeightColtmp2 $WeightColtmp
	}
	lappend WeightCol $WeightColtmp2

	for {set i 0} {$i <= [expr [llength [lindex $LCol $numInFile]]-1]} {incr i 1} {
		 lset WeightCol $numInFile $i 1 [expr $QdlCol*[lindex $LCol $numInFile $i 1]];    # total Column weight
		 lset WeightCol $numInFile $i 0 [lindex $LCol $numInFile $i 0]
	}
# ---------- Girder Weights -----------------------	
	set WeightGirdtmp ""
	set WeightGirdtmp2 ""
	set Lslabtmp ""
	set Lslabtmp2 ""
	set Qslabtmp ""
	lappend WeightGirdtmp 0
	lappend WeightGirdtmp 0
	lappend Lslabtmp 0
	lappend Lslabtmp 0
	lappend Qslabtmp 0
	lappend Qslabtmp 0
	
	for {set i 0} {$i <= [expr [llength [lindex $LGird $numInFile]]-1]} {incr i 1} {
		lappend WeightGirdtmp2 $WeightGirdtmp
		lappend Lslabtmp2 $Lslabtmp
	}
	lappend WeightGird $WeightGirdtmp2
	lappend Lslab $Lslabtmp2

#exteriorBeamnodesID   exteriorGirdernodesID

	for {set i 0} {$i <= [expr [llength [lindex $LGird $numInFile]]-1]} {incr i 1} {
		 lset WeightGird $numInFile  $i 1 [expr $QdlGird*[lindex $LGird $numInFile $i 1]];    # total Gird weight
		 lset Lslab $numInFile  $i 1 [expr [lindex $LGird $numInFile $i 1]/2]; 			# slab extends a distance of $LGird/2 in/out of plane
		 set Qslab [expr $GammaConcrete*$Tslab*[lindex $Lslab $numInFile  $i 1]*$DLfactor]; # ??????????????????????????????
		 lset WeightGird $numInFile  $i 0 [lindex $LGird $numInFile $i 0]
		 lset Lslab $numInFile  $i 0 [lindex $LGird $numInFile $i 0]
	}
	
# ---------- Beam Weights -----------------------
	set WeightBeamtmp ""
	set WeightBeamtmp2 ""
	set QdlBeamtmp2 ""
	set QdlBeamtmp ""
	lappend QdlBeamtmp 0
	lappend QdlBeamtmp 0
	lappend WeightBeamtmp 0
	lappend WeightBeamtmp 0
	for {set i 0} {$i <= [expr [llength [lindex $LBeam $numInFile]]-1]} {incr i 1} {
		lappend WeightBeamtmp2 $WeightBeamtmp
		lappend QdlBeamtmp2 $QdlBeamtmp
	}
	lappend QdlBeam $QdlBeamtmp2
	lappend WeightBeam $WeightBeamtmp2
	for {set i 0} {$i <= [expr [llength [lindex $LBeam $numInFile]]-1]} {incr i 1} {
		 lset QdlBeam $numInFile  $i 1 [expr $Qslab + $QBeam]; 	# dead load distributed along beam (one-way slab)
		 lset QdlBeam $numInFile  $i 0 [lindex $LBeam $numInFile $i 0]
		 lset WeightBeam $numInFile $i 1 [expr [lindex $QdlBeam $numInFile $i 1]*[lindex $LBeam $numInFile $i 1]];    # total Beam weight
		 lset WeightBeam $numInFile $i 0 [lindex $LBeam $numInFile $i 0]
	}

	
# 
# assign masses to the nodes that the columns are connected to 
# each connection takes the mass of 1/2 of each element framing into it (mass=weight/$g)

# ------------------------- MASS NODE ASSIGNMENT is not CORRECT due to unknown NODAL inputting format
set aFloorWeighttmp ""
for {set i 1} {$i <= [lindex $NStory $numInFile]} {incr i 1} {
	lappend aFloorWeighttmp 0
}
	lappend aFloorWeight $aFloorWeighttmp;	# Weight of each floor for each building
	
if [catch {open [lindex $ainputFilename $numInFile 0] r} inFileID] {
	puts stderr "Cannot open input file for reading nodal weights"
} else {
  set flag 1
  set floorcounter 0
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
					set flag2 1
					break
				}
				if {[string match $word "#FLOOR"] == 1} {
					set flag2 0
					set floorcounter [expr $floorcounter+1]
					break
				} else {
				  if {$flag2 == 0} {
					set list [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
					foreach word [split $list] {
						set WeightNodetmp 0
						# Column Weights contribution to nodal mass
						for {set i 0} {$i <= [expr [llength [lindex $LCol $numInFile]]-1]} {incr i 1} {
							if {[lindex $elidcolumnnodes $numInFile $i 1] == $word} {
								set a [lindex $elidcolumnnodes $numInFile $i 0]; #Element ID of connected elements for this node
								for {set j 0} {$j <= [expr [llength [lindex $LCol $numInFile]]-1]} {incr j 1} {
									if {[lindex $WeightCol $numInFile $j 0] == $a} {
										set WeightNodetmp [expr $WeightNodetmp + [expr [lindex $WeightCol $numInFile $j 1]/2]]
									}
								}
							}
							if {[lindex $elidcolumnnodes $numInFile $i 2] == $word} {
								set b [lindex $elidcolumnnodes $numInFile $i 0]; #Element ID of connected elements for this node
								for {set j 0} {$j <= [expr [llength [lindex $LCol $numInFile]]-1]} {incr j 1} {
									if {[lindex $WeightCol $numInFile $j 0] == $b} {
										set WeightNodetmp [expr $WeightNodetmp + [expr [lindex $WeightCol $numInFile $j 1]/2]]
									}
								}
							}
						}
						# Beam Weights contribution to nodal mass
						for {set i 0} {$i <= [expr [llength [lindex $LBeam $numInFile]]-1]} {incr i 1} {
							if {[lindex $elidbeamnodes $numInFile $i 1] == $word} {
								set a [lindex $elidbeamnodes $numInFile $i 0]; #Element ID of connected elements for this node
								for {set j 0} {$j <= [expr [llength [lindex $LBeam $numInFile]]-1]} {incr j 1} {
									if {[lindex $WeightBeam $numInFile $j 0] == $a} {
										set WeightNodetmp [expr $WeightNodetmp + [expr [lindex $WeightBeam $numInFile $j 1]/2]]
									}
								}
							}
							if {[lindex $elidbeamnodes $numInFile $i 2] == $word} {
								set b [lindex $elidbeamnodes $numInFile $i 0]; #Element ID of connected elements for this node
								for {set j 0} {$j <= [expr [llength [lindex $LBeam $numInFile]]-1]} {incr j 1} {
									if {[lindex $WeightBeam $numInFile $j 0] == $b} {
										set WeightNodetmp [expr $WeightNodetmp + [expr [lindex $WeightBeam $numInFile $j 1]/2]]
									}
								}
							}
						}
						# Girder Weights contribution to nodal mass
						for {set i 0} {$i <= [expr [llength [lindex $LGird $numInFile]]-1]} {incr i 1} {
							if {[lindex $elidgirdnodes $numInFile $i 1] == $word} {
								set a [lindex $elidgirdnodes $numInFile $i 0]; #Element ID of connected elements for this node
								for {set j 0} {$j <= [expr [llength [lindex $LGird $numInFile]]-1]} {incr j 1} {
									if {[lindex $WeightGird $numInFile $j 0] == $a} {
										set WeightNodetmp [expr $WeightNodetmp + [expr [lindex $WeightGird $numInFile $j 1]/2]]
									}
								}
							}
							if {[lindex $elidgirdnodes $numInFile $i 2] == $word} {
								set b [lindex $elidgirdnodes $numInFile $i 0]; #Element ID of connected elements for this node
								for {set j 0} {$j <= [expr [llength [lindex $LGird $numInFile]]-1]} {incr j 1} {
									if {[lindex $WeightGird $numInFile $j 0] == $b} {
										set WeightNodetmp [expr $WeightNodetmp + [expr [lindex $WeightGird $numInFile $j 1]/2]]
									}
								}
							}
						}
						set WeightNode $WeightNodetmp;   #actual weight for the Node
						set MassNode [expr $WeightNode/$g];
						mass $word $MassNode 0. $MassNode 0. 0. 0.;	 # define mass
						lset aFloorWeight $numInFile [expr $floorcounter-1] [expr [lindex $aFloorWeight $numInFile [expr $floorcounter-1]] + $WeightNode];    
						break
					}
					break
				  }
				}
			}
		}
	}
	close $inFileID
}

set iFloorWeighttmp2 ""
set maxFrame 0
for {set j 1} {$j <= [lindex $NStory $numInFile]} {incr j 1} {
	if {$maxFrame<[lindex $NFrame $numInFile 1]} {
		set maxFrame [lindex $NFrame $numInFile 1]	
	}
}
for {set i 1} {$i <= $maxFrame} {incr i 1} {
	set iFloorWeighttmp ""
	for {set j 1} {$j <= [lindex $NStory $numInFile]} {incr j 1} {
		lappend iFloorWeighttmp 0
	}
	lappend iFloorWeighttmp2 $iFloorWeighttmp
}
	lappend iFloorWeight $iFloorWeighttmp2;   # Weight of each floor Frames for each building
for {set i 0} {$i <= [expr $maxFrame-1]} {incr i 1} {
	for {set j 0} {$j <=[expr [lindex $NStory $numInFile]-1]} {incr j 1} {
		lset iFloorWeight $numInFile $i $j [expr  [lindex $aFloorWeight $numInFile $j]/[lindex $NFrame $numInFile $j]]
	}
}

set atmp ""
lappend atmp 0
lappend atmp 0
lappend WeightTotal $atmp
lappend MassTotal $atmp
lappend sumWiHi $atmp
set WeightTotaltmp 0
for {set i 1} {$i <= [lindex $NStory $numInFile]} {incr i 1} {
	set WeightTotaltmp [expr $WeightTotaltmp + [lindex $aFloorWeight $numInFile [expr $i-1]]]
}
lset WeightTotal $numInFile 1 $WeightTotaltmp
lset MassTotal $numInFile 1 [expr $WeightTotaltmp/$g]; # total mass for each building


set sumWiHitmp 0.0;		
for {set i 1} {$i <= [lindex $NStory $numInFile]} {incr i 1} {
	# sum of storey weight times height, for lateral-load distribution
	set sumWiHitmp [expr $sumWiHitmp + [lindex $aFloorWeight $numInFile [expr $i-1]]*[lindex $FloorHeight $numInFile [expr $i-1]]]
}
lset sumWiHi $numInFile 1 $sumWiHitmp; 	# sum of storey weight times height, for lateral-load distribution

# --------------------------------------------------------------------------------------------------------------------------------
# LATERAL-LOAD distribution for static pushover analysis
# calculate distribution of lateral load based on mass/weight distributions along building height
# Fj = WjHj/sum(WiHi)  * Weight   at each floor j
# initialize variables for each building as list variables 
set iFPush "";			#lateral load for pushover
set iNodePush "";		# nodes for pushover/cyclic, vectorized
set iFjtmp ""
for {set i 1} {$i <= [lindex $NStory $numInFile]} {incr i 1} {
	lappend iFjtmp 0
}
	lappend iFj $iFjtmp;   # per floor per building

for {set j 0} {$j <=[expr [lindex $NStory $numInFile]-1]} {incr j 1} {	
	set FloorWeight [lindex $iFloorWeight $numInFile 0 $j];
	lset iFj $numInFile $j [expr $FloorWeight*[lindex $FloorHeight $numInFile $j]/[lindex $sumWiHi $numInFile 1]*[lindex $WeightTotal $numInFile 1]];		
}


lappend iNodePush [lindex $iMasterNode $numInFile] ;		# nodes for pushover/cyclic, vectorized
set iFPush $iFj;				# lateral load for pushover, vectorized for each building (list)

puts WeightTotal:$WeightTotal
puts MassTotal:$MassTotal
puts sumWiHi:$sumWiHi
puts iFloorWeight:$iFloorWeight
puts aFloorWeight:$aFloorWeight
puts FloorHeight$FloorHeight
puts FloorWeight$FloorWeight
puts iFj$iFj
puts iFPush$iFPush
#
#
# ------------   Eigenvalue analysis  -------------------------------------------------------
set lambda [eigen $numModes];

# calculate frequencies and periods of the structure ---------------------------------------------------
set omega {}
set f {}
set T {}
set pi 3.141593

foreach lam $lambda {
	lappend omega [expr sqrt($lam)]
	lappend f [expr sqrt($lam)/(2*$pi)]
	lappend T [expr (2*$pi)/sqrt($lam)]
}

# record the eigenvectors
# ------------------------
# record

# Define DISPLAY -------------------------------------------------------------
#DisplayModel3D ModeShape ;	 # options: DeformedShape NodeNumbers ModeShape

# -------------------------------------------------------------

for {set numInFile 0} {$numInFile <= [expr $Buildingnum-1]} {incr numInFile 1} {
	set SupportNodeFirst [lindex $iSupportNode $numInFile 0];						# ID: first support node
	set aBID [lindex $BID $numInFile]; # assign Building number
	set _aBID "_Bid$aBID"

	for { set k 1 } { $k <= $numModes } { incr k } {
		recorder Node -file [format "$dataDir/mode%i$_aBID.out" $k] -node [lindex $FreeNodeID $numInFile] -dof 1 2 3  "eigen $k"
	}
	puts "eigenfrequencies of the Building $aBID are $f"
	puts "periods of the Building $aBID are $T"
}
#
if { $numSpan > 0 && $includeAbutmentGap=="YES"} {
		# Parameters for deck-abutment gap and pounding effects
	set gapAbutment         [expr 6.0*$in];          # When use rigid elements to replace SHJ, we need some length.
	set gammaRatio          [expr 20];               # Stiffness ratio of pounding to the axial stiffness of deck. 
	set poundingStiffness   [expr $gammaRatio*$A_deckEndDiaphragm*0.5*$E_deck/($typicalSpanLength*$numSpanContinuous)];         
	set poundingFy          [expr $poundingStiffness*0.01];
	set eta                 [expr 0.01]; 
	set damage              "nodamage";
};

uniaxialMaterial ElasticPPGap 51 $poundingStiffness $poundingFy [expr -$gapAbutment] $eta $damage;
	element zeroLength    [expr 1*10000+0]        [expr 1*10000+0]         [expr 1*10000+1]        -mat 51 -dir 1; #AbutBridgeGap on The Left
	element zeroLength    [expr ($numSpan+1)*10000+0] [expr $numSpan*10000+9]  [expr ($numSpan+1)*10000+0] -mat 51 -dir 1; #AbutBridgeGap on The Right
	puts -nonewline $ElementsTypeFile "[expr 1*10000+0]        $poundingElementsTypeTag \n";
	puts -nonewline $ElementsTypeFile "[expr ($numSpan+1)*10000+0] $poundingElementsTypeTag \n";
	lappend abutmentGapEleList  [expr 1*10000+0];
	lappend abutmentGapEleList  [expr ($numSpan+1)*10000+0];
	
	
		uniaxialMaterial ElasticPPGap 51 $poundingStiffness $poundingFy [expr -$gapAbutment] $eta $damage;
	element zeroLength    [expr 1*10000+0]        [expr 1*10000+0]         [expr 1*10000+1]        -mat 51 -dir 1; #AbutBridgeGap on The Left
	element zeroLength    [expr ($numSpan+1)*10000+0] [expr $numSpan*10000+9]  [expr ($numSpan+1)*10000+0] -mat 51 -dir 1; #AbutBridgeGap on The Right
	puts -nonewline $ElementsTypeFile "[expr 1*10000+0]        $poundingElementsTypeTag \n";
	puts -nonewline $ElementsTypeFile "[expr ($numSpan+1)*10000+0] $poundingElementsTypeTag \n";
	lappend abutmentGapEleList  [expr 1*10000+0];
	lappend abutmentGapEleList  [expr ($numSpan+1)*10000+0];
#
#	DIKKAT BU DAHA BI BASLANGIC; 
#
# ################################################# implementation of zeroLengthImpact3D with nodes in 3DOF domain:
model BasicBuilder -ndm 3 -ndf 3
node 30110122	576.0	336.0	0.0
node 30110222	576.0	336.0	288.0
node 30110131	576.0	336.0	0.0
node 30110231	576.0	336.0	288.0
node 20110122	576.0	168.0	0.0
node 20110222	576.0	168.0	288.0
node 20110131	576.0	168.0	0.0
node 20110231	576.0	168.0	288.0
model BasicBuilder -ndm 3 -ndf 6
equalDOF 30000122 30110122 1 2 3
equalDOF 30000222 30110222 1 2 3
equalDOF 30000131 30110131 1 2 3
equalDOF 30000231 30110231 1 2 3
equalDOF 20000122 20110122 1 2 3
equalDOF 20000222 20110222 1 2 3
equalDOF 20000131 20110131 1 2 3
equalDOF 20000231 20110231 1 2 3
#
set direction 1; # direction of normal of contact surface
set initGap 0.01; # initial gap  5cm = 1.97 inch
set frictionRatio 0.3; # friction ratio 
set mu 0.3; # friction coefficient 
set Kt 1.6e12; # penalty stiffness for tangential directions 		
set Kn 1.6e12; # penalty stiffness for normal direction		 
set Kn2 [expr $Kn * 0.1]; # penalty stiffness after yielding, based on Hertz impact model 
set Delta_y 0.1; # yield displacement based on Hertz impact model 	  
set cohesion 0; # cohesion
#
element zeroLengthImpact3D 3 30110131 30110122 $direction $initGap $frictionRatio $Kt $Kn $Kn2 $Delta_y $cohesion;
element zeroLengthImpact3D 4 30110231 30110222 $direction $initGap $frictionRatio $Kt $Kn $Kn2 $Delta_y $cohesion;
element zeroLengthImpact3D 5 20110131 20110122 $direction $initGap $frictionRatio $Kt $Kn $Kn2 $Delta_y $cohesion;
element zeroLengthImpact3D 6 20110231 20110222 $direction $initGap $frictionRatio $Kt $Kn $Kn2 $Delta_y $cohesion;
#
#uniaxialMaterial Elastic $matTag $E;
uniaxialMaterial Elastic 6 1.0e2;
uniaxialMaterial Elastic 7 1.0e3;
#element zeroLength $eleTag $iNode $jNode -mat $matTag1 $matTag2 ... -dir $dir1 $dir2 ... <-orient $x1 $x2 $x3 $yp1 $yp2 $yp3> <-doRayleigh $rFlag>
element zeroLength 30000 30110122 30110131 -mat 6 7 6 -dir 1 2 3; # springs with very low stiffness for convergance of Newton-Raphson method 
element zeroLength 40000 30110222 30110231 -mat 6 7 6 -dir 1 2 3; # springs with very low stiffness for convergance of Newton-Raphson method 
element zeroLength 50000 20110122 20110131 -mat 6 7 6 -dir 1 2 3; # springs with very low stiffness for convergance of Newton-Raphson method 
element zeroLength 60000 20110222 20110231 -mat 6 7 6 -dir 1 2 3; # springs with very low stiffness for convergance of Newton-Raphson method 
#
#
###########################################################################
# ReadSMDFile $inFilename $outFilename $dt                                                             #
###########################################################################
# read gm input format
#
# Written: MHS
# Date: July 2000
#
# A procedure which parses a ground motion record from the PEER
# strong motion database by finding dt in the record header, then
# echoing data values to the output file.
#
# Formal arguments
#   inFilename -- file which contains PEER strong motion record
#   outFilename -- file to be written in format G3 can read
#   dt -- time step determined from file header
#
# Assumptions
#   The header in the PEER record is, e.g., formatted as follows:
#    PACIFIC ENGINEERING AND ANALYSIS STRONG-MOTION DATA
#     IMPERIAL VALLEY 10/15/79 2319, EL CENTRO ARRAY 6, 230                           
#     ACCELERATION TIME HISTORY IN UNITS OF G                                         
#     NPTS=  3930, DT= .00500 SEC

proc ReadSMDFile {inFilename outFilename dt} {
	# read gm input format

   # Pass dt by reference
   upvar $dt DT

   # Open the input file and catch the error if it can't be read
   if [catch {open $inFilename r} inFileID] {
      puts stderr "Cannot open $inFilename for reading"
   } else {
      # Open output file for writing
      set outFileID [open $outFilename w]

      # Flag indicating dt is found and that ground motion
      # values should be read -- ASSUMES dt is on last line
      # of header!!!
      set flag 0

      # Look at each line in the file
      foreach line [split [read $inFileID] \n] {

         if {[llength $line] == 0} {
            # Blank line --> do nothing
            continue
         } elseif {$flag == 1} {
            # Echo ground motion values to output file
            puts $outFileID $line
         } else {
            # Search header lines for dt
            foreach word [split $line] {
               # Read in the time step
               if {$flag == 1} {
                  set DT $word
                  break
               }
               # Find the desired token and set the flag
               if {[string match $word "DT="] == 1} {set flag 1}
            }
         }
      }

      # Close the output file
      close $outFileID

      # Close the input file
      close $inFileID
   }
};                                                                                                                                     #
###########################################################################

# --------------------------------------------------------------------------------------------------
#
# 				OUTPUTTING THE RESULTS
#
#
# Define RECORDERS -------------------------------------------------------------

	set SupportNodeFirst [lindex $iSupportNode $numInFile 0];						# ID: first support node
	set SupportNodeLast [lindex $iSupportNode $numInFile [expr [llength [lindex $iSupportNode $numInFile]]-1]];		# ID: last support node 
	set MasterNodeFirst [lindex $iMasterNode $numInFile 0];						# ID: first master node
	set MasterNodeLast [lindex $iMasterNode $numInFile [expr [llength [lindex $iMasterNode $numInFile]]-1]];			# ID: last master node
	
	set aBID [lindex $BID $numInFile 0]; # assign Building number
	set _aBID "_Bid$aBID"
	set underscore "_"
	set _numIntgrPts_ "_$numIntgrPts$underscore"

# ------------------------------- Ground Column IDs to output element RESULTs ------------------------------------------
	set FirstColumntmp2 ""
	for {set i 0} {$i <= [expr [llength [lindex $iSupportNode $numInFile]]-1]} {incr i 1} {
		for {set j 0} {$j <= [expr [llength [lindex $LCol $numInFile]]-1]} {incr j 1} {
			if {[lindex $elidcolumnnodes $numInFile $j 1] == [lindex $iSupportNode $numInFile $i]} {
				set FirstColumntmp [lindex $elidcolumnnodes $numInFile $j 0];	# Take the Ground Columns for outputing purposes 
			} elseif {[lindex $elidcolumnnodes $numInFile $j 2] == [lindex $iSupportNode $numInFile $i]} {
				set FirstColumntmp [lindex $elidcolumnnodes $numInFile $j 0];	# Take the Ground Columns for outputing purposes 
			}
		}
		lappend FirstColumntmp2 $FirstColumntmp
	}
	lappend FirstColumn $FirstColumntmp2

	recorder Node -file $dataDir/Disp_FreeNodes$_aBID.out -time -node [lindex $FreeNodeID $numInFile 0] -dof 1 2 3 disp; # displacements of free node
	recorder Node -file $dataDir/Disp_MasterNodes$_aBID.out -time -nodeRange $MasterNodeFirst $MasterNodeLast -dof 1 2 3 disp;# displacements of master nodes
	recorder Node -file $dataDir/Disp_BaseNodes$_aBID.out -time -nodeRange $SupportNodeFirst $SupportNodeLast -dof 1 2 3 disp;# displacements of support nodes
	recorder Node -file $dataDir/Reaction_BaseNodes$_aBID.out -time -nodeRange $SupportNodeFirst $SupportNodeLast -dof 1 2 3 reaction;	# support reaction
	recorder Drift -file $dataDir/DrNode_LateralDrift$_aBID.out -time -iNode $SupportNodeFirst  -jNode [lindex $FreeNodeID $numInFile 0] -dof 1 -perpDirn 2;	# lateral drift

	for {set i 0} {$i <= [expr [llength [lindex $iSupportNode $numInFile]]-1]} {incr i 1} {
		set aFirstColumn [lindex $FirstColumn $numInFile $i]
		recorder Element -file $dataDir/ForceEle_$aFirstColumn$_aBID.out -time -ele $aFirstColumn localForce;				# element forces in local coordinates
		recorder Element -file $dataDir/ForceEle_sec_1_$aFirstColumn$_aBID.out -time -ele $aFirstColumn section 1 force;	# section forces, axial and moment, node i
		recorder Element -file $dataDir/DefoEle_sec_1_$aFirstColumn$_aBID.out -time -ele $aFirstColumn section 1 deformation;	# section deformations, axial and curvature, node i
		recorder Element -file $dataDir/ForceEle_sec$_numIntgrPts_$aFirstColumn$_aBID.out -time -ele $aFirstColumn section $numIntgrPts force;	# section forces, axial and moment, node j
		recorder Element -file $dataDir/DefoEle_sec$_numIntgrPts_$aFirstColumn$_aBID.out -time -ele $aFirstColumn section $numIntgrPts deformation;# section deformations, axial and curvature, node j
		set yFiber [expr $HCol/2-$cover];		# fiber location for stress-strain recorder, local coords
		set zFiber [expr $BCol/2-$cover];		# fiber location for stress-strain recorder, local coords
		recorder Element -file $dataDir/StressStrain_concEle_sec_1_$aFirstColumn$_aBID.out -time -ele $aFirstColumn section $numIntgrPts fiber $yFiber $zFiber $IDconcCore  stressStrain;	# Core Concrete stress-strain, node i
		recorder Element -file $dataDir/StressStrain_reinfEle_sec_1_$aFirstColumn$_aBID.out -time -ele $aFirstColumn section $numIntgrPts fiber $yFiber $zFiber $IDSteel  stressStrain;	# steel fiber stress-strain, node i
	}
	recorder Element -file $dataDir/ForceEletest_220020101.out -time -ele 220020101 localForce;				# element forces in local coordinates
	
#
#

# Section Properties:
set HCol [expr 18*$in];		# square-Column width
set BCol $HCol
set HBeam [expr 24*$in];		# Beam depth -- perpendicular to bending axis
set BBeam [expr 18*$in];		# Beam width -- parallel to bending axis
set HGird [expr 24*$in];		# Girder depth -- perpendicular to bending axis
set BGird [expr 18*$in];		# Girder width -- parallel to bending axis

set GammaConcrete [expr 150*$pcf];
set QdlCol [expr $GammaConcrete*$HCol*$BCol];	# self weight of Column, weight per length
set QBeam [expr $GammaConcrete*$HBeam*$BBeam];	# self weight of Beam, weight per length
set QGird [expr $GammaConcrete*$HGird*$BGird];	# self weight of Gird, weight per length

if {$SectionType == "Elastic"} {
	# material properties:
	set fc 4000*$psi;			# concrete nominal compressive strength
	set Ec [expr 57*$ksi*pow($fc/$psi,0.5)];	# concrete Young's Modulus
	set nu 0.2;			# Poisson's ratio
	set Gc [expr $Ec/2./[expr 1+$nu]];  	# Torsional stiffness Modulus
	set J $Ubig;			# set large torsional stiffness
	# column section properties:
	set AgCol [expr $HCol*$BCol];		# rectuangular-Column cross-sectional area
	set IzCol [expr 0.5*1./12*$BCol*pow($HCol,3)];	# about-local-z Rect-Column gross moment of inertial
	set IyCol [expr 0.5*1./12*$HCol*pow($BCol,3)];	# about-local-z Rect-Column gross moment of inertial
	# beam sections:
	set AgBeam [expr $HBeam*$BBeam];		# rectuangular-Beam cross-sectional area
	set IzBeam [expr 0.5*1./12*$BBeam*pow($HBeam,3)];	# about-local-z Rect-Beam cracked moment of inertial
	set IyBeam [expr 0.5*1./12*$HBeam*pow($BBeam,3)];	# about-local-y Rect-Beam cracked moment of inertial
	# girder sections:
	set AgGird [expr $HGird*$BGird];		# rectuangular-Girder cross-sectional area
	set IzGird [expr 0.5*1./12*$BGird*pow($HGird,3)];	# about-local-z Rect-Girder cracked moment of inertial
	set IyGird [expr 0.5*1./12*$HGird*pow($BGird,3)];	# about-local-y Rect-Girder cracked moment of inertial
		
	section Elastic $ColSecTag $Ec $AgCol $IzCol $IyCol $Gc $J
	section Elastic $BeamSecTag $Ec $AgBeam $IzBeam $IyBeam $Gc $J
	section Elastic $GirdSecTag $Ec $AgGird $IzGird $IyGird $Gc $J

	set IDconcCore  1;		# material numbers for recorder (this stressstrain recorder will be blank, as this is an elastic section)
	set IDSteel  2;			# material numbers for recorder (this stressstrain recorder will be blank, as this is an elastic section)

} elseif {$SectionType == "FiberSection"} {
	# MATERIAL parameters 
	source LibMaterialsRC.tcl;	# define library of Reinforced-concrete Materials
	# FIBER SECTION properties 
	# Column section geometry:
	set cover [expr 2.5*$in];	# rectangular-RC-Column cover
	set numBarsTopCol 8;		# number of longitudinal-reinforcement bars on top layer
	set numBarsBotCol 8;		# number of longitudinal-reinforcement bars on bottom layer
	set numBarsIntCol 6;		# TOTAL number of reinforcing bars on the intermediate layers
	set barAreaTopCol [expr 1.*$in*$in];	# longitudinal-reinforcement bar area
	set barAreaBotCol [expr 1.*$in*$in];	# longitudinal-reinforcement bar area
	set barAreaIntCol [expr 1.*$in*$in];	# longitudinal-reinforcement bar area

	set numBarsTopBeam 6;		# number of longitudinal-reinforcement bars on top layer
	set numBarsBotBeam 6;		# number of longitudinal-reinforcement bars on bottom layer
	set numBarsIntBeam 2;		# TOTAL number of reinforcing bars on the intermediate layers
	set barAreaTopBeam [expr 1.*$in*$in];	# longitudinal-reinforcement bar area
	set barAreaBotBeam [expr 1.*$in*$in];	# longitudinal-reinforcement bar area
	set barAreaIntBeam [expr 1.*$in*$in];	# longitudinal-reinforcement bar area

	set numBarsTopGird 6;		# number of longitudinal-reinforcement bars on top layer
	set numBarsBotGird 6;		# number of longitudinal-reinforcement bars on bottom layer
	set numBarsIntGird 2;		# TOTAL number of reinforcing bars on the intermediate layers
	set barAreaTopGird [expr 1.*$in*$in];	# longitudinal-reinforcement bar area
	set barAreaBotGird [expr 1.*$in*$in];	# longitudinal-reinforcement bar area
	set barAreaIntGird [expr 1.*$in*$in];	# longitudinal-reinforcement bar area

	set nfCoreY 12;		# number of fibers in the core patch in the y direction
	set nfCoreZ 12;		# number of fibers in the core patch in the z direction
	set nfCoverY 8;		# number of fibers in the cover patches with long sides in the y direction
	set nfCoverZ 8;		# number of fibers in the cover patches with long sides in the z direction
	# rectangular section with one layer of steel evenly distributed around the perimeter and a confined core.
	BuildRCrectSection $ColSecTagFiber $HCol $BCol $cover $cover $IDconcCore  $IDconcCover $IDSteel $numBarsTopCol $barAreaTopCol $numBarsBotCol $barAreaBotCol $numBarsIntCol $barAreaIntCol  $nfCoreY $nfCoreZ $nfCoverY $nfCoverZ
	BuildRCrectSection $BeamSecTagFiber $HBeam $BBeam $cover $cover $IDconcCore  $IDconcCover $IDSteel $numBarsTopBeam $barAreaTopBeam $numBarsBotBeam $barAreaBotBeam $numBarsIntBeam $barAreaIntBeam  $nfCoreY $nfCoreZ $nfCoverY $nfCoverZ
	BuildRCrectSection $GirdSecTagFiber $HGird $BGird $cover $cover $IDconcCore  $IDconcCover $IDSteel $numBarsTopGird $barAreaTopGird $numBarsBotGird $barAreaBotGird $numBarsIntGird $barAreaIntGird  $nfCoreY $nfCoreZ $nfCoverY $nfCoverZ

	# assign torsional Stiffness for 3D Model
	uniaxialMaterial Elastic $SecTagTorsion $Ubig
	section Aggregator $ColSecTag $SecTagTorsion T -section $ColSecTagFiber
	section Aggregator $BeamSecTag $SecTagTorsion T -section $BeamSecTagFiber
	section Aggregator $GirdSecTag $SecTagTorsion T -section $GirdSecTagFiber
} else {
	puts "No section has been defined"
	return -1
}
#
#	Assumed input file names are like "xxx_123.tcl"
#	where xxx and 123 are seperated by "_"
#	and the file has an extension ".tcl"
#   123 is the building ID (BID)
#
set contents [glob -directory  $InputDir "*.tcl"]

foreach item $contents {
    lappend pathname $item
}
foreach ff $pathname {
    set ff [split $ff "/"]
    lappend Filename [lindex $ff [expr [llength $ff]-1]]
}
foreach ll $Filename {
    set ll [split $ll "_"]
    lappend infiles [lindex $ll 1]
}
foreach kk $infiles {
    set kk [split $kk $FileExt]
	set iBID [lindex $kk 0]
    lappend BID $iBID
	lappend ainputFilename $inputFilename$iBID$FileExt
	set Buildingnum [expr $Buildingnum+1]
}
#
# Script Identifying:
#		IDBeamTransf   IDGirdTransf   IDColTransf
# 	(Perpendicular unit vectors to each element axis)
# 	For the Linear Transformation Purpose
#
#
# --------- Take all Element ID's with their nodes  ---------
   if [catch {open [lindex $ainputFilename $numInFile 0] r} inFileID] {
      puts stderr "Cannot open input file"
   } else {
      set flag 0
	  set BeamConnect ""
	  set GirderConnect ""
	  set ColumnConnect ""
      foreach line [split [read $inFileID] \n] {
         if {[llength $line] == 0} {
            # Blank line --> do nothing
            continue
         } elseif {$flag == 1} {
		    foreach word [split $line] {
			   if {[string match $word "#END"] == 1} {set flag 0}
            }
			if {$flag == 1} {
				foreach word [split $line] {
					if {[string match $word "beam"] == 1} {
						set list [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
						set BeamConnecttmp ""
						foreach BeamConnecttmp2 [split $list] {
							lappend BeamConnecttmp $BeamConnecttmp2
						}
						lappend BeamConnect $BeamConnecttmp
					}
					if {[string match $word "girder"] == 1} {
						set list [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
						set GirderConnecttmp ""
						foreach GirderConnecttmp2 [split $list] {
							lappend GirderConnecttmp $GirderConnecttmp2
						}
						lappend GirderConnect $GirderConnecttmp
					}
					if {[string match $word "column"] == 1} {
						set list [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
						set ColumnConnecttmp ""
						foreach ColumnConnecttmp2 [split $list] {
							lappend ColumnConnecttmp $ColumnConnecttmp2
						}
						lappend ColumnConnect $ColumnConnecttmp
					}
				}
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
lappend iBeamConnect $BeamConnect
lappend iGirderConnect $GirderConnect
lappend iColumnConnect $ColumnConnect
						

# --------- Take all Node ID's with their coordinates  ---------						
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
	
# --------- Make the list for perpendicular vectors for each element axis  ---------			
set Beamvecxz ""
set Girdervecxz ""
set Columnvecxz ""
for {set k 0} {$k <= [expr [llength [lindex $iBeamConnect $numInFile]]-1]} {incr k 1} {;	# For Beams
set vecxztmp ""
	for {set m 0} {$m <= [expr [llength [lindex $iNodeList $numInFile]]-1]} {incr m 1} {
		if {[lindex $iBeamConnect $numInFile $k 1]==[lindex $iNodeList $numInFile $m 0]} {; # search element's first node in Nodelist
			set vecxztmp1x [lindex $iNodeList $numInFile $m 1]
			set vecxztmp1y [lindex $iNodeList $numInFile $m 2]
			set vecxztmp1z [lindex $iNodeList $numInFile $m 3]
		}
		if {[lindex $iBeamConnect $numInFile $k 2]==[lindex $iNodeList $numInFile $m 0]} {; # search element's second node in Nodelist
			set vecxztmp2x [lindex $iNodeList $numInFile $m 1]
			set vecxztmp2y [lindex $iNodeList $numInFile $m 2]
			set vecxztmp2z [lindex $iNodeList $numInFile $m 3]
		}
	}
	if {$vecxztmp1x>$vecxztmp2x} {
		#set changetmp $vecxztmp1z
		#set vecxztmp1z $vecxztmp2z
		#set vecxztmp2z $changetmp
		#set changetmp $vecxztmp1x
		#set vecxztmp1x $vecxztmp2x
		#set vecxztmp2x $changetmp
	# { x, z } becomes { -z, x } : perpendicular CCW
		set vecxztmpx [expr $vecxztmp2z-$vecxztmp1z]
		set vecxztmpz [expr $vecxztmp1x-$vecxztmp2x]		
	}
		
	# { x, z } becomes { z, -x } : perpendicular CW
	set vecxztmpx [expr $vecxztmp1z-$vecxztmp2z]
	set vecxztmpz [expr $vecxztmp2x-$vecxztmp1x]
	
	set vecxztmpabs [expr {sqrt($vecxztmpx*$vecxztmpx+$vecxztmpz*$vecxztmpz)}]
	set vecxztmpx [expr {$vecxztmpx/$vecxztmpabs}]
	set vecxztmpz [expr {$vecxztmpz/$vecxztmpabs}]

	lappend vecxztmp $vecxztmpx
	lappend vecxztmp $vecxztmpz
	lappend Beamvecxz $vecxztmp
}

for {set k 0} {$k <= [expr [llength [lindex $iGirderConnect $numInFile]]-1]} {incr k 1} {;	# For Girder
set vecxztmp ""
	for {set m 0} {$m <= [expr [llength [lindex $iNodeList $numInFile]]-1]} {incr m 1} {
		if {[lindex $iGirderConnect $numInFile $k 1]==[lindex $iNodeList $numInFile $m 0]} {; # search element's first node in Nodelist
			set vecxztmp1x [lindex $iNodeList $numInFile $m 1]
			set vecxztmp1y [lindex $iNodeList $numInFile $m 2]
			set vecxztmp1z [lindex $iNodeList $numInFile $m 3]
		}
		if {[lindex $iGirderConnect $numInFile $k 2]==[lindex $iNodeList $numInFile $m 0]} {; # search element's second node in Nodelist
			set vecxztmp2x [lindex $iNodeList $numInFile $m 1]
			set vecxztmp2y [lindex $iNodeList $numInFile $m 2]
			set vecxztmp2z [lindex $iNodeList $numInFile $m 3]
		}
	}
	if {$vecxztmp1z>$vecxztmp2z} {
#		set changetmp $vecxztmp1z
#		set vecxztmp1z $vecxztmp2z
#		set vecxztmp2z $changetmp
#		set changetmp $vecxztmp1x
#		set vecxztmp1x $vecxztmp2x
#		set vecxztmp2x $changetmp
	# { x, z } becomes { z, -x } : perpendicular CW
	
	set vecxztmpx [expr $vecxztmp1z-$vecxztmp2z]
	set vecxztmpz [expr $vecxztmp2x-$vecxztmp1x]
	} 
	# { x, z } becomes { -z, x } : perpendicular CCW
	set vecxztmpx [expr $vecxztmp2z-$vecxztmp1z]
	set vecxztmpz [expr $vecxztmp1x-$vecxztmp2x]	

	
	set vecxztmpabs [expr {sqrt($vecxztmpx*$vecxztmpx+$vecxztmpz*$vecxztmpz)}]
	set vecxztmpx [expr {$vecxztmpx/$vecxztmpabs}]
	set vecxztmpz [expr {$vecxztmpz/$vecxztmpabs}]

	lappend vecxztmp $vecxztmpx
	lappend vecxztmp $vecxztmpz
	lappend Girdervecxz $vecxztmp
}

set ivecxztmp ""
lappend ivecxztmp 0.0
lappend ivecxztmp 0.0
lappend ivecxztmp 0.0
lappend ivecxztmp 0.0
set ivecxztmp2 ""
for {set i 0} {$i <= [expr [llength [lindex $iBeamConnect $numInFile]]-1]} {incr i 1} {
	lappend ivecxztmp2 $ivecxztmp
};	# IDTransf = {ElementID, vecxzX, vecxzY, vecxzZ}
lappend IDBeamTransf $ivecxztmp2

set ivecxztmp2 ""
for {set i 0} {$i <= [expr [llength [lindex $iGirderConnect $numInFile]]-1]} {incr i 1} {
	lappend ivecxztmp2 $ivecxztmp
};	# IDTransf = {ElementID, vecxzX, vecxzY, vecxzZ}
lappend IDGirdTransf $ivecxztmp2

for {set k 0} {$k <= [expr [llength [lindex $iBeamConnect $numInFile]]-1]} {incr k 1} {
	lset IDBeamTransf $numInFile $k 0 [lindex $iBeamConnect $numInFile $k 0]
	# Perpendicular vector to element Axis:
	lset IDBeamTransf $numInFile $k 1 [lindex $Beamvecxz $k 0]
	lset IDBeamTransf $numInFile $k 3 [lindex $Beamvecxz $k 1]
}

for {set k 0} {$k <= [expr [llength [lindex $iGirderConnect $numInFile]]-1]} {incr k 1} {
	lset IDGirdTransf $numInFile $k 0 [lindex $iGirderConnect $numInFile $k 0]
	# Perpendicular vector to element Axis:
	lset IDGirdTransf $numInFile $k 1 [lindex $Girdervecxz $k 0]
	lset IDGirdTransf $numInFile $k 3 [lindex $Girdervecxz $k 1]
}

for {set i 0} {$i <= [expr [llength [lindex $iColumnConnect $numInFile]]-1]} {incr i 1} {;	# For Column
set vecxztmp ""
	for {set k 0} {$k <= [expr [llength [lindex $iBeamConnect $numInFile]]-1]} {incr k 1} {
		if {[lindex $iBeamConnect $numInFile $k 1]==[lindex $iColumnConnect $numInFile $i 1]} {
			set vecxztmpx [lindex $IDBeamTransf $numInFile $k 1]
			set vecxztmpz [lindex $IDBeamTransf $numInFile $k 3]
		} elseif {[lindex $iBeamConnect $numInFile $k 1]==[lindex $iColumnConnect $numInFile $i 2]} {
			set vecxztmpx [lindex $IDBeamTransf $numInFile $k 1]
			set vecxztmpz [lindex $IDBeamTransf $numInFile $k 3]			
		}
		if {[lindex $iBeamConnect $numInFile $k 2]==[lindex $iColumnConnect $numInFile $i 1]} {
			set vecxztmpx [lindex $IDBeamTransf $numInFile $k 1]
			set vecxztmpz [lindex $IDBeamTransf $numInFile $k 3]
		} elseif {[lindex $iBeamConnect $numInFile $k 2]==[lindex $iColumnConnect $numInFile $i 2]} {
			set vecxztmpx [lindex $IDBeamTransf $numInFile $k 1]
			set vecxztmpz [lindex $IDBeamTransf $numInFile $k 3]
		}
	}
	lappend vecxztmp $vecxztmpx
	lappend vecxztmp $vecxztmpz
	lappend Columnvecxz $vecxztmp
}

set ivecxztmp2 ""
for {set i 0} {$i <= [expr [llength [lindex $iColumnConnect $numInFile]]-1]} {incr i 1} {
	lappend ivecxztmp2 $ivecxztmp
};	# IDTransf = {ElementID, vecxzX, vecxzY, vecxzZ}
lappend IDColTransf $ivecxztmp2

for {set k 0} {$k <= [expr [llength [lindex $iColumnConnect $numInFile]]-1]} {incr k 1} {
	lset IDColTransf $numInFile $k 0 [lindex $iColumnConnect $numInFile $k 0]
	# Perpendicular vector to element Axis:
	lset IDColTransf $numInFile $k 1 [lindex $Columnvecxz $k 0]
	lset IDColTransf $numInFile $k 3 [lindex $Columnvecxz $k 1]
}
# define ELEMENTS tags
# set up geometric transformations of element
#   separate columns and beams, in case of P-Delta analysis for columns
#set IDColTransf 1; # all columns
#set IDBeamTransf 2; # all beams
#set IDGirdTransf 3; # all girds
set ColTransfType Linear ;		# options for columns: Linear PDelta  Corotational
#
puts IDBeamTransf$IDBeamTransf
puts IDGirdTransf$IDGirdTransf
for {set k 0} {$k <= [expr [llength [lindex $iBeamConnect $numInFile]]-1]} {incr k 1} {
	set vecxzX [lindex $IDBeamTransf $numInFile $k 1]
	set vecxzY [lindex $IDBeamTransf $numInFile $k 2]
	set vecxzZ	[lindex $IDBeamTransf $numInFile $k 3]
	geomTransf Linear [lindex $IDBeamTransf $numInFile $k 0] $vecxzX $vecxzY $vecxzZ
}

for {set k 0} {$k <= [expr [llength [lindex $iGirderConnect $numInFile]]-1]} {incr k 1} {
	set vecxzX [lindex $IDGirdTransf $numInFile $k 1]
	set vecxzY [lindex $IDGirdTransf $numInFile $k 2]
	set vecxzZ	[lindex $IDGirdTransf $numInFile $k 3]
	geomTransf Linear [lindex $IDGirdTransf $numInFile $k 0] $vecxzX $vecxzY $vecxzZ
}

for {set k 0} {$k <= [expr [llength [lindex $iColumnConnect $numInFile]]-1]} {incr k 1} {
	set vecxzX [lindex $IDColTransf $numInFile $k 1]
	set vecxzY [lindex $IDColTransf $numInFile $k 2]
	set vecxzZ	[lindex $IDColTransf $numInFile $k 3]
	# orientation of column stiffness affects bidirectional response.
	geomTransf $ColTransfType [lindex $IDColTransf $numInFile $k 0] $vecxzX $vecxzY $vecxzZ
}
#
#		
