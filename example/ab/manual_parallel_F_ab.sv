
//This file should be called F_ab.sv
//This is autogenerated code. Edit by hand at your peril!!!

//Warning: This is experimental parallel composition code.


module F_combinatorialVerilog_ab_policy_a_input(
	//inputs (plant to controller)


	input wire [1:0] ab_policy_a_state_in,

	// Recovery Reference
	output wire [2:0] ab_policy_a_input_recovery_ref,

	input wire clk
	);

	//For each policy, we need define types for the state machines
	localparam
		POLICY_STATE_ab_a_a0 = 0,
		POLICY_STATE_ab_a_a1 = 1,
		POLICY_STATE_ab_a_a2 = 3,
		POLICY_STATE_ab_a_violation = 2;


	// Recovery ref declare and init
	reg [2:0] recoveryReference = 0;

	//internal vars
	
	// initial begin
	// 	policy_a_no_edit = 1;
	// end

	always @* begin
		
		// Default no change to inputs/outputs (transparency) 

		// Do we need //recoveryReference default?

		// Default no clock reset
		

		//input policies
		
			//INPUT POLICY a BEGIN 
			case(ab_policy_a_state_in)
				POLICY_STATE_ab_a_a0: begin
					
				end
				POLICY_STATE_ab_a_a1: begin
					
				end
				POLICY_STATE_ab_a_a2: begin
					
				end
				
			endcase
		
		//INPUT POLICY a END
	end
	assign ab_policy_a_input_recovery_ref = recoveryReference;

endmodule

module F_combinatorialVerilog_ab_policy_a_output (
	//outputs (controller to plant)
	input wire  A_ctp_in,
	// output reg  A_ctp_out,
	
	input wire  B_ctp_in,
	// output reg  B_ctp_out,


	// State Input
	input wire [1:0] ab_policy_a_state_in,

	// Recovery Reference Output
	output wire [2:0] ab_policy_a_output_recovery_ref,

	input wire clk

	);

	//For each policy, we need define types for the state machines
	localparam
		POLICY_STATE_ab_a_a0 = 0,
		POLICY_STATE_ab_a_a1 = 1,
		POLICY_STATE_ab_a_a2 = 3,
		POLICY_STATE_ab_a_violation = 2;


	reg A = 0;

	reg B = 0;

	// Recovery ref declare and init
	reg [2:0] recoveryReference = 0;

	initial begin
		recoveryReference = 0;
	end

	always @* begin
		// Default no change to inputs/outputs (transparency) 
		A = A_ctp_in;
		B = B_ctp_in;

		recoveryReference = 0;

		// Default no clock reset

		//output policies
			//OUTPUT POLICY a BEGIN 
		
		case(ab_policy_a_state_in)
			POLICY_STATE_ab_a_a0: begin
				// Default location recovery reference
				recoveryReference = 3;

				if (!(A) && B) begin
					//transition a0 -> violation on (!A and B)
					//select a transition to solve the problem
					
					//Selected non-violation transition "a0 -> a1 on ( A )" and action is required
					A = 1;

					// Set recovery reference
					recoveryReference = 1;
					
				end 
				if (!(A) && !(B)) begin
					//transition a0 -> violation on (!A and !B)
					//select a transition to solve the problem
					
					//Selected non-violation transition "a0 -> a1 on ( A )" and action is required
					A = 1;

					// Set recovery reference
					recoveryReference = 2;
	
				end 
			end
			POLICY_STATE_ab_a_a1: begin
				// Default location recovery reference
				recoveryReference = 6;

				if (A && B) begin
					//transition a1 -> violation on (A and B)
					//select a transition to solve the problem
					
					//Selected non-violation transition "a1 -> a0 on ( !A )" and action is required
					A = 0;

					// Set recovery reference
					recoveryReference = 4;
					
				end 
				if (A && !(B)) begin
					//transition a1 -> violation on (A and !B)
					//select a transition to solve the problem
					
					//Selected non-violation transition "a1 -> a0 on ( !A )" and action is required
					A = 0;

					// Set recovery reference
					recoveryReference = 5;

				end 
			end
			POLICY_STATE_ab_a_a2: begin

			end
		endcase

		//OUTPUT POLICY a END
		
		// Post output enforced 
		// A_ctp_out = A;
		// B_ctp_out = B;
		
	end

	assign ab_policy_a_output_recovery_ref = recoveryReference;

