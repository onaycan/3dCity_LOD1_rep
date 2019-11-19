# compute the area of a polygon given its coordinates
 #
 # Argument: coords -> list of coordinates
 #
 # Returns: Area of polygon (taking care of holes inside the polygon)
 #
 proc polygonArea {coords}  {
   # make sure we have a closed set of coords:
   if {[lindex $coords 0] != [lindex $coords end-1] \
    || [lindex $coords 1] != [lindex $coords end]} {
       lappend coords [lindex $coords 0] [lindex $coords 1]
   }
   # append another point for the calculation:
   lappend coords [lindex $coords 2] [lindex $coords 3]
   # area:
   set area 0
   # number of vertices:
   set n [expr {([llength $coords]-4)/2}]
   # build lists with x and y coordinates only:
   foreach {x y} $coords {
      lappend xList $x
      lappend yList $y
   }
   for {set i 1; set j 2; set k 0} {$i <= $n} {incr i; incr j; incr k} {
      set area [expr {$area + ([lindex $xList $i] * ([lindex $yList $j] - [lindex $yList $k]))}]
   }
   set result [expr {$area/2.0}]
   return [expr abs($result)]
 }

