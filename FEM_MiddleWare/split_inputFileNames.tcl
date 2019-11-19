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