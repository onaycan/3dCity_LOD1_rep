#+##########################################################################
 #
 # Intersect -- find where two line intersect given two points on each line
 # IntersectV -- same but w/ 2 point/vector pairs
 #   we want K,J where p1+K(v1) = p3+J(v3)
 #   convert into and solve matrix equation (a b / c d) ( K / J) = ( e / f )
 #
 proc Intersect {p1 p2 p3 p4} {
    return [IntersectV $p1 [VSub $p2 $p1] $p3 [VSub $p4 $p3]]
 }
 proc IntersectV {p1 v1 p3 v3} {
    foreach {x1 y1} $p1 {vx1 vy1} $v1 {x3 y3} $p3 {vx3 vy3} $v3 break
 
    set a $vx1
    set b [expr {-1 * $vx3}]
    set c $vy1
    set d [expr {-1 * $vy3}]
    set e [expr {$x3 - $x1}]
    set f [expr {$y3 - $y1}]
 
    set det [expr {double($a*$d - $b*$c)}]
    if {$det == 0} {error "Determinant is 0"}
 
    set k [expr {($d*$e - $b*$f) / $det}]
    #set j [expr {($a*$f - $c*$e) / $det}]
    return [VAdd $p1 $v1 $k]
 }
 ##+##########################################################################
 #
 # FindAngle -- returns the angle formed by p1,p2,p3
 # Computes the dot product on vectors p1-p2, p3-p2
 #
 proc FindAngle {p1 p2 p3} {
    foreach {x1 y1} [VSub $p1 $p2] {x2 y2} [VSub $p3 $p2] break
    
    set m1 [expr {hypot($x1,$y1)}]
    set m2 [expr {hypot($x2,$y2)}]
    if {$m1 == 0 || $m2 == 0} { return 0 }      ;# Coincidental points
    set dot [expr {$x1 * $x2 + $y1 * $y2}]
    
    set theta [expr {acos($dot / $m1 / $m2)}]
    if {$theta < 1e-5} {set theta 0}
    return $theta
 }
 ##+##########################################################################
 #
 # BisectAngle -- returns point on bisector of the angle formed by p1,p2,p3
 #
 proc BisectAngle {p1 p2 p3} {
    foreach {x1 y1} [VSub $p1 $p2] {x2 y2} [VSub $p3 $p2] break
    
    set s1 [expr {100.0 / hypot($x1, $y1)}]
    set s2 [expr {100.0 / hypot($x2, $y2)}]
    set v1 [VAdd $p2 [list $x1 $y1] $s1]        ;# 100*Unit vector from p2 to p1
    set v2 [VAdd $p2 [list $x2 $y2] $s2]        ;# 100*Unit vector from p2 to p3
    return [VAdd $v1 [VSub $v2 $v1] .5]
 }
 ##+##########################################################################
 #
 # TrisectAngle -- returns two points which are on the two lines trisecting
 # the angle created by points p1,p2,p3. We use the cross product to tell
 # us clockwise ordering.
 #
 proc TrisectAngle {p1 p2 p3} {
    set cross [VCross [VSub $p2 $p1] [VSub $p2 $p3]]
    if {$cross < 0} {foreach {p1 p3} [list $p3 $p1] break}
 
    set theta [FindAngle $p1 $p2 $p3]           ;# What the angle is
    set theta1 [expr {$theta / 3.0}]            ;# 1/3 of that angle
    set theta2 [expr {2 * $theta1}]             ;# 2/3 of that angle
 
    set v [VSub $p3 $p2]                        ;# We'll rotate this leg
    set v1 [VRotate $v $theta1]                 ;# By 1/3
    set v2 [VRotate $v $theta2]                 ;# By 2/3
    set t1 [VAdd $p2 $v1]                       ;# Trisect point 1
    set t2 [VAdd $p2 $v2]                       ;# Trisect point 2
 
    if {$cross < 0} {return [list $t2 $t1]}
    return [list $t1 $t2]
 }
 ##+##########################################################################
 #
 # HELPER FUNCTIONS:
 #   VAdd -- adds two vectors w/ scaling of 2nd vector
 #   VSub -- subtract two vectors
 #   VCross -- returns the cross product for 2D vectors (z=0)
 #   VRotate -- rotates vector counter-clockwise
 #
 proc VAdd {v1 v2 {scaling 1}} {
    foreach {x1 y1} $v1 {x2 y2} $v2 break
    return [list [expr {$x1 + $scaling*$x2}] [expr {$y1 + $scaling*$y2}]]
 }
 proc VSub {v1 v2} { return [VAdd $v1 $v2 -1] }
 proc VCross {v1 v2} {
    foreach {x1 y1} $v1 {x2 y2} $v2 break
    return [expr {($x1*$y2) - ($y1*$x2)}]
 }
 proc VRotate {v beta} {
    foreach {x y} $v break
    set xx [expr {$x * cos(-$beta) - $y * sin(-$beta)}]
    set yy [expr {$x * sin(-$beta) + $y * cos(-$beta)}]
    return [list $xx $yy]
 }