# --------------------------------------------------------------------------------------------------
#
# 				OUTPUTTING THE RESULTS
#
#
# -------------------------------------------------------------

set aBID [lindex $BID $numInFile 0]; # assign Building number
set _aBID "_Bid$aBID"
set underscore "_"
set _numIntgrPts_ "_$numIntgrPts$underscore"

set SupportNodeFirst [lindex $iSupportNode $numInFile 0];						# ID: first support node
set SupportNodeLast [lindex $iSupportNode $numInFile [expr [llength [lindex $iSupportNode $numInFile]]-1]];		# ID: last support node 
set MasterNodeFirst [lindex $iMasterNode $numInFile 0];						# ID: first master node
set MasterNodeLast [lindex $iMasterNode $numInFile [expr [llength [lindex $iMasterNode $numInFile]]-1]];			# ID: last master node

# ------------------------------- Ground Column IDs to output element RESULTs ------------------------------------------
	set GroundColumntmp2 ""
	for {set i 0} {$i <= [expr [llength [lindex $iSupportNode $numInFile]]-1]} {incr i 1} {
		for {set j 0} {$j <= [expr [llength [lindex $LCol $numInFile]]-1]} {incr j 1} {
			if {[lindex $iColumnConnect $numInFile $j 1] == [lindex $iSupportNode $numInFile $i]} {
				set GroundColumntmp [lindex $iColumnConnect $numInFile $j 0];	# Take the Ground Columns for outputing purposes 
			} elseif {[lindex $iColumnConnect $numInFile $j 2] == [lindex $iSupportNode $numInFile $i]} {
				set GroundColumntmp [lindex $iColumnConnect $numInFile $j 0];	# Take the Ground Columns for outputing purposes 
			}
		}
		lappend GroundColumntmp2 $GroundColumntmp
	}
	lappend GroundColumn $GroundColumntmp2

# ------------------------------- Floor Column IDs to output element RESULTs ------------------------------------------	
	set FloorColumntmp ""
	for {set i 0} {$i <= [expr [llength [lindex $LCol $numInFile]]-1]} {incr i 1} {
		lappend FloorColumntmp [lindex $iColumnConnect $numInFile $i 0]
	}
	lappend FloorColumn $FloorColumntmp

# ------------------------------- Floor Beam IDs to output element RESULTs ------------------------------------------
	set FloorBeamtmp ""
	for {set i 0} {$i <= [expr [llength [lindex $LBeam $numInFile]]-1]} {incr i 1} {
		lappend FloorBeamtmp [lindex $iBeamConnect $numInFile $i 0]
	}
	lappend FloorBeam $FloorBeamtmp

# ------------------------------- Floor Girder IDs to output element RESULTs ------------------------------------------	

	set FloorGirdertmp ""
	for {set i 0} {$i <= [expr [llength [lindex $LGird $numInFile]]-1]} {incr i 1} {
		lappend FloorGirdertmp [lindex $iGirderConnect $numInFile $i 0]
	}
	lappend FloorGirder $FloorGirdertmp
	
# set up name of data directory and create the folder
	set dispOutdir $dataDir/Building_$aBID/Displacements
	file mkdir "$dispOutdir"
	set reactOutdir $dataDir/Building_$aBID/Reactions
	file mkdir "$reactOutdir"
	set LdriftOutdir $dataDir/Building_$aBID/LateralDrifts
	file mkdir "$LdriftOutdir"
	set eleForcOutdir $dataDir/Building_$aBID/ElementForces
	file mkdir "$eleForcOutdir"
	set sectForcOutdir $dataDir/Building_$aBID/SectionForces
	file mkdir "$sectForcOutdir"
	set sectDefoOutdir $dataDir/Building_$aBID/SectionDeformations
	file mkdir "$sectDefoOutdir"
	set ssOutdir $dataDir/Building_$aBID/StressStrain
	file mkdir "$ssOutdir"
	
	recorder Node -file $dispOutdir/Disp_FreeNodes$_aBID.out -time -node [lindex $FreeNodeID $numInFile 0] -dof 1 2 3 disp; # displacements of free node
	recorder Node -file $dispOutdir/Disp_MasterNodes$_aBID.out -time -nodeRange $MasterNodeFirst $MasterNodeLast -dof 1 2 3 disp;# displacements of master nodes
	recorder Node -file $dispOutdir/Disp_BaseNodes$_aBID.out -time -nodeRange $SupportNodeFirst $SupportNodeLast -dof 1 2 3 disp;# displacements of support nodes
	recorder Node -file $reactOutdir/Reaction_BaseNodes$_aBID.out -time -nodeRange $SupportNodeFirst $SupportNodeLast -dof 1 2 3 reaction;	# support reaction
	recorder Drift -file $LdriftOutdir/DrNode_LateralDrift$_aBID.out -time -iNode $SupportNodeFirst  -jNode [lindex $FreeNodeID $numInFile 0] -dof 1 -perpDirn 2;	# lateral drift

