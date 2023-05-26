# Readme Profiling rtec main

1. Install profiler tool (`go get github.com/pkg/profile`)
1. Enable profiling in rtec/main.go
    - CPU Profiling: `defer profile.Start().Stop()`
    - Memory Profiling: `defer profile.Start(profile.MemProfile).Stop()`
2. Build (`make local`)
3. Run (`make verilog_enf PROJECT=Printer_3D FILE=Printer_3D_5 PARSEARGS=-product COMPILEARGS=-synthesis`)
    - Make note of the output pprof file 
    - Example: 
        - `2023/05/25 11:37:26 profile: cpu profiling disabled, /tmp/profile4262808058/cpu.pprof`
        - You need: `/tmp/profile4262808058/cpu.pprof`
4. For graphical output install graphviz (pdf visualisation) (`apt install graphviz` works on WSL too)
5.  Run
    - PDF Visualisation:
        - `go tool pprof --pdf easy-rte-c /tmp/[CHANGE ME]/cpu.pprof > prof_cpu_Printer_3D_5.pdf`
    - Text File:
        - `go tool pprof --text easy-rte-c /tmp/profile124250000/mem.pprof > prof_mem_Printer_3D_5.txt`

_Source: this guide was used - https://flaviocopes.com/golang-profiling/_

## Examples
go tool pprof --pdf easy-rte-parser URL >    rtec/profiling/serial/prof_cpu_parser_Printer_3D_1.pdf
go tool pprof --text easy-rte-parser URL >   rtec/profiling/serial/prof_cpu_parser_Printer_3D_1.txt

go tool pprof --pdf easy-rte-c /tmp/profile193268262/cpu.pprof >    rtec/profiling/serial/prof_cpu_c_Printer_3D_1.pdf
go tool pprof --text easy-rte-c /tmp/profile193268262/cpu.pprof >   rtec/profiling/serial/prof_cpu_c_Printer_3D_1.txt

go tool pprof --pdf easy-rte-parser URL >    rtec/profiling/serial/prof_cpu_parser_Printer_3D_2.pdf
go tool pprof --text easy-rte-parser URL >   rtec/profiling/serial/prof_cpu_parser_Printer_3D_2.txt

go tool pprof --pdf easy-rte-c /tmp/profile2888591762/cpu.pprof >    rtec/profiling/serial/prof_cpu_c_Printer_3D_2.pdf
go tool pprof --text easy-rte-c /tmp/profile2888591762/cpu.pprof >   rtec/profiling/serial/prof_cpu_c_Printer_3D_2.txt

go tool pprof --pdf easy-rte-parser URL >    rtec/profiling/serial/prof_cpu_parser_Printer_3D_3.pdf
go tool pprof --text easy-rte-parser URL >   rtec/profiling/serial/prof_cpu_parser_Printer_3D_3.txt

go tool pprof --pdf easy-rte-c /tmp/profile3802877529/cpu.pprof >    rtec/profiling/serial/prof_cpu_c_Printer_3D_3.pdf
go tool pprof --text easy-rte-c /tmp/profile3802877529/cpu.pprof >   rtec/profiling/serial/prof_cpu_c_Printer_3D_3.txt

go tool pprof --pdf easy-rte-parser URL >    rtec/profiling/serial/prof_cpu_parser_Printer_3D_4.pdf
go tool pprof --text easy-rte-parser URL >   rtec/profiling/serial/prof_cpu_parser_Printer_3D_4.txt

go tool pprof --pdf easy-rte-c /tmp/profile1916642571/cpu.pprof >    rtec/profiling/serial/prof_cpu_c_Printer_3D_4.pdf
go tool pprof --text easy-rte-c /tmp/profile1916642571/cpu.pprof >   rtec/profiling/serial/prof_cpu_c_Printer_3D_4.txt

go tool pprof --pdf easy-rte-parser URL >    rtec/profiling/serial/prof_cpu_parser_Printer_3D_5.pdf
go tool pprof --text easy-rte-parser URL >   rtec/profiling/serial/prof_cpu_parser_Printer_3D_5.txt

go tool pprof --pdf easy-rte-c /tmp/profile3611809586/cpu.pprof >    rtec/profiling/serial/prof_cpu_c_Printer_3D_5.pdf
go tool pprof --text easy-rte-c /tmp/profile3611809586/cpu.pprof >   rtec/profiling/serial/prof_cpu_c_Printer_3D_5.txt

