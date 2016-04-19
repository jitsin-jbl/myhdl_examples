#
#
# ISE implementation script
# create: Fri, 29 Nov 2013 16:00:06 +0000
# by: compile_user_io.py
#
#
# set compile directory:
set compile_directory .
set top_name xula
set top xula
# set Project:
set proj xula
# change to the directory:
cd xilinx/ise/user_io/
# set ucf file:
set constraints_file xula.ucf
# set variables:
project open xula.xise 
project set family spartan3A
project set device xc3s200a
project set package VQ100
project set speed -4

# add hdl files:
xfile add xula.v
# test if set_source_directory is set:
if { ! [catch {set source_directory $source_directory}]} {
  project set "Macro Search Path"
 $source_directory -process Translate
}
project set "FPGA Start-Up Clock" "JTAG Clock" -process "Generate Programming File" 
# run the implementation:
process run "Synthesize" 
process run "Translate" 
process run "Map" 
process run "Place & Route" 
process run "Generate Programming File" 
# close the project:
project close
