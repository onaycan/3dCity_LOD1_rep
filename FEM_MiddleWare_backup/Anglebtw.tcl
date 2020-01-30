#
#  ANGLE BETWEEN BEAMS
# 
# Returns the angle in radians between beams, input: BEAM ID's
# Additionally, returns the angle in radians between vectors 'v1' and 'v2'
#
proc angle_btw_vec_from_EID {EID1 EID2 iBeamConnect iGirderConnect ifloornodes numInFile} {; # angle between beams/girders
	set v1 [EID_to_Vector $EID1 $iBeamConnect $iGirderConnect $ifloornodes $numInFile]
	set v2 [EID_to_Vector $EID2 $iBeamConnect $iGirderConnect $ifloornodes $numInFile]
	set theta [angle_btw_3 $v1 $v2]
	return $theta
}

proc EID_to_Vector {eltID iBeamConnect iGirderConnect ifloornodes numInFile} {; #Convert vectors from Element ID's
	set vector_from_eltID ""
	set checkbeam 0
	for {set i 0} {$i <= [expr [llength [lindex $iBeamConnect $numInFile]]-1]} {incr i 1} {
		if {$eltID == [lindex $iBeamConnect $numInFile $i 0]} {
			set beamnode1 [lindex $iBeamConnect $numInFile $i 1]
			set beamnode2 [lindex $iBeamConnect $numInFile $i 2]
			set checkbeam 1
		}
	}
	if {$checkbeam==1} {
		for {set i 0} {$i <= [expr [llength [lindex $ifloornodes $numInFile]]-1]} {incr i 1} {
			for {set j 0} {$j <= [expr [llength [lindex $ifloornodes $numInFile $i]]-1]} {incr j 1} {
				if {$beamnode1 == [lindex $ifloornodes $numInFile $i $j 0]} {
					set nodeI_X [lindex $ifloornodes $numInFile $i $j 1]
					set nodeI_Y [lindex $ifloornodes $numInFile $i $j 2]
					set nodeI_Z [lindex $ifloornodes $numInFile $i $j 3]
				} 
				if {$beamnode2 == [lindex $ifloornodes $numInFile $i $j 0]} {
					set nodeJ_X [lindex $ifloornodes $numInFile $i $j 1]
					set nodeJ_Y [lindex $ifloornodes $numInFile $i $j 2]
					set nodeJ_Z [lindex $ifloornodes $numInFile $i $j 3]
				}
			}
		}
		set vec_X [expr $nodeJ_X-$nodeI_X]
		set vec_Y [expr $nodeJ_Y-$nodeI_Y]
		set vec_Z [expr $nodeJ_Z-$nodeI_Z]
		lappend vector_from_eltID $vec_X
		lappend vector_from_eltID $vec_Y
		lappend vector_from_eltID $vec_Z
	}
	set checkgirder 0
	for {set i 0} {$i <= [expr [llength [lindex $iGirderConnect $numInFile]]-1]} {incr i 1} {
		if {$eltID == [lindex $iGirderConnect $numInFile $i 0]} {
			set girdernode1 [lindex $iGirderConnect $numInFile $i 1]
			set girdernode2 [lindex $iGirderConnect $numInFile $i 2]
			set checkgirder 1
		}
	}
	if {$checkgirder==1} {
		for {set i 0} {$i <= [expr [llength [lindex $ifloornodes $numInFile]]-1]} {incr i 1} {
			for {set j 0} {$j <= [expr [llength [lindex $ifloornodes $numInFile $i]]-1]} {incr j 1} {
				if {$girdernode1 == [lindex $ifloornodes $numInFile $i $j 0]} {
					set nodeI_X [lindex $ifloornodes $numInFile $i $j 1]
					set nodeI_Y [lindex $ifloornodes $numInFile $i $j 2]
					set nodeI_Z [lindex $ifloornodes $numInFile $i $j 3]
				} 
				if {$girdernode2 == [lindex $ifloornodes $numInFile $i $j 0]} {
					set nodeJ_X [lindex $ifloornodes $numInFile $i $j 1]
					set nodeJ_Y [lindex $ifloornodes $numInFile $i $j 2]
					set nodeJ_Z [lindex $ifloornodes $numInFile $i $j 3]
				}
			}
		}
		set vec_X [expr $nodeJ_X-$nodeI_X]
		set vec_Y [expr $nodeJ_Y-$nodeI_Y]
		set vec_Z [expr $nodeJ_Z-$nodeI_Z]
		lappend vector_from_eltID $vec_X
		lappend vector_from_eltID $vec_Y
		lappend vector_from_eltID $vec_Z
	}
	return $vector_from_eltID
}