endmodule

module F_combinatorialVerilog_ab_policy_a_transition (
	// Final inputs (plant to controller) 
	// Final outputs (controller to plant) 
	input wire A_ctp_final,

	input wire B_ctp_final,


	// State Output
	output wire [1:0] ab_policy_a_state_out,

	input wire clk
	);

	//For each policy, we need define types for the state machines
	localparam
		POLICY_STATE_ab_a_a0 = 0,
		POLICY_STATE_ab_a_a1 = 1,
		POLICY_STATE_ab_a_a2 = 3,
		POLICY_STATE_ab_a_violation = 2;

	// Maybe remove these?
	reg A = 0; 

	reg B = 0;



	//For each policy, we need a reg for the state machine
	reg [1:0] ab_policy_a_c_state = POLICY_STATE_ab_a_a2;
	reg [1:0] ab_policy_a_n_state = POLICY_STATE_ab_a_a2;

	initial begin
		ab_policy_a_c_state = POLICY_STATE_ab_a_a2;
		ab_policy_a_n_state = POLICY_STATE_ab_a_a2;
	end

	always @(posedge clk)
	begin
		ab_policy_a_c_state = ab_policy_a_n_state;

		//increment timers/clocks
		//internal vars
		
	end

	always @* begin


		A = A_ctp_final;
		B = B_ctp_final;

		// Default no location change
		ab_policy_a_n_state = ab_policy_a_c_state;
		
		// Default no clock reset
		

		//transTaken_ab_policy_a = 0;
		//select transition to advance state
		case(ab_policy_a_c_state)
			POLICY_STATE_ab_a_a0: begin
				
				if (A) begin
					//transition a0 -> a1 on ( A )
					ab_policy_a_n_state = POLICY_STATE_ab_a_a1;
					//set expressions
					
					//transTaken_ab_policy_a = 1;
				end 
				else if (!(A) && B) begin
					//transition a0 -> violation on (!A and B)
					ab_policy_a_n_state = POLICY_STATE_ab_a_violation;
					//set expressions
					
					//transTaken_ab_policy_a = 1;
				end 
				else if (!(A) && !(B)) begin
					//transition a0 -> violation on (!A and !B)
					ab_policy_a_n_state = POLICY_STATE_ab_a_violation;
					//set expressions
					
					//transTaken_ab_policy_a = 1;
				end  
				else begin
					//only possible in a violation
					ab_policy_a_n_state = POLICY_STATE_ab_a_violation;
					//transTaken_ab_policy_a = 1;
				end
			end
			POLICY_STATE_ab_a_a1: begin
				
				if (!(A)) begin
					//transition a1 -> a0 on ( !A )
					ab_policy_a_n_state = POLICY_STATE_ab_a_a0;
					//set expressions
					
					//transTaken_ab_policy_a = 1;
				end 
				else if (A && B) begin
					//transition a1 -> violation on (A and B)
					ab_policy_a_n_state = POLICY_STATE_ab_a_violation;
					//set expressions
					
					//transTaken_ab_policy_a = 1;
				end 
				else if (A && !(B)) begin
					//transition a1 -> violation on (A and !B)
					ab_policy_a_n_state = POLICY_STATE_ab_a_violation;
					//set expressions
					
					//transTaken_ab_policy_a = 1;
				end
				else begin
					//only possible in a violation
					ab_policy_a_n_state = POLICY_STATE_ab_a_violation;
					//transTaken_ab_policy_a = 1;
				end
			end
			POLICY_STATE_ab_a_a2: begin
				if (A) begin
					ab_policy_a_n_state = POLICY_STATE_ab_a_a1;
				end		
			end
			default begin
				//if we are here, we're in the violation state
				//the violation state permanently stays in violation
				ab_policy_a_n_state = POLICY_STATE_ab_a_violation;
				//transTaken_ab_policy_a = 1;
			end
		endcase
	end

	assign ab_policy_a_state_out = ab_policy_a_c_state;

