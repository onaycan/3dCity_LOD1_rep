#
#	START THE SIMULATION
#
# Read Input Parameters File first:
source ReadParameters.tcl


while 1 {
	if {[string match $typesim "Dynamic"] == 1} {
		puts "Dynamic Analysis has been selected..."
		puts ""
		source Frame3D_analyze_Dynamic_EQ_bidirect.tcl
        break
    } elseif {[string match $typesim "Static"] == 1} {
		puts "Static Pushover Analysis has been selected..."
		puts ""
		source Frame3D_analyze_Static_Pushover.tcl
        break
    }
}
