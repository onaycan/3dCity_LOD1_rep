#
#	START THE SIMULATION
#
# Read Input Parameters File first:
set filename "Paramaters_Input.txt"
source ReadParameters.tcl

while 1 {
	if {[string match $typesim "dynamic"] == 1} {
		puts "Dynamic Analysis has been selected..."
		puts ""
		set tclfilename "/"
		append tclfilename "Frame3D_analyze_Dynamic_EQ_bidirect.tcl"
		set tclfile2source ""
		append tclfile2source $tclfilesdir $tclfilename
		source $tclfile2source
        break
    } elseif {[string match $typesim "static"] == 1} {
		puts "Static Pushover Analysis has been selected..."
		puts ""
		set tclfilename "/"
		append tclfilename "Frame3D_analyze_Static_Pushover.tcl"
		set tclfile2source ""
		append tclfile2source $tclfilesdir $tclfilename
		source $tclfile2source		
        break
    }
}