endmodule


module F_combinatorialVerilog_ab_policy_b_input (

	//inputs (plant to controller)

	//helpful internal variable outputs 
	
	//helpful state output input var,

	input wire [1:0] ab_policy_b_state_in,

	// Recovery Reference
	output wire [2:0] ab_policy_b_input_recovery_ref,

	input wire clk
	);

	//For each policy, we need define types for the state machines
	localparam
		POLICY_STATE_ab_b_b0 = 0,
		POLICY_STATE_ab_b_b1 = 1,
		POLICY_STATE_ab_b_b2 = 3,
		POLICY_STATE_ab_b_violation = 2;


	// Recovery ref declare and init
	reg [2:0] recoveryReference = 0;
	//internal vars
	

	initial begin
		recoveryReference = 0;
	end

	always @* begin
		
		// Default no change to inputs/outputs (transparency) 

		// Do we need //recoveryReference default?

		// Default no clock reset
		

		//input policies
		
			//INPUT POLICY b BEGIN 
			case(ab_policy_b_state_in)
				POLICY_STATE_ab_b_b0: begin
					
				end
				POLICY_STATE_ab_b_b1: begin
					
				end
				POLICY_STATE_ab_b_b2: begin
					
				end
				
			endcase
		
		//INPUT POLICY b END
	end
	assign ab_policy_b_input_recovery_ref = recoveryReference;

endmodule

module F_combinatorialVerilog_ab_policy_b_output (
	//outputs (controller to plant)
	input wire  A_ctp_in,
	output reg  A_ctp_out,
	
	input wire  B_ctp_in,
	output reg  B_ctp_out,
	

	// State Input
	input wire [1:0] ab_policy_b_state_in,

	// Recovery Reference Output
	output wire [2:0] ab_policy_b_output_recovery_ref,

	input wire clk

	);

	//For each policy, we need define types for the state machines
	localparam
		POLICY_STATE_ab_b_b0 = 0,
		POLICY_STATE_ab_b_b1 = 1,
		POLICY_STATE_ab_b_b2 = 3,
		POLICY_STATE_ab_b_violation = 2;


	reg A = 0;

	reg B = 0;

	// Recovery ref declare and init
	reg [2:0] recoveryReference = 0;


	initial begin
		recoveryReference = 0;
	end

	always @* begin
		// Default no change to inputs/outputs (transparency) 
		A = A_ctp_in;
		B = B_ctp_in;

		recoveryReference = 0;

		//output policies
		//OUTPUT POLICY b BEGIN 
		
		case(ab_policy_b_state_in)
			POLICY_STATE_ab_b_b0: begin
				// Default location recovery reference
				recoveryReference = 3;

				if (A && !(B)) begin
					//transition b0 -> violation on (A and !B)
					//select a transition to solve the problem
					
					//Selected non-violation transition "b0 -> b1 on ( B )" and action is required
					B = 1;

					// Set recovery reference
					recoveryReference = 1;
					
				end 
				if (!(A) && !(B)) begin
					//transition b0 -> violation on (!A and !B)
					//select a transition to solve the problem
					
					//Selected non-violation transition "b0 -> b1 on ( B )" and action is required
					B = 1;
					
					// Set recovery reference
					recoveryReference = 2;

				end 
			end
			POLICY_STATE_ab_b_b1: begin
				// Default location recovery reference
				recoveryReference = 6;

				if (A && B) begin
					//transition b1 -> violation on (A and B)
					//select a transition to solve the problem
					
					//Selected non-violation transition "b1 -> b0 on ( !B )" and action is required
					B = 0;

					// Set recovery reference
					recoveryReference = 4;

				end 
				if (!(A) && B) begin
					//transition b1 -> violation on (!A and B)
					//select a transition to solve the problem
					
					//Selected non-violation transition "b1 -> b0 on ( !B )" and action is required
					B = 0;
					
					// Set recovery reference
					recoveryReference = 5;

				end 
			end
			POLICY_STATE_ab_b_b2: begin
					
			end
		endcase
		
		//OUTPUT POLICY b END

		// Post input enforced 
		
		// Post output enforced 
		A_ctp_out = A;
		B_ctp_out = B;
	end
	assign ab_policy_b_output_recovery_ref = recoveryReference;
	
