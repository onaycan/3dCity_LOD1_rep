# --------------------------------------------------------------------------------------------------------------------------------
# Define GRAVITY LOADS, weight and masses
# calculate dead load of frame, assume this to be an internal frame (do LL in a similar manner)
# calculate distributed weight along the beam length
#set GammaConcrete [expr 150*$pcf];   		# Reinforced-Concrete floor slabs, defined above
set Tslab [expr 6*$in];			# 6-inch slab
set DLfactor 1.0;				# scale dead load up a little
set QdlGird $QGird; 			# dead load distributed along girder
#
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
							if {[lindex $iColumnConnect $numInFile $i 1] == $word} {
								set a [lindex $iColumnConnect $numInFile $i 0]; #Element ID of connected elements for this node
								for {set j 0} {$j <= [expr [llength [lindex $LCol $numInFile]]-1]} {incr j 1} {
									if {[lindex $WeightCol $numInFile $j 0] == $a} {
										set WeightNodetmp [expr $WeightNodetmp + [expr [lindex $WeightCol $numInFile $j 1]/2]]
									}
								}
							}
							if {[lindex $iColumnConnect $numInFile $i 2] == $word} {
								set b [lindex $iColumnConnect $numInFile $i 0]; #Element ID of connected elements for this node
								for {set j 0} {$j <= [expr [llength [lindex $LCol $numInFile]]-1]} {incr j 1} {
									if {[lindex $WeightCol $numInFile $j 0] == $b} {
										set WeightNodetmp [expr $WeightNodetmp + [expr [lindex $WeightCol $numInFile $j 1]/2]]
									}
								}
							}
						}
						# Beam Weights contribution to nodal mass
						for {set i 0} {$i <= [expr [llength [lindex $LBeam $numInFile]]-1]} {incr i 1} {
							if {[lindex $iBeamConnect $numInFile $i 1] == $word} {
								set a [lindex $iBeamConnect $numInFile $i 0]; #Element ID of connected elements for this node
								for {set j 0} {$j <= [expr [llength [lindex $LBeam $numInFile]]-1]} {incr j 1} {
									if {[lindex $WeightBeam $numInFile $j 0] == $a} {
										set WeightNodetmp [expr $WeightNodetmp + [expr [lindex $WeightBeam $numInFile $j 1]/2]]
									}
								}
							}
							if {[lindex $iBeamConnect $numInFile $i 2] == $word} {
								set b [lindex $iBeamConnect $numInFile $i 0]; #Element ID of connected elements for this node
								for {set j 0} {$j <= [expr [llength [lindex $LBeam $numInFile]]-1]} {incr j 1} {
									if {[lindex $WeightBeam $numInFile $j 0] == $b} {
										set WeightNodetmp [expr $WeightNodetmp + [expr [lindex $WeightBeam $numInFile $j 1]/2]]
									}
								}
							}
						}
						# Girder Weights contribution to nodal mass
						for {set i 0} {$i <= [expr [llength [lindex $LGird $numInFile]]-1]} {incr i 1} {
							if {[lindex $iGirderConnect $numInFile $i 1] == $word} {
								set a [lindex $iGirderConnect $numInFile $i 0]; #Element ID of connected elements for this node
								for {set j 0} {$j <= [expr [llength [lindex $LGird $numInFile]]-1]} {incr j 1} {
									if {[lindex $WeightGird $numInFile $j 0] == $a} {
										set WeightNodetmp [expr $WeightNodetmp + [expr [lindex $WeightGird $numInFile $j 1]/2]]
									}
								}
							}
							if {[lindex $iGirderConnect $numInFile $i 2] == $word} {
								set b [lindex $iGirderConnect $numInFile $i 0]; #Element ID of connected elements for this node
								for {set j 0} {$j <= [expr [llength [lindex $LGird $numInFile]]-1]} {incr j 1} {
									if {[lindex $WeightGird $numInFile $j 0] == $b} {
										set WeightNodetmp [expr $WeightNodetmp + [expr [lindex $WeightGird $numInFile $j 1]/2]]
									}
								}
							}
						}
						set WeightNode $WeightNodetmp;   #actual weight for the Node
						set MassNode [expr $WeightNode/$g];
						if {[lindex $NStory $numInFile]==1} {
							mass $word $MassNode 1e-9 $MassNode 0. 0. 0.;	 # define mass
						} else {
							mass $word $MassNode 0. $MassNode 0. 0. 0.;	 # define mass
						}
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
#for {set i 1} {$i <= [lindex $NStory $numInFile]} {incr i 1} {
	# sum of storey weight times height, for lateral-load distribution
#	set sumWiHitmp [expr $sumWiHitmp + [lindex $aFloorWeight $numInFile [expr $i-1]]*[lindex $FloorHeight $numInFile [expr $i-1]]]
#}
#lset sumWiHi $numInFile 1 $sumWiHitmp; 	# sum of storey weight times height, for lateral-load distribution

# --------------------------------------------------------------------------------------------------------------------------------
# LATERAL-LOAD distribution for static pushover analysis
# calculate distribution of lateral load based on mass/weight distributions along building height
# Fj = WjHj/sum(WiHi)  * Weight   at each floor j
# initialize variables for each building as list variables 
set iFPush "";			#lateral load for pushover
set iNodePush "";		# nodes for pushover/cyclic, vectorized
set iFjtmp ""
#for {set i 1} {$i <= [lindex $NStory $numInFile]} {incr i 1} {
#	lappend iFjtmp 0
#}
#	lappend iFj $iFjtmp;   # per floor per building

#for {set j 0} {$j <=[expr [lindex $NStory $numInFile]-1]} {incr j 1} {	
#	set FloorWeight [lindex $iFloorWeight $numInFile 0 $j];
#	lset iFj $numInFile $j [expr $FloorWeight*[lindex $FloorHeight $numInFile $j]/[lindex $sumWiHi $numInFile 1]*[lindex $WeightTotal $numInFile 1]];		
#}


#lappend iNodePush [lindex $iMasterNode $numInFile] ;		# nodes for pushover/cyclic, vectorized
#set iFPush $iFj;				# lateral load for pushover, vectorized for each building (list)

#puts WeightTotal:$WeightTotal
#puts MassTotal:$MassTotal
#puts sumWiHi:$sumWiHi
#puts iFloorWeight:$iFloorWeight
#puts aFloorWeight:$aFloorWeight
#puts FloorHeight$FloorHeight
#puts FloorWeight$FloorWeight
#puts iFj$iFj
#puts iFPush$iFPush
#
#