proc norm_vector {vec} {
	set tmpnormvec [expr pow([lindex $vec 0],2)+pow([lindex $vec 1],2)+pow([lindex $vec 2],2)]
	set normvec [expr sqrt($tmpnormvec)]
	return $normvec
}

proc unit_vector {vec} {
	set normv [norm_vector $vec]
	set unitvec ""
	lappend unitvec [expr [lindex $vec 0]/$normv]
	lappend unitvec [expr [lindex $vec 0]/$normv]
	lappend unitvec [expr [lindex $vec 0]/$normv]
	return $unitvec
}
 
proc dotProduct {vect_A vect_B} {
    set product 0.0
	for {set i 0} {$i < 3} {incr i 1} {
		set product [expr $product + ([lindex $vect_A $i]*[lindex $vect_B $i])]
	}
    return $product
}  

proc crossProduct {vect_A vect_B} {
	set cross_P ""
    lappend cross_P [expr ([lindex $vect_A 1]*[lindex $vect_B 2])-([lindex $vect_A 2]*[lindex $vect_B 1])]
    lappend cross_P [expr ([lindex $vect_A 0]*[lindex $vect_B 2])-([lindex $vect_A 2]*[lindex $vect_B 0])]
    lappend cross_P [expr ([lindex $vect_A 0]*[lindex $vect_B 1])-([lindex $vect_A 1]*[lindex $vect_B 0])]
	return $cross_P
} 

proc angle_btw {v1 v2} {
    set n_v1 [norm_vector $v1]
	set n_v2 [norm_vector $v2]
	for {set i 0} {$i < 3} {incr i 1} {
		lset v1 $i [expr [lindex $v1 $i]/$n_v1]
		lset v2 $i [expr [lindex $v2 $i]/$n_v2]
	}
    set cosang [dotProduct $v1 $v2]
	set cross [crossProduct $v1 $v2]
    set sinang [norm_vector $cross]
	set atmp [expr $sinang/$cosang]
	return [expr { atan($atmp) }]
}

proc angle_btw_2 {v1 v2} {

# Returns the angle in radians between vectors 'v1' and 'v2'::
    set v1_u [unit_vector $v1]
    set v2_u [unit_vector $v2]
	set dotprod [dotProduct $v1_u $v2_u]
	if {$dotprod<=-1.0} {
		set dotprod -1.0
	} elseif {$dotprod>=1.0} {
		set dotprod 1.0
	}
	set result [expr {acos($dotprod)}]
	return $result
}

proc angle_btw_3 {v1 v2} {
    set n_v1 [norm_vector $v1]
	set n_v2 [norm_vector $v2]
	for {set i 0} {$i < 3} {incr i 1} {
		lset v1 $i [expr [lindex $v1 $i]/$n_v1]
		lset v2 $i [expr [lindex $v2 $i]/$n_v2]
	}
    set cosang [dotProduct $v1 $v2]
	set cross [crossProduct $v1 $v2]
    set sinang [norm_vector $cross]
	#set atmp [expr $sinang/$cosang]
	return [expr { atan2($sinang, $cosang) }]
}
#a = atan2d(x1*y2-y1*x2,x1*x2+y1*y2);

#
#