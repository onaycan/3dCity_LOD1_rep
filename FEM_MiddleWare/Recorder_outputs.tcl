# --------------------------------------------------------------------------------------------------
#
# 				OUTPUTTING THE RESULTS
#
#
# -------------------------------------------------------------
set outFileforRecorderSTR CreateRecorderCommands.tcl
set outFileforRecorder [open $outFileforRecorderSTR w]
#set outFileNodeIDName $dataDir/NodeIDs.out
#set outFileEltIDName $dataDir/ElementIDs.out
#set outFileBeamEltIDName $dataDir/BeamElementIDs.out
#set outFileGirderEltIDName $dataDir/GirderElementIDs.out
#set outFileColumnEltIDName $dataDir/ColumnElementIDs.out

set _numIntgrPts "_$numIntgrPts"

set AllnodesFirst [lindex $iNodeList 0 0 0]
set AllnodesLast [lindex $iNodeList [expr $Buildingnum-1] [expr [llength [lindex $iNodeList [expr $Buildingnum-1]]]-1] 0]

set AllEltFirst [lindex $ElementwColumns 0 0 0]
set AllEltLast [lindex $ElementwColumns [expr $Buildingnum-1] [expr [llength [lindex $ElementwColumns [expr $Buildingnum-1]]]-1] 0]

set AllBeamsFirst [lindex $iBeamConnect 0 0 0]
set AllBeamsLast [lindex $iBeamConnect [expr $Buildingnum-1] [expr [llength [lindex $iBeamConnect [expr $Buildingnum-1]]]-1] 0]
set AllGirdersFirst [lindex $iGirderConnect 0 0 0]
set AllGirdersLast [lindex $iGirderConnect [expr $Buildingnum-1] [expr [llength [lindex $iGirderConnect [expr $Buildingnum-1]]]-1] 0]
set AllColumnsFirst [lindex $iColumnConnect 0 0 0]
set AllColumnsLast [lindex $iColumnConnect [expr $Buildingnum-1] [expr [llength [lindex $iColumnConnect [expr $Buildingnum-1]]]-1] 0]

# -------------------------------  Lateral Drift RESULTs ------------------------------------------
for {set numInFile 0} {$numInFile <= [expr $Buildingnum-1]} {incr numInFile 1} {
	set aBID [lindex $BID $numInFile 0]; # assign Building number
	set _aBID "_Building_$aBID"
	set SupportNodeFirst [lindex $iSupportNode $numInFile 0];						# ID: first support node
	recorder Drift -file $dataDir/LateralDrift$_aBID.out -time -iNode $SupportNodeFirst  -jNode [lindex $FreeNodeID $numInFile 0] -dof 1 -perpDirn 2;	# lateral drift
}
#For displaying purpose:
#recorder Node -file $dataDir/Disp_FreeNodes.out -time -node [lindex $FreeNodeID $numInFile 0] -dof 1 2 3 disp; # displacements of free node

# -------------------------------  Node RESULTs ------------------------------------------
	set infileNodeIDName [open $dataDir/NodeIDs.out r]
	set str ""
	while { [gets $infileNodeIDName line] >= 0 } {
		append str $line " "
	}
	close $infileNodeIDName
#	
set tmpoutDataDir $dataDir/Displacement_AllNodes.out
	set recorderstr "recorder Node -file $tmpoutDataDir -time -node ";	# displacements of All Nodes
	set arg "-dof 1 2 3 disp"
	append recorderstr $str$arg
	puts $outFileforRecorder $recorderstr
#
if {$typesim=="Dynamic"} {
for { set k 1 } { $k <= $numModes } { incr k } {
	set tmpoutDataDir [format "$dataDir/mode%i_AllNodes.out" $k]
		set recorderstr "recorder Node -file $tmpoutDataDir -node ";	# displacements of All Nodes
		set arg "-dof 1 2 3 "
		append recorderstr $str$arg"eigen $k"
		puts $outFileforRecorder $recorderstr
	#
}
}
#recorder Node -file $dataDir/Displacement_AllNodes.out -time -nodeRange $AllnodesFirst $AllnodesLast -dof 1 2 3 disp;# displacements of All Nodes

# -------------------------------  Element RESULTs ------------------------------------------
	set infileEltIDName [open $dataDir/ElementIDs.out r]
	set str ""
	while { [gets $infileEltIDName line] >= 0 } {
		append str $line " "
	}
	close $infileEltIDName
#	
set tmpoutDataDir $dataDir/Force_AllElements.out
	set recorderstr "recorder Element -file $tmpoutDataDir -time -ele ";	# element forces in local coordinates
	set arg "localForce"
	append recorderstr $str$arg
	puts $outFileforRecorder $recorderstr
