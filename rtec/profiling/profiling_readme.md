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
