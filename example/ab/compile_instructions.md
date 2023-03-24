# Easy RTE Compile AB Example
## Default XML
./easy-rte-parser -i example/ab/ab.erte -o example/ab/ab.xml
## Modify XML to Add Recoveries
python rtecomp/main.py // Check the file is selected in the script (TODO: input file path)
## EasyRTE XML to Verilog
 make verilog_enf PROJECT=ab FILE=ab_modified COMPILEARGS=-synthesis

# ModelSim Manual AB Example
## Manual Parallel
vlog -reportprogress 300 -work work D:/github.com/AlexBaird/easy-rte-composition/example/ab/manual_parallel_F_ab.sv

## Test Bench Temp Save Commands
### Compile Test Bench
vlog -reportprogress 300 -work work D:/github.com/AlexBaird/easy-rte-composition/example/ab/testbench_manual_parallel_F_ab.sv

### Simulate Test Bench
vsim work.testbench_manual_parallel_F_ab

### Add waveforms and force inputs and clock
add wave -position end  sim:/testbench_manual_parallel_F_ab/A_ctp
add wave -position end  sim:/testbench_manual_parallel_F_ab/B_ctp
add wave -position end  sim:/testbench_manual_parallel_F_ab/clk
add wave -position end  sim:/testbench_manual_parallel_F_ab/OUTPUT_A_ctp_enf_final_policy_a
add wave -position end  sim:/testbench_manual_parallel_F_ab/OUTPUT_A_ctp_enf_final_policy_b
add wave -position end  sim:/testbench_manual_parallel_F_ab/OUTPUT_B_ctp_enf_final_policy_a
add wave -position end  sim:/testbench_manual_parallel_F_ab/OUTPUT_B_ctp_enf_final_policy_b
add wave -position end  sim:/testbench_manual_parallel_F_ab/state
add wave -position end  sim:/testbench_manual_parallel_F_ab/state_b
add wave -position end  sim:/testbench_manual_parallel_F_ab/ab_policy_a_output_recovery_ref
add wave -position end  sim:/testbench_manual_parallel_F_ab/ab_policy_b_output_recovery_ref
add wave -position end  sim:/testbench_manual_parallel_F_ab/A_ctp_out
add wave -position end  sim:/testbench_manual_parallel_F_ab/B_ctp_out
add wave -position end  sim:/testbench_manual_parallel_F_ab/instance_LUT/recovery_key

add wave -position end  sim:/testbench_manual_parallel_F_ab/instance_trans_a/ab_policy_a_c_state
add wave -position end  sim:/testbench_manual_parallel_F_ab/instance_trans_a/ab_policy_a_n_state
add wave -position end  sim:/testbench_manual_parallel_F_ab/instance_trans_a/ab_policy_a_state_out

add wave -position end  sim:/testbench_manual_parallel_F_ab/instance_trans_b/ab_policy_b_c_state
add wave -position end  sim:/testbench_manual_parallel_F_ab/instance_trans_b/ab_policy_b_n_state
add wave -position end  sim:/testbench_manual_parallel_F_ab/instance_trans_b/ab_policy_b_state_out

force -freeze sim:/testbench_manual_parallel_F_ab/clk 1 0, 0 {50 ps} -r 100
force -freeze sim:/testbench_manual_parallel_F_ab/B_ctp 0 0
force -freeze sim:/testbench_manual_parallel_F_ab/A_ctp 0 0

run .1ns
force -freeze sim:/testbench_manual_parallel_F_ab/A_ctp 1 0
force -freeze sim:/testbench_manual_parallel_F_ab/B_ctp 1 0
run .1ns
force -freeze sim:/testbench_manual_parallel_F_ab/A_ctp 0 0
force -freeze sim:/testbench_manual_parallel_F_ab/B_ctp 0 0
run 1ns

force -freeze sim:/testbench_manual_parallel_F_ab/A_ctp 1 0
force -freeze sim:/testbench_manual_parallel_F_ab/B_ctp 1 0
run 1ns


# Easy RTE Verilog Parallel Composition Template
## Build EasyRTE Local and then Compile AB Example using modified
make local && make verilog_enf PROJECT=ab FILE=ab_modified COMPILEARGS=-parallelComposition

# ModelSim Compiled AB Example
## Compiled Parallel
vlog -reportprogress 300 -work work D:/github.com/AlexBaird/easy-rte-composition/example/ab/parallel_F_ab.sv

## Some Simulation Things
vsim work.parallel_F_ab

add wave -position end  sim:/parallel_F_ab/A_ctp
add wave -position end  sim:/parallel_F_ab/A_ctp_out
add wave -position end  sim:/parallel_F_ab/ab_policy_a_input_recovery_ref
add wave -position end  sim:/parallel_F_ab/ab_policy_a_output_recovery_ref
add wave -position end  sim:/parallel_F_ab/ab_policy_a_state
add wave -position end  sim:/parallel_F_ab/ab_policy_b_input_recovery_ref
add wave -position end  sim:/parallel_F_ab/ab_policy_b_output_recovery_ref
add wave -position end  sim:/parallel_F_ab/ab_policy_b_state
add wave -position end  sim:/parallel_F_ab/B_ctp
add wave -position end  sim:/parallel_F_ab/B_ctp_out
add wave -position end  sim:/parallel_F_ab/clk

force -freeze sim:/parallel_F_ab/clk 1 0, 0 {50 ps} -r 100
force -freeze sim:/parallel_F_ab/B_ctp 0 0
force -freeze sim:/parallel_F_ab/A_ctp 0 0
run .1ns

force -freeze sim:/parallel_F_ab/A_ctp 1 0
force -freeze sim:/parallel_F_ab/B_ctp 1 0
run .1ns
force -freeze sim:/parallel_F_ab/A_ctp 0 0
force -freeze sim:/parallel_F_ab/B_ctp 0 0
run 1ns

force -freeze sim:/parallel_F_ab/A_ctp 1 0
force -freeze sim:/parallel_F_ab/B_ctp 1 0
run 1ns