# ------------   Eigenvalue analysis  -------------------------------------------------------
set lambda [eigen $numModes];
#set lambda [eigen -fullGenLapack $numModes]

# calculate frequencies and periods of the structure ---------------------------------------------------
set omega {}
set f {}
set T {}
set pi 3.141593

foreach lam $lambda {
	lappend omega [expr sqrt($lam)]
	lappend f [expr sqrt($lam)/(2*$pi)]
	lappend T [expr (2*$pi)/sqrt($lam)]
}

# record the eigenvectors
# ------------------------
# record

# Define DISPLAY -------------------------------------------------------------
#DisplayModel3D ModeShape ;	 # options: DeformedShape NodeNumbers ModeShape

# -------------------------------------------------------------
	

for {set numInFile 0} {$numInFile <= [expr $Buildingnum-1]} {incr numInFile 1} {
	set aBID [lindex $BID $numInFile]; # assign Building number
	#set _aBID "_Building_$aBID"
	puts "eigenfrequencies of the Building $aBID are $f"
	puts "periods of the Building $aBID are $T"
}
#