endmodule

module F_combinatorialVerilog_ab_policy_b_transition (
	input wire A_ctp_final,
	input wire B_ctp_final,

	output reg [1:0] ab_policy_b_state_out,

	input wire clk
	);

	//For each policy, we need define types for the state machines
	localparam
		POLICY_STATE_ab_b_b0 = 0,
		POLICY_STATE_ab_b_b1 = 1,
		POLICY_STATE_ab_b_b2 = 3,
		POLICY_STATE_ab_b_violation = 2;

	// Maybe remove these?
	reg A = 0; 

	reg B = 0;

	//For each policy, we need a reg for the state machine
	reg [1:0] ab_policy_b_c_state = POLICY_STATE_ab_b_b2;
	reg [1:0] ab_policy_b_n_state = POLICY_STATE_ab_b_b2;

	initial begin
		// A = 0; Maybe needed?? If transition module outputs ctrl sigs
		// B = 0;
		ab_policy_b_c_state = POLICY_STATE_ab_b_b2;
		ab_policy_b_n_state = POLICY_STATE_ab_b_b2;
	end

	always @(posedge clk)
	begin
		ab_policy_b_c_state = ab_policy_b_n_state;

		//increment timers/clocks
		//internal vars
		
	end

	always @* begin


		A = A_ctp_final;
		B = B_ctp_final;

		//transTaken_ab_policy_a = 0;
		//select transition to advance state
		case(ab_policy_b_c_state)
			POLICY_STATE_ab_b_b0: begin
				
				if (B) begin
					//transition b0 -> b1 on ( B )
					ab_policy_b_n_state = POLICY_STATE_ab_b_b1;
					//set expressions
					
					//transTaken_ab_policy_b = 1;
				end 
				else if (A && !(B)) begin
					//transition b0 -> violation on (A and !B)
					ab_policy_b_n_state = POLICY_STATE_ab_b_violation;
					//set expressions
					
					//transTaken_ab_policy_b = 1;
				end 
				else if (!(A) && !(B)) begin
					//transition b0 -> violation on (!A and !B)
					ab_policy_b_n_state = POLICY_STATE_ab_b_violation;
					//set expressions
					
					//transTaken_ab_policy_b = 1;
				end  
				else begin
					//only possible in a violation
					ab_policy_b_n_state = POLICY_STATE_ab_b_violation;
					//transTaken_ab_policy_b = 1;
				end
			end
			POLICY_STATE_ab_b_b1: begin
				
				if (!(B)) begin
					//transition b1 -> b0 on ( !B )
					ab_policy_b_n_state = POLICY_STATE_ab_b_b0;
					//set expressions
					
					//transTaken_ab_policy_b = 1;
				end 
				else if (A && B) begin
					//transition b1 -> violation on (A and B)
					ab_policy_b_n_state = POLICY_STATE_ab_b_violation;
					//set expressions
					
					//transTaken_ab_policy_b = 1;
				end 
				else if (!(A) && B) begin
					//transition b1 -> violation on (!A and B)
					ab_policy_b_n_state = POLICY_STATE_ab_b_violation;
					//set expressions
					
					//transTaken_ab_policy_b = 1;
				end  else begin
					//only possible in a violation
					ab_policy_b_n_state = POLICY_STATE_ab_b_violation;
					//transTaken_ab_policy_b = 1;
				end
			end
			POLICY_STATE_ab_b_b2: begin
				if (B) begin
					ab_policy_b_n_state = POLICY_STATE_ab_b_b1;
				end
			end
			default begin
				//if we are here, we're in the violation state
				//the violation state permanently stays in violation
				ab_policy_b_n_state = POLICY_STATE_ab_b_violation;
				//transTaken_ab_policy_b = 1;
			end
		endcase
		
	end

	assign ab_policy_b_state_out =  ab_policy_b_c_state;