#
set tmpoutDataDir $dataDir/Force_AllElements_sec_1.out
	set recorderstr "recorder Element -file $tmpoutDataDir -time -ele ";	# section forces, axial and moment, node i
	set arg "section 1 force"
	append recorderstr $str$arg
	puts $outFileforRecorder $recorderstr
#
set tmpoutDataDir $dataDir/Deformation_AllElements_sec_1.out
	set recorderstr "recorder Element -file $tmpoutDataDir -time -ele ";	# section deformations, axial and curvature, node i
	set arg "section 1 deformation"
	append recorderstr $str$arg
	puts $outFileforRecorder $recorderstr
#
set tmpoutDataDir $dataDir/Force_AllElements_sec$_numIntgrPts.out
	set recorderstr "recorder Element -file $tmpoutDataDir -time -ele ";	# section forces, axial and moment, node j
	set arg "section $numIntgrPts force"
	append recorderstr $str$arg
	puts $outFileforRecorder $recorderstr
#
set tmpoutDataDir $dataDir/Deformation_AllElements_sec$_numIntgrPts.out
	set recorderstr "recorder Element -file $tmpoutDataDir -time -ele ";	# section deformations, axial and curvature, node j
	set arg "section $numIntgrPts deformation"
	append recorderstr $str$arg
	puts $outFileforRecorder $recorderstr
#recorder Element -file $dataDir/Force_AllGirderElements.out -time -ele $AllGirdersFirst $AllGirdersLast localForce;				# element forces in local coordinates
#recorder Element -file $dataDir/Force_AllGirderElements_sec_1.out -time -ele $AllGirdersFirst $AllGirdersLast section 1 force;	# section forces, axial and moment, node i
#recorder Element -file $dataDir/Deformation_AllGirderElements_sec_1.out -time -ele $AllGirdersFirst $AllGirdersLast section 1 deformation;	# section deformations, axial and curvature, node i
#recorder Element -file $dataDir/Force_AllGirderElements_sec$_numIntgrPts.out -time -ele $AllGirdersFirst $AllGirdersLast section $numIntgrPts force;	# section forces, axial and moment, node j
#recorder Element -file $dataDir/Deformation_AllGirderElements_sec$_numIntgrPts.out -time -ele $AllGirdersFirst $AllGirdersLast section $numIntgrPts deformation;# section deformations, axial and curvature, node j

