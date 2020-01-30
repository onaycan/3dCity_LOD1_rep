#
# Written: SA
# Date: November 2019
#
# A procedure which parses a ground motion record from the PEER
# strong motion database by finding dt in the record header, then
# echoing data values to the output file.
#
# Formal arguments
#   inFilename -- file which contains PEER strong motion record
#   outFilename -- file to be written in format G3 can read
#   dt -- time step determined from file header
#

proc ReadSMDFile {inFilename outFilename dt} {
	# read gm input format

   # Pass dt by reference
   upvar $dt DT

   # Open the input file and catch the error if it can't be read
   if [catch {open $inFilename r} inFileID] {
      puts stderr "Cannot open $inFilename for reading"
   } else {
      # Open output file for writing
      set outFileID [open $outFilename w]

      # Flag indicating dt is found and that ground motion
      # values should be read -- ASSUMES dt is on last line
      # of header!!!
      set flag 0

      # Look at each line in the file
      foreach line [split [read $inFileID] \n] {

         if {[llength $line] == 0} {
            # Blank line --> do nothing
            continue
         } elseif {$flag == 1} {
            # Echo ground motion values to output file
            puts $outFileID $line
         } else {
            # Search header lines for dt
            foreach word [split $line] {
               # Read in the time step
               if {$flag == 1} {
                  set DT $word
                  break
               }
               # Find the desired token and set the flag
               if {[string match $word "DT="] == 1} {set flag 1}
            }
         }
      }

      # Close the output file
      close $outFileID

      # Close the input file
      close $inFileID
   }
};                                                                                                                                     #
###########################################################################