endmodule

// OUTPUT Select Look Up Table
// Inputs: recovery references from each policy
// Outputs: final signals for outputs (in this example A and B)
module F_LUT_Output_Edit (
		// Outputs (controller to plant) 
		input wire A_ctp_in,
		output reg A_ctp_out, // final

		input wire B_ctp_in,
		output reg B_ctp_out, // final

		input reg [2:0] ab_policy_a_output_recovery_ref,
		input reg [2:0] ab_policy_b_output_recovery_ref,

		input wire clk
	);

	// wire [5:0] recovery_key = 0;
	// assign recovery_key = {ab_policy_a_output_recovery_ref, ab_policy_b_output_recovery_ref};

	reg A = 0;
	reg B = 0;

	initial begin
		A_ctp_out = 0;
		B_ctp_out = 0;
	end

	always @(*) begin
		case({ ab_policy_a_output_recovery_ref, ab_policy_b_output_recovery_ref })
			6'b001001: begin
				A = 1;
				B = 1;
				end
			6'b010001: begin
				A = 1;
				B = 1;
				end
			6'b011001: begin
				A = 0;
				B = 1;
				end
			6'b100001: begin
				A = 0;
				B = 1;
				end
			6'b101001: begin
				A = 0;
				B = 1;
				end
			6'b110001: begin
				A = 0;
				B = 1;
				end
			6'b001010: begin
				A = 1;
				B = 1;
				end
			6'b001011: begin
				A = 1;
				B = 0;
				end
			6'b001100: begin
				A = 1;
				B = 0;
				end
			6'b001101: begin
				A = 1;
				B = 0;
				end
			6'b001110: begin
				A = 1;
				B = 0;
				end
			6'b010010: begin
				A = 1;
				B = 1;
				end
			6'b010011: begin
				A = 1;
				B = 0;
				end
			6'b010100: begin
				A = 1;
				B = 0;
				end
			6'b010101: begin
				A = 1;
				B = 0;
				end
			6'b010110: begin
				A = 1;
				B = 0;
				end
			6'b011010: begin
				A = 0;
				B = 1;
				end
			6'b011011: begin
				A = 1;
				B = 1;
				end
			6'b011100: begin
				A = 0;
				B = 0;
				end
			6'b011101: begin
				A = 1;
				B = 0;
				end
			6'b011110: begin
				A = 1;
				B = 0;
				end
			6'b100010: begin
				A = 0;
				B = 1;
				end
			6'b100011: begin
				A = 0;
				B = 0;
				end
			6'b100100: begin
				A = 0;
				B = 0;
				end
			6'b100101: begin
				A = 0;
				B = 0;
				end
			6'b100110: begin
				A = 0;
				B = 0;
				end
			6'b101010: begin
				A = 0;
				B = 1;
				end
			6'b101011: begin
				A = 0;
				B = 1;
				end
			6'b101100: begin
				A = 0;
				B = 0;
				end
			6'b101101: begin
				A = 0;
				B = 0;
				end
			6'b101110: begin
				A = 0;
				B = 0;
				end
			6'b110010: begin
				A = 1;
				B = 0;
				end
			6'b110011: begin
				A = 0;
				B = 1;
				end
			6'b110100: begin
				A = 0;
				B = 0;
				end
			6'b110101: begin
				A = 0;
				B = 0;
				end
			6'b110110: begin
				A = 0;
				B = 0;
				end

			default: begin
					A = A_ctp_in;
					B = B_ctp_in;
				end
		endcase

		A_ctp_out = A;
		B_ctp_out = B;
	end

endmodule

