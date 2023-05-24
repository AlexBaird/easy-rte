./easy-rte-parser -i example/incrementalDronesBool/pb.erte -o example/incrementalDronesBool/pb.xml


# Step 1 - Monolithic Composition XML File
Make sure any existing XML files are deleted
Otherwise when you run step 2 the XML file will not be recreated

# Step 2 - Compile Verilog
make verilog_enf PROJECT=incrementalDronesBool FILE=pb PARSEARGS=-product COMPILEARGS=-synthesis

# Batch
make verilog_enf PROJECT=incrementalDronesBool FILE=pb PARSEARGS=-product COMPILEARGS=-synthesis
make verilog_enf PROJECT=incrementalDronesBool FILE=pb_and_ps PARSEARGS=-product COMPILEARGS=-synthesis
make verilog_enf PROJECT=incrementalDronesBool FILE=pb_and_ps_and_pj PARSEARGS=-product COMPILEARGS=-synthesis
make verilog_enf PROJECT=incrementalDronesBool FILE=pb_and_ps_and_pj_and_pr PARSEARGS=-product COMPILEARGS=-synthesis
make verilog_enf PROJECT=incrementalDronesBool FILE=pb_and_ps_and_pj_and_pr_and_pb2 PARSEARGS=-product COMPILEARGS=-synthesis
make verilog_enf PROJECT=incrementalDronesBool FILE=pb_and_ps_and_pj_and_pr_and_pb2_and_ps2 PARSEARGS=-product COMPILEARGS=-synthesis
make verilog_enf PROJECT=incrementalDronesBool FILE=pb_and_ps_and_pj_and_pr_and_pb2_and_ps2_and_pj2 PARSEARGS=-product COMPILEARGS=-synthesis
make verilog_enf PROJECT=incrementalDronesBool FILE=pb_and_ps_and_pj_and_pr_and_pb2_and_ps2_and_pj2_and_pr2 PARSEARGS=-product COMPILEARGS=-synthesis
make verilog_enf PROJECT=incrementalDronesBool FILE=pb_and_ps_and_pj_and_pr_and_pb2_and_ps2_and_pj2_and_pr2_and_pd PARSEARGS=-product COMPILEARGS=-synthesis