go tool pprof --pdf easy-rte-parser URL >    rtec/profiling/serial/prof_cpu_parser_Printer_3D_6.pdf
go tool pprof --text easy-rte-parser URL >   rtec/profiling/serial/prof_cpu_parser_Printer_3D_6.txt

go tool pprof --pdf easy-rte-c /tmp/profile2572985671/cpu.pprof >    rtec/profiling/serial/prof_cpu_c_Printer_3D_6.pdf
go tool pprof --text easy-rte-c /tmp/profile2572985671/cpu.pprof >   rtec/profiling/serial/prof_cpu_c_Printer_3D_6.txt

go tool pprof --pdf easy-rte-parser URL >    rtec/profiling/serial/prof_cpu_parser_Printer_3D_7.pdf
go tool pprof --text easy-rte-parser URL >   rtec/profiling/serial/prof_cpu_parser_Printer_3D_7.txt

go tool pprof --pdf easy-rte-c /tmp/profile989126581/cpu.pprof >    rtec/profiling/serial/prof_cpu_c_Printer_3D_7.pdf
go tool pprof --text easy-rte-c /tmp/profile989126581/cpu.pprof >   rtec/profiling/serial/prof_cpu_c_Printer_3D_7.txt

go tool pprof --pdf easy-rte-parser URL >    rtec/profiling/serial/prof_cpu_parser_Printer_3D_8.pdf
go tool pprof --text easy-rte-parser URL >   rtec/profiling/serial/prof_cpu_parser_Printer_3D_8.txt

go tool pprof --pdf easy-rte-c /tmp/profile3339226909/cpu.pprof >    rtec/profiling/serial/prof_cpu_c_Printer_3D_8.pdf
go tool pprof --text easy-rte-c /tmp/profile3339226909/cpu.pprof >   rtec/profiling/serial/prof_cpu_c_Printer_3D_8.txt

go tool pprof --pdf easy-rte-parser URL >    rtec/profiling/serial/prof_cpu_parser_Printer_3D_9.pdf
go tool pprof --text easy-rte-parser URL >   rtec/profiling/serial/prof_cpu_parser_Printer_3D_9.txt

go tool pprof --pdf easy-rte-c /tmp/profile546692640/cpu.pprof >    rtec/profiling/serial/prof_cpu_c_Printer_3D_9.pdf
go tool pprof --text easy-rte-c /tmp/profile546692640/cpu.pprof >   rtec/profiling/serial/prof_cpu_c_Printer_3D_9.txt

go tool pprof --pdf easy-rte-parser URL >    rtec/profiling/serial/prof_cpu_parser_Printer_3D_10.pdf
go tool pprof --text easy-rte-parser URL >   rtec/profiling/serial/prof_cpu_parser_Printer_3D_10.txt

go tool pprof --pdf easy-rte-c /tmp/profile4232059260/cpu.pprof >    rtec/profiling/serial/prof_cpu_c_Printer_3D_10.pdf
go tool pprof --text easy-rte-c /tmp/profile4232059260/cpu.pprof >   rtec/profiling/serial/prof_cpu_c_Printer_3D_10.txt

##########################################################

go tool pprof --pdf easy-rte-parser /tmp/profile4066190099/cpu.pprof >    rtec/profiling/parallel/prof_cpu_parser_Printer_3D_1.pdf
go tool pprof --text easy-rte-parser /tmp/profile4066190099/cpu.pprof >   rtec/profiling/parallel/prof_cpu_parser_Printer_3D_1.txt
go tool pprof --pdf easy-rte-c /tmp/profile4108432407/cpu.pprof >    rtec/profiling/parallel/prof_cpu_c_Printer_3D_1.pdf
go tool pprof --text easy-rte-c /tmp/profile4108432407/cpu.pprof >   rtec/profiling/parallel/prof_cpu_c_Printer_3D_1.txt


go tool pprof --pdf easy-rte-parser /tmp/profile219508670/cpu.pprof >    rtec/profiling/parallel/prof_cpu_parser_Printer_3D_2.pdf
go tool pprof --text easy-rte-parser /tmp/profile219508670/cpu.pprof >   rtec/profiling/parallel/prof_cpu_parser_Printer_3D_2.txt
go tool pprof --pdf easy-rte-c /tmp/profile3694088205/cpu.pprof >    rtec/profiling/parallel/prof_cpu_c_Printer_3D_2.pdf
go tool pprof --text easy-rte-c /tmp/profile3694088205/cpu.pprof >   rtec/profiling/parallel/prof_cpu_c_Printer_3D_2.txt


