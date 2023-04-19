./easy-rte-parser -i example/incrementalDronesBool/pb.erte -o example/incrementalDronesBool/pb.xml
python rtecomp/main.py incrementalDronesBool pb
make verilog_enf PROJECT=incrementalDronesBool FILE=pb_modified COMPILEARGS=-synthesis

./easy-rte-parser -i example/incrementalDronesBool/pb_and_ps.erte -o example/incrementalDronesBool/pb_and_ps.xml
python rtecomp/main.py incrementalDronesBool pb_and_ps
make verilog_enf PROJECT=incrementalDronesBool FILE=pb_and_ps_modified COMPILEARGS=-synthesis

./easy-rte-parser -i example/incrementalDronesBool/pb_and_ps_and_pj.erte -o example/incrementalDronesBool/pb_and_ps_and_pj.xml
python rtecomp/main.py incrementalDronesBool pb_and_ps_and_pj
make verilog_enf PROJECT=incrementalDronesBool FILE=pb_and_ps_and_pj_modified COMPILEARGS=-synthesis

./easy-rte-parser -i example/incrementalDronesBool/pb_and_ps_and_pj_and_pr.erte -o example/incrementalDronesBool/pb_and_ps_and_pj_and_pr.xml
python rtecomp/main.py incrementalDronesBool pb_and_ps_and_pj_and_pr
make verilog_enf PROJECT=incrementalDronesBool FILE=pb_and_ps_and_pj_and_pr_modified COMPILEARGS=-synthesis

