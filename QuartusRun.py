
import os
import shutil
import datetime
import subprocess

def generate_tcl_mon(fname):
  fp = open(fname + ".tcl", "w")

  string = """
	# Load Quartus Prime Tcl Project package
	package require ::quartus::project

	set need_to_close_project 0
	set make_assignments 1

	# Check that the right project is open
	if {[is_project_open]} {
		if {[string compare $quartus(project) """ + "/" + fname + "/" + """ ]} {
			puts "Project  """+ fname +""" is not open"
			set make_assignments 0
		}
	} else {
		# Only open if not already open
		if {[project_exists  """+ fname +"""]} {
			project_open -revision """+ fname.replace("_", "") +""" """+ fname +"""
		} else {
			project_new -revision """+ fname.replace("_", "") +""" """+ fname +"""
		}
		set need_to_close_project 1
	}

	# Make assignments
	if {$make_assignments} {
		set_global_assignment -name FAMILY "Cyclone IV E"
		set_global_assignment -name DEVICE EP4CE115F29C7
		set_global_assignment -name TOP_LEVEL_ENTITY """ + fname.replace("_", "") + """
		set_global_assignment -name ORIGINAL_QUARTUS_VERSION 21.1.0
		set_global_assignment -name PROJECT_CREATION_TIME_DATE " """ + datetime.datetime.now().strftime("%H:%M:%S %B %d, %Y ") + """ "
		set_global_assignment -name LAST_QUARTUS_VERSION "21.1.0 Lite Edition"
		set_global_assignment -name PROJECT_OUTPUT_DIRECTORY output_files
		set_global_assignment -name MIN_CORE_JUNCTION_TEMP 0
		set_global_assignment -name MAX_CORE_JUNCTION_TEMP 85
		set_global_assignment -name ERROR_CHECK_FREQUENCY_DIVISOR 1
		set_global_assignment -name NOMINAL_CORE_SUPPLY_VOLTAGE 1.2V
		set_global_assignment -name POWER_PRESET_COOLING_SOLUTION "23 MM HEAT SINK WITH 200 LFPM AIRFLOW"
		set_global_assignment -name POWER_BOARD_THERMAL_MODEL "NONE (CONSERVATIVE)"
		set_global_assignment -name EDA_SIMULATION_TOOL "ModelSim (Verilog)"
		set_global_assignment -name EDA_TIME_SCALE "1 ps" -section_id eda_simulation
		set_global_assignment -name EDA_RUN_TOOL_AUTOMATICALLY OFF -section_id eda_simulation
		set_global_assignment -name EDA_OUTPUT_DATA_FORMAT "VERILOG HDL" -section_id eda_simulation
		set_global_assignment -name EDA_GENERATE_FUNCTIONAL_NETLIST OFF -section_id eda_board_design_timing
		set_global_assignment -name EDA_GENERATE_FUNCTIONAL_NETLIST OFF -section_id eda_board_design_symbol
		set_global_assignment -name EDA_GENERATE_FUNCTIONAL_NETLIST OFF -section_id eda_board_design_signal_integrity
		set_global_assignment -name EDA_GENERATE_FUNCTIONAL_NETLIST OFF -section_id eda_board_design_boundary_scan
		set_global_assignment -name EDA_DESIGN_ENTRY_SYNTHESIS_TOOL "Precision Synthesis"
		set_global_assignment -name EDA_LMF_FILE mentor.lmf -section_id eda_design_synthesis
		set_global_assignment -name EDA_INPUT_DATA_FORMAT VQM -section_id eda_design_synthesis
		set_global_assignment -name ALLOW_REGISTER_RETIMING ON
		set_global_assignment -name SYSTEMVERILOG_FILE "../../../github.com/AlexBaird/easy-rte-composition/example/pacemaker/parallel_F_p1.sv"
		set_global_assignment -name PARTITION_NETLIST_TYPE SOURCE -section_id Top
		set_global_assignment -name PARTITION_FITTER_PRESERVATION_LEVEL PLACEMENT_AND_ROUTING -section_id Top
		set_global_assignment -name PARTITION_COLOR 16764057 -section_id Top

		# Commit assignments
		export_assignments

		# Close project
		if {$need_to_close_project} {
			project_close
		}
	}
	"""
  fp.write(string)
  fp.close()

def log(path, file, textToLog):
	with open(path+"\\"+file+'.txt', 'a') as f:
		s = ("{}".format(textToLog))
		f.write(s)

if __name__ == "__main__":  

	quartusDir = "M:\\Software\\Quartus\\quartus\\bin64\\"
	# projectDir = "C:\\Users\\Alex\\Downloads\\Quartus"
	projectDir = "D:\\github.com\\AlexBaird\\easy-rte-composition\\example"
	os.chdir(projectDir)
	basedir = "incrementalDronesBool" 

	files = []
	dir_list = os.listdir(basedir)
	for thing in dir_list:
		if thing.startswith("parallel") and thing.endswith(".sv"):
			files.append(thing.replace(".sv",""))

	# Setup folder for compilation
	for file in files:
		try:
			os.mkdir(basedir + "\\compiled_" + file)
		except:
			pass

		shutil.copyfile(projectDir+"\\"+basedir+"\\"+file+".sv", projectDir+"\\"+basedir+"\\compiled_"+file+"\\"+file+".sv")

	# Perform compilation
	for file in files:
		print(file)

		# os.chdir(basedir + "/" + "Monolithic")
		os.chdir(basedir + "\\compiled_" + file)

		direc = basedir #+"_new"+ str(j+2) + "neurons"
		# print(direc)
		# os.chdir(direc)

		generate_tcl_mon(direc)
		tcl_file = direc + ".tcl"
		top_level_entity = file + ".sv"

		processesToRun = [
			[quartusDir + "quartus_sh.exe", "-t", tcl_file],
			[quartusDir + "quartus_map.exe", top_level_entity],
			[quartusDir + "quartus_fit.exe", top_level_entity],
			[quartusDir + "quartus_sta.exe", top_level_entity, "--model=slow"]
		]

		for process in processesToRun:
			with open(projectDir+"\\"+basedir+"\\compiled_"+file+"\\log.txt", 'a') as f:
				try:
					subprocess.run(process, stdout=f, universal_newlines=True)
				except:
					pass
        
		os.chdir("..\\..")
