# Section Properties
# W-Section
#
set GammaConcrete [expr 150*$pcf];   		# Reinforced-Concrete floor slabs
set QdlCol [expr 114*$lbf/$ft]; 		# W-section weight per length
set QBeam [expr 94*$lbf/$ft];		# W-section weight per length
set QGird [expr 94*$lbf/$ft];		# W-section weight per length

if {$SectionType == "Elastic"} {
	# material properties:
	set Es [expr 29000*$ksi];		# Steel Young's Modulus
	set nu 0.3;			# Poisson's ratio
	set Gs [expr $Es/2./[expr 1+$nu]];  	# Torsional stiffness Modulus
	set J $Ubig;			# set large torsional stiffness
	# column sections: W27x114
	set AgCol [expr 33.5*pow($in,2)];		# cross-sectional area
	set IzCol [expr 4090.*pow($in,4)];		# moment of Inertia
	set IyCol [expr 159.*pow($in,4)];		# moment of Inertia
	# beam sections: W24x94
	set AgBeam [expr 27.7*pow($in,2)];		# cross-sectional area
	set IzBeam [expr 2700.*pow($in,4)];		# moment of Inertia
	set IyBeam [expr 109.*pow($in,4)];		# moment of Inertia
	# girder sections: W24x94
	set AgGird [expr 27.7*pow($in,2)];		# cross-sectional area
	set IzGird [expr 2700.*pow($in,4)];		# moment of Inertia
	set IyGird [expr 109.*pow($in,4)];		# moment of Inertia
	
	section Elastic $ColSecTag $Es $AgCol $IzCol $IyCol $Gs $J
	section Elastic $BeamSecTag $Es $AgBeam $IzBeam $IyBeam $Gs $J
	section Elastic $GirdSecTag $Es $AgGird $IzGird $IyGird $Gs $J

	set matIDhard 1;		# material numbers for recorder (this stressstrain recorder will be blank, as this is an elastic section)

} elseif {$SectionType == "FiberSection"} {
	# define MATERIAL properties 
	set Fy [expr 60.0*$ksi]
	set Es [expr 29000*$ksi];		# Steel Young's Modulus
	set nu 0.3;
	set Gs [expr $Es/2./[expr 1+$nu]];  # Torsional stiffness Modulus
	set Hiso 0
	set Hkin 1000
	set matIDhard 1
	uniaxialMaterial Hardening  $matIDhard $Es $Fy   $Hiso  $Hkin

	# ELEMENT properties
	# Structural-Steel W-section properties
	# column sections: W27x114
	set d [expr 27.29*$in];	# depth
	set bf [expr 10.07*$in];	# flange width
	set tf [expr 0.93*$in];	# flange thickness
	set tw [expr 0.57*$in];	# web thickness
	set nfdw 16;		# number of fibers along dw
	set nftw 2;		# number of fibers along tw
	set nfbf 16;		# number of fibers along bf
	set nftf 4;			# number of fibers along tf
	Wsection  $ColSecTagFiber $matIDhard $d $bf $tf $tw $nfdw $nftw $nfbf $nftf
	# beam sections: W24x94
	set d [expr 24.31*$in];	# depth
	set bf [expr 9.065*$in];	# flange width
	set tf [expr 0.875*$in];	# flange thickness
	set tw [expr 0.515*$in];	# web thickness
	set nfdw 16;		# number of fibers along dw
	set nftw 2;		# number of fibers along tw
	set nfbf 16;		# number of fibers along bf
	set nftf 4;			# number of fibers along tf
	Wsection  $BeamSecTagFiber $matIDhard $d $bf $tf $tw $nfdw $nftw $nfbf $nftf
	# girder sections: W24x94
	set d [expr 24.31*$in];	# depth
	set bf [expr 9.065*$in];	# flange width
	set tf [expr 0.875*$in];	# flange thickness
	set tw [expr 0.515*$in];	# web thickness
	set nfdw 16;		# number of fibers along dw
	set nftw 2;		# number of fibers along tw
	set nfbf 16;		# number of fibers along bf
	set nftf 4;			# number of fibers along tf
	Wsection  $GirdSecTagFiber $matIDhard $d $bf $tf $tw $nfdw $nftw $nfbf $nftf
	
	# assign torsional Stiffness for 3D Model
	uniaxialMaterial Elastic $SecTagTorsion $Ubig
	section Aggregator $ColSecTag $SecTagTorsion T -section $ColSecTagFiber
	section Aggregator $BeamSecTag $SecTagTorsion T -section $BeamSecTagFiber
	section Aggregator $GirdSecTag $SecTagTorsion T -section $GirdSecTagFiber
} else {
	puts "No section has been defined"
	return -1
}