package main

import (
	"encoding/xml"
	"flag"
	"fmt"
	"io/ioutil"
	"os"
	"strings"

	"github.com/PRETgroup/easy-rte/rtedef"

	"github.com/PRETgroup/easy-rte/rtec"
	
	"github.com/pkg/profile"
)

var (
	inFileName          = flag.String("i", "", "Specifies the name of the source xml file to be compiled.")
	outLocation         = flag.String("o", "", "Specifies the name of the directory to put output files. If blank, uses current directory")
	language            = flag.String("l", "c", "The output language")
	serialComposition 	= flag.Bool("serialComposition", false, "(Experimental, Verilog Only) Set this to true to produce a serial composition of enforcers. Mutually exclusive with parallelComposition.")
	parallelComposition = flag.Bool("parallelComposition", false, "(Experimental, Verilog Only) Set this to true to produce a parallel composition of enforcers. Mutually exclusive with serialComposition.")
	synthesis           = flag.Bool("synthesis", false, "(Experimental, Verilog Only) Set this to true to produce Verilog which is compatible with ModelSim simulation and Quartus for hardware synthesis.")
)

func main() {
	defer profile.Start().Stop() // CPU PROFILING
	// defer profile.Start(profile.MemProfile).Stop() // MEMORY PROFILING

	flag.Parse()

	*outLocation = strings.TrimSuffix(*outLocation, "/")
	*outLocation = strings.TrimSuffix(*outLocation, "\\")

	if *inFileName == "" {
		fmt.Println("You need to specify a file or directory name to compile! Check out -help for options")
		return

	}

	// fileInfo, err := os.Stat(*inFileName)
	// if err != nil {
	// 	fmt.Println("Error reading file statistics:", err.Error())
	// 	return
	// }

	conv, err := rtec.New(*language, *serialComposition, *parallelComposition, *synthesis)
	if err != nil {
		fmt.Println("Error creating converter:", err.Error())
		return
	}

	//var xmlFileNames []string

	// if fileInfo.IsDir() {
	// 	fmt.Println("Running in Dir mode")
	// 	files, err := ioutil.ReadDir(*inFileName)
	// 	if err != nil {
	// 		log.Fatal(err)
	// 	}

	// 	for _, file := range files {
	// 		//only read the .fbt and .res files
	// 		name := file.Name()
	// 		nameComponents := strings.Split(name, ".")
	// 		extension := nameComponents[len(nameComponents)-1]
	// 		if extension == "xml" {
	// 			xmlFileNames = append(xmlFileNames, name)
	// 		}
	// 	}
	// } else {
	//	fmt.Println("Running in Single mode")
	// 	xmlFileNames = append(xmlFileNames, *inFileName)
	// }

	// for _, name := range xmlFileNames {
	// 	sourceFile, err := ioutil.ReadFile(fmt.Sprintf("%s%c%s", *inFileName, os.PathSeparator, name))
	// 	if err != nil {
	// 		fmt.Printf("Error reading file '%s' for conversion: %s\n", name, err.Error())
	// 		return
	// 	}

	// 	err = conv.AddFunction(sourceFile)
	// 	if err != nil {
	// 		fmt.Printf("Error during adding file '%s' for conversion: %s\n", name, err.Error())
	// 		return
	// 	}
	// }

	sourceFile, err := ioutil.ReadFile(*inFileName)
	if err != nil {
		fmt.Printf("Error reading file '%s' for conversion: %s\n", *inFileName, err.Error())
		return
	}

	err = conv.AddFunction(sourceFile)
	if err != nil {
		fmt.Printf("Error during adding file '%s' for conversion: %s\n", *inFileName, err.Error())
		return
	}

	outputs, err := conv.ConvertAll(*serialComposition, *parallelComposition, *synthesis)
	if err != nil {
		fmt.Println("Error during conversion:", err.Error())
		return
	}

	for _, output := range outputs {
		fmt.Printf("Writing %s.%s\n", output.Name, output.Extension)

		err = ioutil.WriteFile(fmt.Sprintf("%s%c%s.%s", *outLocation, os.PathSeparator, output.Name, output.Extension), output.Contents, 0644)
		if err != nil {
			fmt.Println("Error during file write:", err.Error())
			return
		}
	}

}
