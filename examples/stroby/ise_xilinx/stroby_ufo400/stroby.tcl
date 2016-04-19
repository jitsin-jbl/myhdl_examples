#
#
# ISE implementation script
# create: Sun, 05 Feb 2012 16:40:12 +0000
# by: stroby_run_tools.py
#
#
# set compile directory:
set compile_directory ise_xilinx/stroby_ufo400/
set top_name stroby
# input source files:
set hdl_files [ list \
                 ufo400_leds.v \
]
# set ucf file:
set constraints_file ise_xilinx/stroby_ufo400/stroby.ucf
# set Project:
set proj stroby
# change to the directory:
cd ise_xilinx/stroby_ufo400/
# set variables:
project new stroby.xise
project set family spartan3
project set device xc3s400
project set package tq144
project set speed -5
# add hdl files:
xfile add ufo400_leds.v
# test if set_source_directory is set:
if { ! [catch {set source_directory $source_directory}]} {
  project set "Macro Search Path"
 $source_directory -process Translate
}
# run the implementation:
process run "Synthesize" 
process run "Translate" 
process run "Map" 
process run "Place & Route" 
process run "Generate Programming File" 
# close the project:
project close
