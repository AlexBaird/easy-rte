# Easy RTE Verilog Parallel Composition Template
./easy-rte-parser -i example/ab5/ab5.erte -o example/ab5/ab5.xml
python rtecomp/main.py ab5 ab5
## Build EasyRTE Local and then Compile AB5 Example using modified
make local && make verilog_enf PROJECT=ab5 FILE=ab5_modified COMPILEARGS=-parallelComposition

# ModelSim Compiled AB5 Example
vlog -reportprogress 300 -work work D:/github.com/AlexBaird/easy-rte-composition/example/ab5/parallel_F_ab5.sv

vsim work.parallel_F_ab5

add wave -position end  sim:/parallel_F_ab5/clk
add wave -position end  sim:/parallel_F_ab5/clk_input
add wave -position end  sim:/parallel_F_ab5/clk_output
add wave -position end  sim:/parallel_F_ab5/clk_transition
add wave -position end  sim:/parallel_F_ab5/fsm_state
add wave -position end  sim:/parallel_F_ab5/A_ptc
add wave -position end  sim:/parallel_F_ab5/A_ptc_out
add wave -position end  sim:/parallel_F_ab5/A_ptc_out_temp
add wave -position end  sim:/parallel_F_ab5/A_ptc_out_latched
add wave -position end  sim:/parallel_F_ab5/A_ptc_out_trans
add wave -position end  sim:/parallel_F_ab5/ab5_policy_AB5_input_recovery_ref
add wave -position end  sim:/parallel_F_ab5/ab5_policy_AB5_output_recovery_ref
add wave -position end  sim:/parallel_F_ab5/ab5_policy_AB5_state
add wave -position end  sim:/parallel_F_ab5/B_ctp
add wave -position end  sim:/parallel_F_ab5/B_ctp_ignore
add wave -position end  sim:/parallel_F_ab5/B_ctp_out
add wave -position end  sim:/parallel_F_ab5/B_ctp_out_latched
add wave -position end  sim:/parallel_F_ab5/B_ctp_out_trans
add wave -position end  sim:/parallel_F_ab5/v

force -freeze sim:/parallel_F_ab5/A_ptc 0 0
force -freeze sim:/parallel_F_ab5/B_ctp 0 0
force -freeze sim:/parallel_F_ab5/clk 0 0
force -freeze sim:/parallel_F_ab5/clk 1 50, 0 {75 ps} -r 100
#force -freeze sim:/parallel_F_ab5/clk_input 1 0, 0 {25 ps} -r 100
run .5ns

force -freeze sim:/parallel_F_ab5/A_ptc 1 0
run .2ns
force -freeze sim:/parallel_F_ab5/A_ptc 0 0
run 3ns