# -------------------------------  Node RESULTs ------------------------------------------
for {set i 0} {$i <= [expr [llength [lindex $ifloornodes $numInFile]]-1]} {incr i 1} {
	for {set j 0} {$j <= [expr [llength [lindex $ifloornodes $numInFile $i]]-1]} {incr j 1} {
		set aNode [lindex $ifloornodes $numInFile $i $j 0]
		recorder Node -file $dispOutdir/Disp_Nodes_$aNode$_aBID.out -time -node $aNode -dof 1 2 3 disp;# displacements of floor nodes
	}
}
# ------------------------------- Ground Column element RESULTs ------------------------------------------
for {set i 0} {$i <= [expr [llength [lindex $iSupportNode $numInFile]]-1]} {incr i 1} {
	set aFirstColumn [lindex $GroundColumn $numInFile $i]
	recorder Element -file $eleForcOutdir/ForceEle_$aFirstColumn$_aBID.out -time -ele $aFirstColumn localForce;				# element forces in local coordinates
	recorder Element -file $sectForcOutdir/ForceEle_sec_1_$aFirstColumn$_aBID.out -time -ele $aFirstColumn section 1 force;	# section forces, axial and moment, node i
	recorder Element -file $sectDefoOutdir/DefoEle_sec_1_$aFirstColumn$_aBID.out -time -ele $aFirstColumn section 1 deformation;	# section deformations, axial and curvature, node i
	recorder Element -file $sectForcOutdir/ForceEle_sec$_numIntgrPts_$aFirstColumn$_aBID.out -time -ele $aFirstColumn section $numIntgrPts force;	# section forces, axial and moment, node j
	recorder Element -file $sectDefoOutdir/DefoEle_sec$_numIntgrPts_$aFirstColumn$_aBID.out -time -ele $aFirstColumn section $numIntgrPts deformation;# section deformations, axial and curvature, node j

	if {$RCSection=="True"} {
		set yFiber [expr $HCol/2-$cover];		# fiber location for stress-strain recorder, local coords
		set zFiber [expr $BCol/2-$cover];		# fiber location for stress-strain recorder, local coords
		recorder Element -file $ssOutdir/StressStrain_concEle_sec_1_$aFirstColumn$_aBID.out -time -ele $aFirstColumn section $numIntgrPts fiber $yFiber $zFiber $IDconcCore  stressStrain;	# Core Concrete stress-strain, node i
		recorder Element -file $ssOutdir/StressStrain_reinfEle_sec_1_$aFirstColumn$_aBID.out -time -ele $aFirstColumn section $numIntgrPts fiber $yFiber $zFiber $IDSteel  stressStrain;	# steel fiber stress-strain, node i
	}
	if {$WSection=="True"} {
		set yFiber [expr 0.];								# fiber location for stress-strain recorder, local coords
		set zFiber [expr 0.];								# fiber location for stress-strain recorder, local coords
		recorder Element -file $ssOutdir/StressStrain_reinfEle_sec_1_$aFirstColumn$_aBID.out -time -ele $aFirstColumn section $numIntgrPts fiber $yFiber $zFiber stressStrain;	# steel fiber stress-strain, node i
	}
}

