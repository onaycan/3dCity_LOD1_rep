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