go tool pprof --pdf easy-rte-parser /tmp/profile2708860939/cpu.pprof >    rtec/profiling/parallel/prof_cpu_parser_Printer_3D_3.pdf
go tool pprof --text easy-rte-parser /tmp/profile2708860939/cpu.pprof >   rtec/profiling/parallel/prof_cpu_parser_Printer_3D_3.txt
go tool pprof --pdf easy-rte-c /tmp/profile2166879467/cpu.pprof >    rtec/profiling/parallel/prof_cpu_c_Printer_3D_3.pdf
go tool pprof --text easy-rte-c /tmp/profile2166879467/cpu.pprof >   rtec/profiling/parallel/prof_cpu_c_Printer_3D_3.txt



go tool pprof --pdf easy-rte-parser /tmp/profile901738375/cpu.pprof >    rtec/profiling/parallel/prof_cpu_parser_Printer_3D_4.pdf
go tool pprof --text easy-rte-parser /tmp/profile901738375/cpu.pprof >   rtec/profiling/parallel/prof_cpu_parser_Printer_3D_4.txt
go tool pprof --pdf easy-rte-c /tmp/profile986779737/cpu.pprof >    rtec/profiling/parallel/prof_cpu_c_Printer_3D_4.pdf
go tool pprof --text easy-rte-c /tmp/profile986779737/cpu.pprof >   rtec/profiling/parallel/prof_cpu_c_Printer_3D_4.txt



go tool pprof --pdf easy-rte-parser /tmp/profile1459818940/cpu.pprof >    rtec/profiling/parallel/prof_cpu_parser_Printer_3D_5.pdf
go tool pprof --text easy-rte-parser /tmp/profile1459818940/cpu.pprof >   rtec/profiling/parallel/prof_cpu_parser_Printer_3D_5.txt
go tool pprof --pdf easy-rte-c /tmp/profile2906846023/cpu.pprof >    rtec/profiling/parallel/prof_cpu_c_Printer_3D_5.pdf
go tool pprof --text easy-rte-c /tmp/profile2906846023/cpu.pprof >   rtec/profiling/parallel/prof_cpu_c_Printer_3D_5.txt



go tool pprof --pdf easy-rte-parser /tmp/profile547411694/cpu.pprof >    rtec/profiling/parallel/prof_cpu_parser_Printer_3D_6.pdf
go tool pprof --text easy-rte-parser /tmp/profile547411694/cpu.pprof >   rtec/profiling/parallel/prof_cpu_parser_Printer_3D_6.txt
go tool pprof --pdf easy-rte-c /tmp/profile3078877054/cpu.pprof >    rtec/profiling/parallel/prof_cpu_c_Printer_3D_6.pdf
go tool pprof --text easy-rte-c /tmp/profile3078877054/cpu.pprof >   rtec/profiling/parallel/prof_cpu_c_Printer_3D_6.txt


go tool pprof --pdf easy-rte-parser /tmp/profile117902317/cpu.pprof >    rtec/profiling/parallel/prof_cpu_parser_Printer_3D_7.pdf
go tool pprof --text easy-rte-parser /tmp/profile117902317/cpu.pprof >   rtec/profiling/parallel/prof_cpu_parser_Printer_3D_7.txt
go tool pprof --pdf easy-rte-c /tmp/profile3096250762/cpu.pprof >    rtec/profiling/parallel/prof_cpu_c_Printer_3D_7.pdf
go tool pprof --text easy-rte-c /tmp/profile3096250762/cpu.pprof >   rtec/profiling/parallel/prof_cpu_c_Printer_3D_7.txt


go tool pprof --pdf easy-rte-parser /tmp/profile3873093002/cpu.pprof >    rtec/profiling/parallel/prof_cpu_parser_Printer_3D_8.pdf
go tool pprof --text easy-rte-parser /tmp/profile3873093002/cpu.pprof >   rtec/profiling/parallel/prof_cpu_parser_Printer_3D_8.txt

go tool pprof --pdf easy-rte-c /tmp/profile252846961/cpu.pprof >    rtec/profiling/parallel/prof_cpu_c_Printer_3D_8.pdf
go tool pprof --text easy-rte-c /tmp/profile252846961/cpu.pprof >   rtec/profiling/parallel/prof_cpu_c_Printer_3D_8.txt


