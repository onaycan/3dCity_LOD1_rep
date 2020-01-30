#
#	Finds the tcl files inside the folder and its subfolders
# 	The number of tcl files gives the number of buildings
#
#set contents [glob -directory  $InputDir "*.tcl"]
set FileExt ".tcl"
set ainputFilename [findFiles $InputDir "INPUT_*"]
set Buildingnum [llength $ainputFilename]

foreach item $ainputFilename {
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
}

set PoundingInputFileList [findFiles $InputDir "POUNDING_*"]; # additional files for Pounding 