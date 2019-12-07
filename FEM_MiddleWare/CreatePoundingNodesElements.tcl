# ------------------------------------------------------
#	CREATE POUNDING
#
#		ZeroLengthImpact3D elements
#		Additional Nodes into Model
#implementation of zeroLengthImpact3D with nodes in 3DOF domain:
# ------------------------------------------------------
#
#		Pounding Parameters:
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
#
set outFileforPoundingSTR CreatePoundingCommands.tcl
set outFileforPounding [open $outFileforPoundingSTR w]
#
#		READ first the POUNDING INPUT File
if [catch {open [lindex $PoundingInputFileList 0] r} inFileID] {
	puts stderr "Cannot open input file for reading Pounding related components"
} else {
  set flagnodes 0
  set flagconstraints 0
  set flagimpact 0
  set flagelements 0
	foreach line [split [read $inFileID] \n] {
		if {[llength $line] == 0} {
			# Blank line --> do nothing
			continue
		} 
		set flag 1
		foreach word [split $line] {
			if {[string match $word "#EXTRANODES"] == 1} {
				set flag 0
				set flagnodes 1
				set flagconstraints 0
				set flagimpact 0
				set flagelements 0				
				break
			} elseif {[string match $word "#CONSTRAINTS"] == 1} {
				set flag 0
				set flagnodes 0
				set flagconstraints 1
				set flagimpact 0
				set flagelements 0
				break
			} elseif {[string match $word "#ZEROLENGTHIMPACT"] == 1} {
				set flag 0
				set flagnodes 0
				set flagconstraints 0
				set flagimpact 1
				set flagelements 0
				break
			} elseif {[string match $word "#ZEROLENGTHELEMENTS"] == 1} {
				set flag 0
				set flagnodes 0
				set flagconstraints 0
				set flagimpact 0
				set flagelements 1
				break
			} elseif {[string match $word "#POUNDING"] == 1 || [string match $word "#END"] == 1} {
				set flag 0
				set flagnodes 0
				set flagconstraints 0
				set flagimpact 0
				set flagelements 0				
				break
			}
		}
		if {$flag == 1} {
			if {$flagnodes == 1} {
				set list [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
				set tags ""
				foreach tagstmp [split $list] {
					lappend tags $tagstmp
				}
				set nodeID [lindex $tags 0]
				set X [lindex $tags 1]
				set Y [lindex $tags 2]
				set Z [lindex $tags 3]
				set poundingstr "node	"
				append poundingstr $nodeID "	" $X "	" $Y "	" $Z
				lappend poundingnodeList $poundingstr
			} elseif {$flagconstraints == 1} {
				foreach word [split $line] {
					if {[string match $word "constraint"] == 1} {
						set list [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
						set tags ""
						foreach tagstmp [split $list] {
							lappend tags $tagstmp
						}
						set MNode [lindex $tags 0]
						set SNode [lindex $tags 1]
						set poundingstr "equalDOF	"
						append poundingstr $MNode "	" $SNode " 1 2 3"
						lappend poundingconstList $poundingstr
					}	
					break
				}
			} elseif {$flagimpact == 1} {
				foreach word [split $line] {
					if {[string match $word "impact"] == 1} {
						set list [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
						set tags ""
						foreach tagstmp [split $list] {
							lappend tags $tagstmp
						}
						set eltID [lindex $tags 0]
						set nodei [lindex $tags 1]
						set nodej [lindex $tags 2]
						set poundingstr "element zeroLengthImpact3D	"
						append poundingstr $eltID "	" $nodei "	" $nodej "	" $direction "	" $initGap "	" $frictionRatio "	" $Kt "	" $Kn "	" $Kn2 "	" $Delta_y "	" $cohesion
						lappend poundingimpactList $poundingstr
					}	
					break
				}
			} elseif {$flagelements == 1} {
				foreach word [split $line] {
					if {[string match $word "element"] == 1} {
						set list [regexp -all -inline -- {[-+]?[0-9]*\.?[0-9]+} $line]
						set tags ""
						foreach tagstmp [split $list] {
							lappend tags $tagstmp
						}
						set eltID [lindex $tags 0]
						set nodei [lindex $tags 1]
						set nodej [lindex $tags 2]
						# springs with very low stiffness for convergance of Newton-Raphson method 
						set poundingstr "element zeroLength	"
						append poundingstr $eltID "	" $nodei "	" $nodej " -mat 6 7 6 -dir 1 2 3"
						lappend poundingelementList $poundingstr
					}	
					break
				}
			}
		}
	}; #end of line read 
	close $inFileID
}
#
#
#	output to a file where the actual Opensees definitions are created:
#
set poundingstr "model BasicBuilder -ndm 3 -ndf 3"
puts $outFileforPounding $poundingstr
for {set i 0} {$i <= [expr [llength [lindex $poundingnodeList]]-1]} {incr i 1} {
	puts $outFileforPounding [lindex $poundingnodeList $i]
}
set poundingstr "model BasicBuilder -ndm 3 -ndf 6"
puts $outFileforPounding $poundingstr
for {set i 0} {$i <= [expr [llength [lindex $poundingconstList]]-1]} {incr i 1} {
	puts $outFileforPounding [lindex $poundingconstList $i]
}
for {set i 0} {$i <= [expr [llength [lindex $poundingimpactList]]-1]} {incr i 1} {
	puts $outFileforPounding [lindex $poundingimpactList $i]
}
set poundingstr "\nuniaxialMaterial Elastic 6 1.0e2\n"
append poundingstr "uniaxialMaterial Elastic 7 1.0e3"
puts $outFileforPounding $poundingstr
for {set i 0} {$i <= [expr [llength [lindex $poundingelementList]]-1]} {incr i 1} {
	puts $outFileforPounding [lindex $poundingelementList $i]
}
close $outFileforPounding
#