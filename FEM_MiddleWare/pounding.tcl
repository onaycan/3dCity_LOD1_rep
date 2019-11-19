if { $numSpan > 0 && $includeAbutmentGap=="YES"} {
		# Parameters for deck-abutment gap and pounding effects
	set gapAbutment         [expr 6.0*$in];          # When use rigid elements to replace SHJ, we need some length.
	set gammaRatio          [expr 20];               # Stiffness ratio of pounding to the axial stiffness of deck. 
	set poundingStiffness   [expr $gammaRatio*$A_deckEndDiaphragm*0.5*$E_deck/($typicalSpanLength*$numSpanContinuous)];         
	set poundingFy          [expr $poundingStiffness*0.01];
	set eta                 [expr 0.01]; 
	set damage              "nodamage";
};

uniaxialMaterial ElasticPPGap 51 $poundingStiffness $poundingFy [expr -$gapAbutment] $eta $damage;
	element zeroLength    [expr 1*10000+0]        [expr 1*10000+0]         [expr 1*10000+1]        -mat 51 -dir 1; #AbutBridgeGap on The Left
	element zeroLength    [expr ($numSpan+1)*10000+0] [expr $numSpan*10000+9]  [expr ($numSpan+1)*10000+0] -mat 51 -dir 1; #AbutBridgeGap on The Right
	puts -nonewline $ElementsTypeFile "[expr 1*10000+0]        $poundingElementsTypeTag \n";
	puts -nonewline $ElementsTypeFile "[expr ($numSpan+1)*10000+0] $poundingElementsTypeTag \n";
	lappend abutmentGapEleList  [expr 1*10000+0];
	lappend abutmentGapEleList  [expr ($numSpan+1)*10000+0];
	
	
		uniaxialMaterial ElasticPPGap 51 $poundingStiffness $poundingFy [expr -$gapAbutment] $eta $damage;
	element zeroLength    [expr 1*10000+0]        [expr 1*10000+0]         [expr 1*10000+1]        -mat 51 -dir 1; #AbutBridgeGap on The Left
	element zeroLength    [expr ($numSpan+1)*10000+0] [expr $numSpan*10000+9]  [expr ($numSpan+1)*10000+0] -mat 51 -dir 1; #AbutBridgeGap on The Right
	puts -nonewline $ElementsTypeFile "[expr 1*10000+0]        $poundingElementsTypeTag \n";
	puts -nonewline $ElementsTypeFile "[expr ($numSpan+1)*10000+0] $poundingElementsTypeTag \n";
	lappend abutmentGapEleList  [expr 1*10000+0];
	lappend abutmentGapEleList  [expr ($numSpan+1)*10000+0];