go tool pprof --pdf easy-rte-parser /tmp/profile1011021791/cpu.pprof >    rtec/profiling/parallel/prof_cpu_parser_Printer_3D_9.pdf
go tool pprof --text easy-rte-parser /tmp/profile1011021791/cpu.pprof >   rtec/profiling/parallel/prof_cpu_parser_Printer_3D_9.txt

go tool pprof --pdf easy-rte-c /tmp/profile487105877/cpu.pprof >    rtec/profiling/parallel/prof_cpu_c_Printer_3D_9.pdf
go tool pprof --text easy-rte-c /tmp/profile487105877/cpu.pprof >   rtec/profiling/parallel/prof_cpu_c_Printer_3D_9.txt


go tool pprof --pdf easy-rte-parser /tmp/profile327009695/cpu.pprof >    rtec/profiling/parallel/prof_cpu_parser_Printer_3D_10.pdf
go tool pprof --text easy-rte-parser /tmp/profile327009695/cpu.pprof >   rtec/profiling/parallel/prof_cpu_parser_Printer_3D_10.txt

go tool pprof --pdf easy-rte-c /tmp/profile414438103/cpu.pprof >    rtec/profiling/parallel/prof_cpu_c_Printer_3D_10.pdf
go tool pprof --text easy-rte-c /tmp/profile414438103/cpu.pprof >   rtec/profiling/parallel/prof_cpu_c_Printer_3D_10.txt


##########################################################

go tool pprof --pdf easy-rte-parser /tmp/profile3292405279/cpu.pprof >    rtec/profiling/monolithic/prof_cpu_parser_Printer_3D_1.pdf
go tool pprof --text easy-rte-parser /tmp/profile3292405279/cpu.pprof >   rtec/profiling/monolithic/prof_cpu_parser_Printer_3D_1.txt
go tool pprof --pdf easy-rte-c /tmp/profile3200846095/cpu.pprof >    rtec/profiling/monolithic/prof_cpu_c_Printer_3D_1.pdf
go tool pprof --text easy-rte-c /tmp/profile3200846095/cpu.pprof >   rtec/profiling/monolithic/prof_cpu_c_Printer_3D_1.txt

go tool pprof --pdf easy-rte-parser /tmp/profile2097256306/cpu.pprof >    rtec/profiling/monolithic/prof_cpu_parser_Printer_3D_2.pdf
go tool pprof --text easy-rte-parser /tmp/profile2097256306/cpu.pprof >   rtec/profiling/monolithic/prof_cpu_parser_Printer_3D_2.txt
go tool pprof --pdf easy-rte-c /tmp/profile3461918016/cpu.pprof >    rtec/profiling/monolithic/prof_cpu_c_Printer_3D_2.pdf
go tool pprof --text easy-rte-c /tmp/profile3461918016/cpu.pprof >   rtec/profiling/monolithic/prof_cpu_c_Printer_3D_2.txt

go tool pprof --pdf easy-rte-parser /tmp/profile1176596594/cpu.pprof >    rtec/profiling/monolithic/prof_cpu_parser_Printer_3D_3.pdf
go tool pprof --text easy-rte-parser /tmp/profile1176596594/cpu.pprof >   rtec/profiling/monolithic/prof_cpu_parser_Printer_3D_3.txt
go tool pprof --pdf easy-rte-c /tmp/profile480890251/cpu.pprof >    rtec/profiling/monolithic/prof_cpu_c_Printer_3D_3.pdf
go tool pprof --text easy-rte-c /tmp/profile480890251/cpu.pprof >   rtec/profiling/monolithic/prof_cpu_c_Printer_3D_3.txt

go tool pprof --pdf easy-rte-parser /tmp/profile3141043753/cpu.pprof >    rtec/profiling/monolithic/prof_cpu_parser_Printer_3D_4.pdf
go tool pprof --text easy-rte-parser /tmp/profile3141043753/cpu.pprof >   rtec/profiling/monolithic/prof_cpu_parser_Printer_3D_4.txt
go tool pprof --pdf easy-rte-c /tmp/profile2228727628/cpu.pprof >    rtec/profiling/monolithic/prof_cpu_c_Printer_3D_4.pdf
go tool pprof --text easy-rte-c /tmp/profile2228727628/cpu.pprof >   rtec/profiling/monolithic/prof_cpu_c_Printer_3D_4.txt

