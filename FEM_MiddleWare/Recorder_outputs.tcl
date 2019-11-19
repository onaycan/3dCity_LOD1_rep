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
			if {[lindex $iColumnConnect $numInFile $j 1] == [lindex $iSupportNode $numInFile $i]} {
				set FirstColumntmp [lindex $iColumnConnect $numInFile $j 0];	# Take the Ground Columns for outputing purposes 
			} elseif {[lindex $iColumnConnect $numInFile $j 2] == [lindex $iSupportNode $numInFile $i]} {
				set FirstColumntmp [lindex $iColumnConnect $numInFile $j 0];	# Take the Ground Columns for outputing purposes 
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