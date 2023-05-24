# Monolithic
make verilog_enf PROJECT=abcd FILE=abcd PARSEARGS=-product COMPILEARGS=-synthesis

# Parallel 
./easy-rte-parser -i example/abcd/abcd.erte -o example/abcd/abcd.xml
python rtecomp/main.py abcd abcd
make verilog_enf PROJECT=abcd FILE=abcd_modified COMPILEARGS=-parallelComposition

vlog -reportprogress 300 -work work D:/github.com/AlexBaird/easy-rte-composition/example/abcd/parallel_F_abcd.sv
vsim work.parallel_F_abcd

# Series (Compiled)
./easy-rte-parser -i example/abcd/abcd.erte -o example/abcd/abcd.xml
python rtecomp/main.py abcd abcd
make verilog_enf PROJECT=abcd FILE=abcd_modified COMPILEARGS=-serialComposition

## Model Sim
vlog -reportprogress 300 -work work D:/github.com/AlexBaird/easy-rte-composition/example/abcd/series_F_abcd.sv
vsim work.series_F_abcd
### Add Clock
force -freeze sim:/manual_series_F_abcd/clk 1 0, 0 {50 ps} -r 100
force -freeze sim:/series_F_abcd/clk 1 0, 0 {50 ps} -r 100
### Run 2ns
run 2ns

# Series (Manual)
vlog -reportprogress 300 -work work D:/github.com/AlexBaird/easy-rte-composition/example/abcd/manual_series_F_abcd.sv
vsim work.manual_series_F_abcd
## Add Waves
add wave -position end  sim:/manual_series_F_abcd/A_ptc
add wave -position end  sim:/manual_series_F_abcd/A_ptc_out
add wave -position end  sim:/manual_series_F_abcd/A_ptc_out_ignore
add wave -position end  sim:/manual_series_F_abcd/A_ptc_out_latched
add wave -position end  sim:/manual_series_F_abcd/A_ptc_out_trans
add wave -position end  sim:/manual_series_F_abcd/abcd_policy_ab_input_recovery_ref
add wave -position end  sim:/manual_series_F_abcd/abcd_policy_ab_output_recovery_ref
add wave -position end  sim:/manual_series_F_abcd/abcd_policy_ab_state
add wave -position end  sim:/manual_series_F_abcd/abcd_policy_ac_input_recovery_ref
add wave -position end  sim:/manual_series_F_abcd/abcd_policy_ac_output_recovery_ref
add wave -position end  sim:/manual_series_F_abcd/abcd_policy_ac_state
add wave -position end  sim:/manual_series_F_abcd/abcd_policy_ad_input_recovery_ref
add wave -position end  sim:/manual_series_F_abcd/abcd_policy_ad_output_recovery_ref
add wave -position end  sim:/manual_series_F_abcd/abcd_policy_ad_state
add wave -position end  sim:/manual_series_F_abcd/B_ctp
add wave -position end  sim:/manual_series_F_abcd/B_ctp_out
add wave -position end  sim:/manual_series_F_abcd/B_ctp_out_ignore
add wave -position end  sim:/manual_series_F_abcd/B_ctp_out_latched
add wave -position end  sim:/manual_series_F_abcd/B_ctp_out_trans
add wave -position end  sim:/manual_series_F_abcd/C_ctp
add wave -position end  sim:/manual_series_F_abcd/C_ctp_out
add wave -position end  sim:/manual_series_F_abcd/C_ctp_out_ignore
add wave -position end  sim:/manual_series_F_abcd/C_ctp_out_latched
add wave -position end  sim:/manual_series_F_abcd/C_ctp_out_trans
add wave -position end  sim:/manual_series_F_abcd/clk
add wave -position end  sim:/manual_series_F_abcd/clk_input_1
add wave -position end  sim:/manual_series_F_abcd/clk_input_2
add wave -position end  sim:/manual_series_F_abcd/clk_input_3
add wave -position end  sim:/manual_series_F_abcd/clk_output_1
add wave -position end  sim:/manual_series_F_abcd/clk_output_2
add wave -position end  sim:/manual_series_F_abcd/clk_output_3
add wave -position end  sim:/manual_series_F_abcd/clk_transition
add wave -position end  sim:/manual_series_F_abcd/D_ctp
add wave -position end  sim:/manual_series_F_abcd/D_ctp_out
add wave -position end  sim:/manual_series_F_abcd/D_ctp_out_ignore
add wave -position end  sim:/manual_series_F_abcd/D_ctp_out_latched
add wave -position end  sim:/manual_series_F_abcd/D_ctp_out_trans
add wave -position end  sim:/manual_series_F_abcd/fsm_state
## Add Clock
force -freeze sim:/manual_series_F_abcd/clk 1 0, 0 {50 ps} -r 100
## Run 2ns
run 2ns

# Quartus Run
python3 QuartusRun.py "D:\\github.com\\AlexBaird\\easy-rte-composition\\example" abcd

# Quartus Results
python3 QuartusReadResults.py "D:\\github.com\\AlexBaird\\easy-rte-composition\\example" abcd
