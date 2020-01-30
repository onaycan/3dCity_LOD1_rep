#
#	Read input parameters from the file
#
#
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
			if {[string match $line "#Tcl files directory:"] == 1} {
				set flag "tclfilesdir"
				continue
			} elseif {[string match $line "#Input folder path:"] == 1} {
				set flag "inputfolderpath"
				continue
			} elseif {[string match $line "#Output folder path:"] == 1} {
				set flag "outputfolderpath"
				continue
			} elseif {[string match $line "#Unit system <Metric> <US>"] == 1} {
				set flag "unitsystem"
				continue
			} elseif {[string match $line "#Acceleration recording in lateral direction 1:"] == 1} {
				set flag "accelerationlat1"
				continue
			}  elseif {[string match $line "#Acceleration recording in lateral direction 2:"] == 1} {
				set flag "accelerationlat2"
				continue
			} elseif {[string match $line "#Acceleration recording in perpendicular direction:"] == 1} {
				set flag "accelerationper"
				continue
			} elseif {[string match $line "#Ground motion scaling factor:"] == 1} {
				set flag "scalingfactor"
				continue 
			} elseif {[string match $line "#Simulation type: <Dynamic> or <Static>:"] == 1} {
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
			if {[string match $flag "tclfilesdir"] == 1} {
				set tclfilesdir $line
			} elseif {[string match $flag "inputfolderpath"] == 1} {
				set inputFilepath $line
			} elseif {[string match $flag "outputfolderpath"] == 1} {
				set outputFilepath $line
			} elseif {[string match $flag "unitsystem"] == 1} {
				set unitsystem $line
				set unitsystem [string tolower $unitsystem]
			} elseif {$flag == "accelerationlat1"} {
				set acc1 [lrange [file split $line] end end]
				set acc1 [file rootname $acc1];  # extract the filename without its extension
			}  elseif {$flag == "accelerationlat2"} {
				set acc2 [lrange [file split $line] end end]
				set acc2 [file rootname $acc2];  # extract the filename without its extension
			} elseif {$flag == "accelerationper"} {
				set GMdir [file dirname $line]; # ground-motion file directory
				set acc3 [lrange [file split $line] end end]
				set acc3 [file rootname $acc3];  # extract the filename without its extension
				set iGMfile "$acc1 $acc3 $acc2" ;		# ground-motion filenames, should be different files
			} elseif {$flag == "scalingfactor"} {
				set GMSF $line; # scaling factor for Ground motions depending on spectra
			} elseif {$flag == "typesim"} {
				set typesim $line; 		# Dynamic/Pushover etc.
				set typesim [string tolower $typesim]
			} elseif {$flag == "duration"} {
				set TmaxAnalysis $line;	# maximum duration of ground-motion analysis 
			} elseif {$flag == "timestep"} {
				set DtAnalysis $line;	# time-step Dt for lateral analysis
			} elseif {$flag == "modes"} {
				set numModes $line; # decide the number of Modes in total for Modal Analysis
			} elseif {$flag == "RCSection"} {
				set RCSection $line; # decide the number of Modes in total for Modal Analysis
				set RCSection [string tolower $RCSection]
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
				set WSection [string tolower $WSection]
			} elseif {$flag == "LiveLoad"} {
				set LiveLoad $line
			}	
		}
	}
close $inFileID
}
#
# ######################################################################
#
set filename ""
append filename $tclfilesdir "/ParamatersFEM_Input.txt"
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
			if {[string match $line "#Display Model"] == 1} {
				set flag "displaymodel"
				continue
			} elseif {[string match $line "#Display recorder plot"] == 1} {
				set flag "displayrecorder"
				continue
			} elseif {[string match $line "#Pounding Type <zeroLengthImpact3D>  <zeroLengthContact3D>  <None>:"] == 1} {
				set flag "poundingtype"
				continue
			} elseif {[string match $line "#Direction of normal of contact surface"] == 1} {
				set flag "direction"
				continue
			} elseif {[string match $line "#Friction coefficient mu:"] == 1} {
				set flag "mu"
				continue
			} elseif {[string match $line "#Penalty stiffness for tangential directions Kt:"] == 1} {
				set flag "kt"
				continue
			} elseif {[string match $line "#Penalty stiffness for normal direction Kn:"] == 1} {
				set flag "kn"
				continue 
			} elseif {[string match $line "#Cohesion:"] == 1} {
				set flag "cohesion"
				continue 
			} elseif {[string match $line "#Initial gap:"] == 1} {
				set flag "initialgap"
				continue 
			} elseif {[string match $line "#Friction ratio:"] == 1} {
				set flag "frictionratio"
				continue 
			} elseif {[string match $line "#Yield displacement based on Hertz impact model:"] == 1} {
				set flag "yielddisp"
				continue 
			} elseif {[string match $line "#Spring element (zeroLength) stiffness:"] == 1} {
				set flag "stiffness"
				continue 
			} 
			if {[string match $flag "displaymodel"] == 1} {
				set displaymodel $line
				set displaymodel [string tolower $displaymodel]
			} elseif {[string match $flag "displayrecorder"] == 1} {
				set displayrecorder $line
				set displayrecorder [string tolower $displayrecorder]
			} elseif {[string match $flag "poundingtype"] == 1} {
				set poundingtype $line
			} elseif {[string match $flag "direction"] == 1} {
				set direction $line
			} elseif {$flag == "mu"} {
				set mu $line
			} elseif {$flag == "kt"} {
				set Kt $line
			} elseif {$flag == "kn"} {
				set Kn $line
			} elseif {$flag == "cohesion"} {
				set cohesion $line 
			} elseif {$flag == "initialgap"} {
				set initGap $line
			} elseif {$flag == "frictionratio"} {
				set frictionRatio $line
			} elseif {$flag == "yielddisp"} {
				set Delta_y $line
			} elseif {$flag == "stiffness"} {
				set stiffness $line
			}	
		}
	}
close $inFileID
}
#
#