go tool pprof --pdf easy-rte-parser /tmp/profile1984848916/cpu.pprof >    rtec/profiling/monolithic/prof_cpu_parser_Printer_3D_5.pdf
go tool pprof --text easy-rte-parser /tmp/profile1984848916/cpu.pprof >   rtec/profiling/monolithic/prof_cpu_parser_Printer_3D_5.txt
go tool pprof --pdf easy-rte-c /tmp/profile1231221460/cpu.pprof >    rtec/profiling/monolithic/prof_cpu_c_Printer_3D_5.pdf
go tool pprof --text easy-rte-c /tmp/profile1231221460/cpu.pprof >   rtec/profiling/monolithic/prof_cpu_c_Printer_3D_5.txt

go tool pprof --pdf easy-rte-parser /tmp/profile2875998266/cpu.pprof >    rtec/profiling/monolithic/prof_cpu_parser_Printer_3D_6.pdf
go tool pprof --text easy-rte-parser /tmp/profile2875998266/cpu.pprof >   rtec/profiling/monolithic/prof_cpu_parser_Printer_3D_6.txt
go tool pprof --pdf easy-rte-c /tmp/profile3750821408/cpu.pprof >    rtec/profiling/monolithic/prof_cpu_c_Printer_3D_6.pdf
go tool pprof --text easy-rte-c /tmp/profile3750821408/cpu.pprof >   rtec/profiling/monolithic/prof_cpu_c_Printer_3D_6.txt


// Maybe no futher than this
go tool pprof --pdf easy-rte-parser URL >    rtec/profiling/monolithic/prof_cpu_parser_Printer_3D_7.pdf
go tool pprof --text easy-rte-parser URL >   rtec/profiling/monolithic/prof_cpu_parser_Printer_3D_7.txt
go tool pprof --pdf easy-rte-c URL >    rtec/profiling/monolithic/prof_cpu_c_Printer_3D_7.pdf
go tool pprof --text easy-rte-c URL >   rtec/profiling/monolithic/prof_cpu_c_Printer_3D_7.txt

go tool pprof --pdf easy-rte-parser URL >    rtec/profiling/monolithic/prof_cpu_parser_Printer_3D_8.pdf
go tool pprof --text easy-rte-parser URL >   rtec/profiling/monolithic/prof_cpu_parser_Printer_3D_8.txt
go tool pprof --pdf easy-rte-c URL >    rtec/profiling/monolithic/prof_cpu_c_Printer_3D_8.pdf
go tool pprof --text easy-rte-c URL >   rtec/profiling/monolithic/prof_cpu_c_Printer_3D_8.txt
go tool pprof --pdf easy-rte-parser URL >    rtec/profiling/monolithic/prof_cpu_parser_Printer_3D_9.pdf
go tool pprof --text easy-rte-parser URL >   rtec/profiling/monolithic/prof_cpu_parser_Printer_3D_9.txt
go tool pprof --pdf easy-rte-c URL >    rtec/profiling/monolithic/prof_cpu_c_Printer_3D_9.pdf
go tool pprof --text easy-rte-c URL >   rtec/profiling/monolithic/prof_cpu_c_Printer_3D_9.txt
go tool pprof --pdf easy-rte-parser URL >    rtec/profiling/monolithic/prof_cpu_parser_Printer_3D_10.pdf
go tool pprof --text easy-rte-parser URL >   rtec/profiling/monolithic/prof_cpu_parser_Printer_3D_10.txt
go tool pprof --pdf easy-rte-c URL >    rtec/profiling/monolithic/prof_cpu_c_Printer_3D_10.pdf
go tool pprof --text easy-rte-c URL >   rtec/profiling/monolithic/prof_cpu_c_Printer_3D_10.txt





go tool pprof --pdf easy-rte-c /tmp/profile1294735486/cpu.pprof > rtec/profiling/prof_cpu_Printer_3D_4_mod2.pdf
go tool pprof --text easy-rte-c /tmp/profile1294735486/cpu.pprof > rtec/profiling/prof_cpu_Printer_3D_4_mod2.txt

go tool pprof --text easy-rte-c /tmp/profile124250000/mem.pprof > rtec/profiling/prof_mem_Printer_3D_6.txt
go tool pprof --pdf easy-rte-c /tmp/profile124250000/mem.pprof > rtec/profiling/prof_mem_Printer_3D_6.pdf
