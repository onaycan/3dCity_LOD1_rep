#
#	Read input parameters from the file
#
#
set filename "Paramaters_Input.txt"
#
set flag ""
if [catch {open $filename r} inFileID] {
    puts stderr "Cannot open input parameters file"
} else {
	foreach line [split [read $inFileID] \n] {
        if {[llength $line] == 0} {
        # Blank line --> do nothing
			continue
        } else {
			if {[string match $line "#Input folder path:"] == 1} {
				set flag "inputfolderpath"
				continue
			} elseif {[string match $line "#Acceleration recording in lateral direction:"] == 1} {
				set flag "acceleration"
				continue
			} elseif {[string match $line "#Acceleration recording in perpendicular direction:"] == 1} {
				set flag "accelerationper"
				continue
			} elseif {[string match $line "#Simulation type: Dynamic or Static Pushover:"] == 1} {
				set flag "typesim"
				continue 
			} elseif {[string match $line "#Maximum duration for simulation in seconds:"] == 1} {
				set flag "duration"
				continue 
			} elseif {[string match $line "#Number of modes in Modal Analysis:"] == 1} {
				set flag "modes"
				continue 
			} 
			if {[string match $flag "inputfolderpath"] == 1} {
				set inputFoldername [lrange [file split $line] end end]
				set inputFilepath $line
			} elseif {$flag == "acceleration"} {
				set accfolder [lrange [file split $line] end-1 end-1]
				set GMdir $accfolder;		# ground-motion file directory
				set acc1 [lrange [file split $line] end end]
				set acc1 [split $acc1 "."];  # extract the filename without its extension
				set acc1 [lindex $acc1 0]
			} elseif {$flag == "accelerationper"} {
			#set iGMfile "H-E01140 H-E12140" ;		# ground-motion filenames, should be different files
				set acc2 [lrange [file split $line] end end]
				set acc2 [split $acc2 "."];  # extract the filename without its extension
				set acc2 [lindex $acc2 0]
				set iGMfile "$acc2 $acc1" ;		# ground-motion filenames, should be different files
			} elseif {$flag == "typesim"} {
				set typesim $line; 		# Dynamic/Pushover etc.
			} elseif {$flag == "duration"} {
				set TmaxAnalysis $line;	# maximum duration of ground-motion analysis 
			} elseif {$flag == "modes"} {
				set numModes $line; # decide the number of Modes in total for Modal Analysis
			}			
		}
	}
close $inFileID
}
#
#