#recorder Element -file $dataDir/Force_AllColumnElements.out -time -ele $AllColumnsFirst $AllColumnsLast localForce;				# element forces in local coordinates
#recorder Element -file $dataDir/Force_AllColumnElements_sec_1.out -time -ele $AllColumnsFirst $AllColumnsLast section 1 force;	# section forces, axial and moment, node i
#recorder Element -file $dataDir/Deformation_AllColumnElements_sec_1.out -time -ele $AllColumnsFirst $AllColumnsLast section 1 deformation;	# section deformations, axial and curvature, node i
#recorder Element -file $dataDir/Force_AllColumnElements_sec$_numIntgrPts.out -time -ele $AllColumnsFirst $AllColumnsLast section $numIntgrPts force;	# section forces, axial and moment, node j
#recorder Element -file $dataDir/Deformation_AllColumnElements_sec$_numIntgrPts.out -time -ele $AllColumnsFirst $AllColumnsLast section $numIntgrPts deformation;# section deformations, axial and curvature, node j
if {$RCSection=="True"} {
	set yFiber [expr $HBeam/2-$cover];		# fiber location for stress-strain recorder, local coords
	set zFiber [expr $BBeam/2-$cover];		# fiber location for stress-strain recorder, local coords

	set infileBeamEltIDName [open $dataDir/BeamElementIDs.out r]
	set strbeam ""
	while { [gets $infileBeamEltIDName line] >= 0 } {
		append strbeam $line " "
	}
	close $infileBeamEltIDName
	#
	set tmpoutDataDir $dataDir/StressStrain_AllBeamElements_concEle_sec_1.out
		set recorderstr "recorder Element -file $tmpoutDataDir -time -ele ";	# Core Concrete stress-strain, node i
		set arg "section $numIntgrPts fiber $yFiber $zFiber $IDconcCore  stressStrain"
		append recorderstr $strbeam$arg
		puts $outFileforRecorder $recorderstr
	#
	set tmpoutDataDir $dataDir/StressStrain_AllBeamElements_reinfEle_sec_1.out
		set recorderstr "recorder Element -file $tmpoutDataDir -time -ele ";	# steel fiber stress-strain, node i
		set arg "section $numIntgrPts fiber $yFiber $zFiber $IDSteel  stressStrain"
		append recorderstr $strbeam$arg
		puts $outFileforRecorder $recorderstr
#
#	
	set yFiber [expr $HGird/2-$cover];		# fiber location for stress-strain recorder, local coords
	set zFiber [expr $BGird/2-$cover];		# fiber location for stress-strain recorder, local coords
	
	set infileGirderEltIDName [open $dataDir/GirderElementIDs.out r]
	set strgird ""
	while { [gets $infileGirderEltIDName line] >= 0 } {
		append strgird $line " "
	}
	close $infileGirderEltIDName
	#
	set tmpoutDataDir $dataDir/StressStrain_AllGirderElements_concEle_sec_1.out
		set recorderstr "recorder Element -file $tmpoutDataDir -time -ele ";	# Core Concrete stress-strain, node i
		set arg "section $numIntgrPts fiber $yFiber $zFiber $IDconcCore  stressStrain"
		append recorderstr $strgird$arg
		puts $outFileforRecorder $recorderstr
	#
	set tmpoutDataDir $dataDir/StressStrain_AllGirderElements_reinfEle_sec_1.out
		set recorderstr "recorder Element -file $tmpoutDataDir -time -ele ";	# steel fiber stress-strain, node i
		set arg "section $numIntgrPts fiber $yFiber $zFiber $IDSteel  stressStrain"
		append recorderstr $strgird$arg
		puts $outFileforRecorder $recorderstr	
#
#
	set yFiber [expr $HCol/2-$cover];		# fiber location for stress-strain recorder, local coords
	set zFiber [expr $BCol/2-$cover];		# fiber location for stress-strain recorder, local coords
	
	set infileColumnEltIDName [open $dataDir/ColumnElementIDs.out r]
	set strcol ""
	while { [gets $infileColumnEltIDName line] >= 0 } {
		append strcol $line " "
	}
	close $infileColumnEltIDName
	#
	set tmpoutDataDir $dataDir/StressStrain_AllColumnElements_concEle_sec_1.out
		set recorderstr "recorder Element -file $tmpoutDataDir -time -ele ";	# Core Concrete stress-strain, node i
		set arg "section $numIntgrPts fiber $yFiber $zFiber $IDconcCore  stressStrain"
		append recorderstr $strcol$arg
		puts $outFileforRecorder $recorderstr
	#
	set tmpoutDataDir $dataDir/StressStrain_AllColumnElements_reinfEle_sec_1.out
		set recorderstr "recorder Element -file $tmpoutDataDir -time -ele ";	# steel fiber stress-strain, node i
		set arg "section $numIntgrPts fiber $yFiber $zFiber $IDSteel  stressStrain"
		append recorderstr $strcol$arg
		puts $outFileforRecorder $recorderstr
		
#	recorder Element -file $dataDir/StressStrain_AllGirderElements_concEle_sec_1.out -time -eleRange $AllGirdersFirst $AllGirdersLast section $numIntgrPts fiber $yFiber $zFiber $IDconcCore  stressStrain;	# Core Concrete stress-strain, node i
#	recorder Element -file $dataDir/StressStrain_AllGirderElements_reinfEle_sec_1.out -time -eleRange $AllGirdersFirst $AllGirdersLast section $numIntgrPts fiber $yFiber $zFiber $IDSteel  stressStrain;	# steel fiber stress-strain, node i
#	recorder Element -file $dataDir/StressStrain_AllColumnElements_concEle_sec_1.out -time -eleRange $AllColumnsFirst $AllColumnsLast section $numIntgrPts fiber $yFiber $zFiber $IDconcCore  stressStrain;	# Core Concrete stress-strain, node i
#	recorder Element -file $dataDir/StressStrain_AllColumnElements_reinfEle_sec_1.out -time -eleRange $AllColumnsFirst $AllColumnsLast section $numIntgrPts fiber $yFiber $zFiber $IDSteel  stressStrain;	# steel fiber stress-strain, node i
}
if {$WSection=="True"} {
	set yFiber [expr 0.];								# fiber location for stress-strain recorder, local coords
	set zFiber [expr 0.];								# fiber location for stress-strain recorder, local coords

	#
	set tmpoutDataDir $dataDir/StressStrain_AllElements_reinfEle_sec_1.out
		set recorderstr "recorder Element -file $tmpoutDataDir -time -ele ";	# steel fiber stress-strain, node i
		set arg "section $numIntgrPts fiber $yFiber $zFiber stressStrain"
		append recorderstr $str$arg
		puts $outFileforRecorder $recorderstr
#	recorder Element -file $dataDir/StressStrain_AllGirderElements_reinfEle_sec_1.out -time -eleRange $AllGirdersFirst $AllGirdersLast section $numIntgrPts fiber $yFiber $zFiber stressStrain;	# steel fiber stress-strain, node i
#	recorder Element -file $dataDir/StressStrain_AllColumnElements_reinfEle_sec_1.out -time -eleRange $AllColumnsFirst $AllColumnsLast section $numIntgrPts fiber $yFiber $zFiber stressStrain;	# steel fiber stress-strain, node i
}
#
close $outFileforRecorder
source $outFileforRecorderSTR
#