import os
import shutil
import datetime
import subprocess
from parse import * # pip install parse

projectDir = "D:\\github.com\\AlexBaird\\easy-rte-composition\\example"
os.chdir(projectDir)
basedir = "incrementalDronesBool" 

# Get all compiled directories (assumption that "compiled_parallel" is directory prefix)
compiledDirectories = []
dir_list = os.listdir(basedir)
for thing in dir_list:
    if thing.startswith("c_"): #and thing.endswith(""):
        compiledDirectories.append(thing)

results = []
for dir in compiledDirectories:
    # print(dir)

    # Find all files in directory
    files = []
    filesInDir = os.listdir(basedir + "\\" + dir)
    topLevelName = None
    for file in filesInDir:
        if file.endswith(".sv"):
            topLevelName = file.replace(".sv", "")
            break
    assert(topLevelName is not None)
    print(topLevelName)

    resultRow = {}
    resultRow['topLevelName'] = topLevelName

    # parallel_F_pb.fit.summary is LU and regs and pins
    fitFileName = topLevelName + ".fit.summary"
    with open(basedir + "\\" + dir + "\\" + fitFileName, "r") as f:
        line = f.readline()
        while not line.startswith("Logic utilization (in ALMs) :"):
            line = f.readline()
            if line == "":
                print("Line not found")
                break
        
        # Logic utilization (in ALMs) : 11 / 56,480 ( < 1 % )
        # Total registers : 33
        # Total pins : 49 / 268 ( 18 % )

        les = int(parse("Logic utilization (in ALMs) : {} / {}", line)[0])
        print("LEs :", les)
        resultRow["les"] = les

        line = f.readline()
        regs = int(parse("Total registers : {}", line)[0])
        print("Regs :", regs)
        resultRow["regs"] = regs

        line = f.readline()
        pins = int(parse("Total pins : {} / {} ( {}", line)[0])
        print("Pins :", pins)
        resultRow["pins"] = pins

    # parallel_F_pb.flow.rpt is flow time (aka compile time)
    staFileName = topLevelName + ".flow.rpt"
    with open(basedir + "\\" + dir + "\\" + staFileName, "r") as f:
        line = f.readline()
        while not line.startswith("; Flow Elapsed Time"):
            line = f.readline()
            if line == "":
                print("Line not found")
                break
        # +--------------------------------------------------------------------------------------------------------------------------+
        # ; Flow Elapsed Time                                                                                                        ;
        # +----------------------+--------------+-------------------------+---------------------+------------------------------------+
        # ; Module Name          ; Elapsed Time ; Average Processors Used ; Peak Virtual Memory ; Total CPU Time (on all processors) ;
        # +----------------------+--------------+-------------------------+---------------------+------------------------------------+
        # ; Analysis & Synthesis ; 00:00:09     ; 1.0                     ; 4838 MB             ; 00:00:01                           ;
        # ; Fitter               ; 00:00:34     ; 1.0                     ; 6662 MB             ; 00:01:06                           ;
        # ; Timing Analyzer      ; 00:00:02     ; 1.0                     ; 4956 MB             ; 00:00:02                           ;
        # ; Total                ; 00:00:45     ; --                      ; --                  ; 00:01:09                           ;
        # +----------------------+--------------+-------------------------+---------------------+------------------------------------+
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()

        line = line.replace(" ", "")

        # allTimes = parse(";Total;{};{};{};{};", line)
        allTimes = line.split(";")
        wallTime = allTimes[2]
        cpuTime = allTimes[-2]

        print("Wall time:", wallTime)
        print("CPU time:", cpuTime)
        resultRow["cpuTime"] = cpuTime
        resultRow["wallTime"] = wallTime



    # parallel_F_pb.sta.rpt is Fmax
    staFileName = topLevelName + ".sta.rpt"
    with open(basedir + "\\" + dir + "\\" + staFileName, "r") as f:
        line = f.readline()
        while not line.startswith("; Fmax Summary                                     ;"):
            line = f.readline()
            if line == "":
                print("Line not found")
                break
        
        # +--------------------------------------------------+
        # ; Fmax Summary                                     ;
        # +------------+-----------------+------------+------+
        # ; Fmax       ; Restricted Fmax ; Clock Name ; Note ;
        # +------------+-----------------+------------+------+
        # ; 234.25 MHz ; 234.25 MHz      ; clk        ;      ;
        # +------------+-----------------+------------+------+
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()

        try:
            fmax = float(parse("; {} MHz {}", line)[0])
        except:
            fmax = None
        print("FMax :", fmax)
        resultRow["fmax"] = fmax

    results.append(resultRow)

import csv
with open(basedir+'\\'+'compilation_summary.csv','w', newline='') as f:
    w = csv.DictWriter(f,results[0].keys())
    w.writeheader()
    # for row in results:
    w.writerows(results)