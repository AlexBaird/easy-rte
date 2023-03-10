# ModelSim Compile AB Example
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
force -freeze sim:/testbench_manual_parallel_F_ab/clk 1 0, 0 {50 ps} -r 100
force -freeze sim:/testbench_manual_parallel_F_ab/B_ctp 0 0
force -freeze sim:/testbench_manual_parallel_F_ab/A_ctp 0 0