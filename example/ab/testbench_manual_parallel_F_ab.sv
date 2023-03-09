module testbench_manual_parallel_F_ab (
    A_ctp,
    OUTPUT_A_ctp_enf_final,
    OUTPUT_A_ctp_enf_final_2,
    B_ctp,
    OUTPUT_B_ctp_enf_final,
    OUTPUT_B_ctp_enf_final_2,
    clk
);
    
	input wire clk;
	input wire A_ctp;
	input wire B_ctp;
	output wire OUTPUT_A_ctp_enf_final;
	output wire OUTPUT_B_ctp_enf_final;
	output wire OUTPUT_A_ctp_enf_final_2;
	output wire OUTPUT_B_ctp_enf_final_2;

    wire [1:0] state;
    wire [1:0] state_b;

    F_combinatorialVerilog_ab_policy_a_input instance_input_a(
        .ab_policy_a_state_in(state),
        .clk(clk)
    );

    F_combinatorialVerilog_ab_policy_a_output instance_output_a(
        .A_ctp_in(A_ctp),
        .A_ctp_out(OUTPUT_A_ctp_enf_final),
        .B_ctp_in(B_ctp),
        .B_ctp_out(OUTPUT_B_ctp_enf_final),
        .ab_policy_a_state_in(state),
        .clk(clk)
    );

    F_combinatorialVerilog_ab_policy_a_transition instance_trans_a(
        .A_ctp_final(OUTPUT_A_ctp_enf_final),
        .B_ctp_final(OUTPUT_B_ctp_enf_final),
        .ab_policy_a_state_out(state),
        .clk(clk)
    );

    F_combinatorialVerilog_ab_policy_b_input instance_input_b(
        .ab_policy_b_state_in(state_b),
        .clk(clk)
    );

    F_combinatorialVerilog_ab_policy_b_output instance_output_b(
        .A_ctp_in(A_ctp),
        .A_ctp_out(OUTPUT_A_ctp_enf_final_2),
        .B_ctp_in(B_ctp),
        .B_ctp_out(OUTPUT_B_ctp_enf_final_2),
        .ab_policy_b_state_in(state_b),
        .clk(clk)
    );

    F_combinatorialVerilog_ab_policy_b_transition instance_trans_b(
        .A_ctp_final(OUTPUT_A_ctp_enf_final_2),
        .B_ctp_final(OUTPUT_B_ctp_enf_final_2),
        .ab_policy_b_state_out(state_b),
        .clk(clk)
    );

endmodule