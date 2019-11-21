#
#	Finds the tcl files inside the folder
# 	The number of tcl files gives the number of buildings
#	Every folder has a block of buildings, or a single building
#	Assumed input file names are like "xxx_123.tcl"
#	where xxx and 123 are seperated by "_"
#	and the file has an extension ".tcl"  (FileExt is a string storing ".tcl" defined in the main part of the code)
#
set contents [glob -directory  $InputDir "*.tcl"]

foreach item $contents {
    lappend pathname $item
}
foreach ff $pathname {
    #set ff [split $ff "/"]
    lappend Filename [lrange [file split $ff] end end]
}
foreach ll $Filename {
    set ll [split $ll "_"]
    lappend infiles [lindex $ll 1]
}
foreach kk $infiles {
    set kk [split $kk $FileExt]
	set iFID [lindex $kk 0]
    lappend FID $iFID;	# File ID
	lappend ainputFilename $inputFilename$iFID$FileExt
	set Buildingnum [expr $Buildingnum+1]
}