# -------------------------------  Column element RESULTs ------------------------------------------
for {set i 0} {$i <= [expr [llength [lindex $FloorColumn $numInFile]]-1]} {incr i 1} {
	set anElement [lindex $FloorColumn $numInFile $i]
	recorder Element -file $eleForcOutdir/ForceEle_$anElement$_aBID.out -time -ele $anElement localForce;				# element forces in local coordinates
	recorder Element -file $sectForcOutdir/ForceEle_sec_1_$anElement$_aBID.out -time -ele $anElement section 1 force;	# section forces, axial and moment, node i
	recorder Element -file $sectDefoOutdir/DefoEle_sec_1_$anElement$_aBID.out -time -ele $anElement section 1 deformation;	# section deformations, axial and curvature, node i
	recorder Element -file $sectForcOutdir/ForceEle_sec$_numIntgrPts_$anElement$_aBID.out -time -ele $anElement section $numIntgrPts force;	# section forces, axial and moment, node j
	recorder Element -file $sectDefoOutdir/DefoEle_sec$_numIntgrPts_$anElement$_aBID.out -time -ele $anElement section $numIntgrPts deformation;# section deformations, axial and curvature, node j

	if {$RCSection=="True"} {
		set yFiber [expr $HCol/2-$cover];		# fiber location for stress-strain recorder, local coords
		set zFiber [expr $BCol/2-$cover];		# fiber location for stress-strain recorder, local coords
		recorder Element -file $ssOutdir/StressStrain_concEle_sec_1_$anElement$_aBID.out -time -ele $anElement section $numIntgrPts fiber $yFiber $zFiber $IDconcCore  stressStrain;	# Core Concrete stress-strain, node i
		recorder Element -file $ssOutdir/StressStrain_reinfEle_sec_1_$anElement$_aBID.out -time -ele $anElement section $numIntgrPts fiber $yFiber $zFiber $IDSteel  stressStrain;	# steel fiber stress-strain, node i
	}
	if {$WSection=="True"} {
		set yFiber [expr 0.];								# fiber location for stress-strain recorder, local coords
		set zFiber [expr 0.];								# fiber location for stress-strain recorder, local coords
		recorder Element -file $ssOutdir/StressStrain_reinfEle_sec_1_$anElement$_aBID.out -time -ele $anElement section $numIntgrPts fiber $yFiber $zFiber stressStrain;	# steel fiber stress-strain, node i
	}
}

# -------------------------------  Beam element RESULTs ------------------------------------------	
for {set i 0} {$i <= [expr [llength [lindex $FloorBeam $numInFile]]-1]} {incr i 1} {
	set anElement [lindex $FloorBeam $numInFile $i]
	recorder Element -file $eleForcOutdir/ForceEle_$anElement$_aBID.out -time -ele $anElement localForce;				# element forces in local coordinates
	recorder Element -file $sectForcOutdir/ForceEle_sec_1_$anElement$_aBID.out -time -ele $anElement section 1 force;	# section forces, axial and moment, node i
	recorder Element -file $sectDefoOutdir/DefoEle_sec_1_$anElement$_aBID.out -time -ele $anElement section 1 deformation;	# section deformations, axial and curvature, node i
	recorder Element -file $sectForcOutdir/ForceEle_sec$_numIntgrPts_$anElement$_aBID.out -time -ele $anElement section $numIntgrPts force;	# section forces, axial and moment, node j
	recorder Element -file $sectDefoOutdir/DefoEle_sec$_numIntgrPts_$anElement$_aBID.out -time -ele $anElement section $numIntgrPts deformation;# section deformations, axial and curvature, node j

	if {$RCSection=="True"} {
		set yFiber [expr $HCol/2-$cover];		# fiber location for stress-strain recorder, local coords
		set zFiber [expr $BCol/2-$cover];		# fiber location for stress-strain recorder, local coords
		recorder Element -file $ssOutdir/StressStrain_concEle_sec_1_$anElement$_aBID.out -time -ele $anElement section $numIntgrPts fiber $yFiber $zFiber $IDconcCore  stressStrain;	# Core Concrete stress-strain, node i
		recorder Element -file $ssOutdir/StressStrain_reinfEle_sec_1_$anElement$_aBID.out -time -ele $anElement section $numIntgrPts fiber $yFiber $zFiber $IDSteel  stressStrain;	# steel fiber stress-strain, node i
	}
	if {$WSection=="True"} {
		set yFiber [expr 0.];								# fiber location for stress-strain recorder, local coords
		set zFiber [expr 0.];								# fiber location for stress-strain recorder, local coords
		recorder Element -file $ssOutdir/StressStrain_reinfEle_sec_1_$anElement$_aBID.out -time -ele $anElement section $numIntgrPts fiber $yFiber $zFiber stressStrain;	# steel fiber stress-strain, node i
	}
}

