module testbench_manual_parallel_F_ab (
        A_ctp,
        OUTPUT_A_ctp_enf_final_policy_a,
        OUTPUT_A_ctp_enf_final_policy_b,
        B_ctp,
        OUTPUT_B_ctp_enf_final_policy_a,
        OUTPUT_B_ctp_enf_final_policy_b,
        ab_policy_a_output_recovery_ref,
        ab_policy_b_output_recovery_ref,
        A_ctp_out,
        B_ctp_out,
        clk
    );
    
	input wire clk;
    
	input wire A_ctp;
	output wire OUTPUT_A_ctp_enf_final_policy_a;
	output wire OUTPUT_A_ctp_enf_final_policy_b;
	output wire [2:0] ab_policy_a_output_recovery_ref;
	output wire A_ctp_out;

	input wire B_ctp;
	output wire OUTPUT_B_ctp_enf_final_policy_a;
	output wire OUTPUT_B_ctp_enf_final_policy_b;
	output wire [2:0] ab_policy_b_output_recovery_ref;
	output wire B_ctp_out;

    wire [1:0] state;
    wire [1:0] state_b;

    F_combinatorialVerilog_ab_policy_a_input instance_input_a(
        .ab_policy_a_state_in(state),
        .clk(clk)
    );

    F_combinatorialVerilog_ab_policy_a_output instance_output_a(
        .A_ctp_in(A_ctp),
        .A_ctp_out(OUTPUT_A_ctp_enf_final_policy_a),
        .B_ctp_in(B_ctp),
        .B_ctp_out(OUTPUT_B_ctp_enf_final_policy_a),
        .ab_policy_a_output_recovery_ref(ab_policy_a_output_recovery_ref),
        .ab_policy_a_state_in(state),
        .clk(clk)
    );

    F_combinatorialVerilog_ab_policy_b_input instance_input_b(
        .ab_policy_b_state_in(state_b),
        .clk(clk)
    );

    F_combinatorialVerilog_ab_policy_b_output instance_output_b(
        .A_ctp_in(A_ctp),
        .A_ctp_out(OUTPUT_A_ctp_enf_final_policy_b),
        .B_ctp_in(B_ctp),
        .B_ctp_out(OUTPUT_B_ctp_enf_final_policy_b),
        .ab_policy_b_output_recovery_ref(ab_policy_b_output_recovery_ref),
        .ab_policy_b_state_in(state_b),
        .clk(clk)
    );

    F_LUT_Output_Edit instance_LUT(
        .A_ctp_in(A_ctp),
		.B_ctp_in(B_ctp),
		.policy_a_recovery_ref(ab_policy_a_output_recovery_ref),
		.policy_b_recovery_ref(ab_policy_b_output_recovery_ref),
		.A_ctp_out(A_ctp_out),
		.B_ctp_out(B_ctp_out),
        .clk(clk)
    );

    F_combinatorialVerilog_ab_policy_a_transition instance_trans_a(
        .A_ctp_final(A_ctp_out),
        .B_ctp_final(B_ctp_out),
        .ab_policy_a_state_out(state),
        .clk(clk)
    );

    F_combinatorialVerilog_ab_policy_b_transition instance_trans_b(
        .A_ctp_final(A_ctp_out),
        .B_ctp_final(B_ctp_out),
        .ab_policy_b_state_out(state_b),
        .clk(clk)
    );

endmodule