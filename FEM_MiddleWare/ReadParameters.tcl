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
			} elseif {[string match $line "#Output folder path:"] == 1} {
				set flag "outputfolderpath"
				continue
			} elseif {[string match $line "#Acceleration recording in lateral direction:"] == 1} {
				set flag "acceleration"
				continue
			} elseif {[string match $line "#Acceleration recording in perpendicular direction:"] == 1} {
				set flag "accelerationper"
				continue
			} elseif {[string match $line "#Simulation type: <Dynamic> or <Static> Pushover:"] == 1} {
				set flag "typesim"
				continue 
			} elseif {[string match $line "#Maximum duration for <Dynamic> simulation in seconds:"] == 1} {
				set flag "duration"
				continue 
			} elseif {[string match $line "#Time step dt in seconds:"] == 1} {
				set flag "timestep"
				continue 
			} elseif {[string match $line "#Number of modes in Modal Analysis:"] == 1} {
				set flag "modes"
				continue 
			} elseif {[string match $line "#RC Section"] == 1} {
				set flag "RCSection"
				continue 
			} elseif {[string match $line "#Square-Column section width in inches:"] == 1} {
				set flag "HCol"
				continue 
			} elseif {[string match $line "#Beam depth -- perpendicular to bending axis in inches:"] == 1} {
				set flag "HBeam"
				continue 
			} elseif {[string match $line "#Beam width -- parallel to bending axis in inches:"] == 1} {
				set flag "BBeam"
				continue 
			} elseif {[string match $line "#Girder depth -- perpendicular to bending axis in inches:"] == 1} {
				set flag "HGird"
				continue 
			} elseif {[string match $line "#Girder width -- parallel to bending axis in inches:"] == 1} {
				set flag "BGird"
				continue 
			} elseif {[string match $line "#W Section"] == 1} {
				set flag "WSection"
				continue 
			} elseif {[string match $line "#Live Loads (uniformly distributed) on each floor (furniture, etc.) in psf (pounds per square foot):"] == 1} {
				set flag "LiveLoad"
				continue 
			}
			if {[string match $flag "inputfolderpath"] == 1} {
				set inputFilepath $line
			} elseif {[string match $flag "outputfolderpath"] == 1} {
				set outputFilepath $line
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
			} elseif {$flag == "timestep"} {
				set DtAnalysis $line;	# time-step Dt for lateral analysis
			} elseif {$flag == "modes"} {
				set numModes $line; # decide the number of Modes in total for Modal Analysis
			} elseif {$flag == "RCSection"} {
				set RCSection $line; # decide the number of Modes in total for Modal Analysis
			} elseif {$flag == "HCol"} {
				set HCol $line
			} elseif {$flag == "HBeam"} {
				set HBeam $line
			} elseif {$flag == "BBeam"} {
				set BBeam $line
			} elseif {$flag == "HGird"} {
				set HGird $line
			} elseif {$flag == "BGird"} {
				set BGird $line
			} elseif {$flag == "WSection"} {
				set WSection $line
			} elseif {$flag == "LiveLoad"} {
				set LiveLoad $line
			}	
		}
	}
close $inFileID
}
#
#