# -------------------------------  Girder element RESULTs ------------------------------------------	
for {set i 0} {$i <= [expr [llength [lindex $FloorGirder $numInFile]]-1]} {incr i 1} {
	set anElement [lindex $FloorGirder $numInFile $i]
	recorder Element -file $eleForcOutdir/ForceEle_$anElement$_aBID.out -time -ele $anElement localForce;				# element forces in local coordinates
	recorder Element -file $sectForcOutdir/ForceEle_sec_1_$anElement$_aBID.out -time -ele $anElement section 1 force;	# section forces, axial and moment, node i
	recorder Element -file $sectDefoOutdir/DefoEle_sec_1_$anElement$_aBID.out -time -ele $anElement section 1 deformation;	# section deformations, axial and curvature, node i
	recorder Element -file $sectForcOutdir/ForceEle_sec$_numIntgrPts_$anElement$_aBID.out -time -ele $anElement section $numIntgrPts force;	# section forces, axial and moment, node j
	recorder Element -file $sectDefoOutdir/DefoEle_sec$_numIntgrPts_$anElement$_aBID.out -time -ele $anElement section $numIntgrPts deformation;# section deformations, axial and curvature, node j

	if {$RCSection=="True"} {
		set yFiber [expr $HCol/2-$cover];		# fiber location for stress-strain recorder, local coords
		set zFiber [expr $BCol/2-$cover];		# fiber location for stress-strain recorder, local coords
		recorder Element -file $ssOutdir/StressStrain_concEle_sec_1_$anElement$_aBID.out -time -ele $anElement section $numIntgrPts fiber $yFiber $zFiber $IDconcCore  stressStrain;	# Core Concrete stress-strain, node i
		recorder Element -file $ssOutdir/StressStrain_reinfEle_sec_1_$anElement$_aBID.out -time -ele $anElement section $numIntgrPts fiber $yFiber $zFiber $IDSteel  stressStrain;	# steel fiber stress-strain, node i
	}
	if {$WSection=="True"} {
		set yFiber [expr 0.];								# fiber location for stress-strain recorder, local coords
		set zFiber [expr 0.];								# fiber location for stress-strain recorder, local coords
		recorder Element -file $ssOutdir/StressStrain_reinfEle_sec_1_$anElement$_aBID.out -time -ele $anElement section $numIntgrPts fiber $yFiber $zFiber stressStrain;	# steel fiber stress-strain, node i
	}
}
#recorder Element -file $eleForcOutdir/ForceEletest_220020101.out -time -ele 220020101 localForce;				# element forces in local coordinates
# Plot displacements -------------------------------------------------------------
recorder plot $dispOutdir/Disp_FreeNodes$_aBID.out DisplDOF[lindex $iGMdirection 0] 1100 10 400 400 -columns  1 [expr 1+[lindex $iGMdirection 0]] ; # a window to plot the nodal displacements versus time
recorder plot $dispOutdir/Disp_FreeNodes$_aBID.out DisplDOF[lindex $iGMdirection 1] 1100 410 400 400 -columns 1 [expr 1+[lindex $iGMdirection 1]] ; # a window to plot the nodal displacements versus time
#
#