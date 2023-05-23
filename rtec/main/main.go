package main

import (
	"flag"
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"strings"
	"github.com/PRETgroup/easy-rte/rtedef"
	"encoding/xml"
	"errors"
	"github.com/PRETgroup/easy-rte/rtec"
)

var (
	inFileName          = flag.String("i", "", "Specifies the name of the source xml file to be compiled.")
	outLocation         = flag.String("o", "", "Specifies the name of the directory to put output files. If blank, uses current directory")
	language            = flag.String("l", "c", "The output language")
	serialComposition   = flag.Bool("serialComposition", false, "(Experimental, Verilog Only) Set this to true to produce a serial composition of enforcers. Mutually exclusive with parallelComposition.")
	parallelComposition = flag.Bool("parallelComposition", false, "(Experimental, Verilog Only) Set this to true to produce a parallel composition of enforcers. Mutually exclusive with serialComposition.")
	synthesis           = flag.Bool("synthesis", false, "(Experimental, Verilog Only) Set this to true to produce Verilog which is compatible with ModelSim simulation and Quartus for hardware synthesis.")
)

func main() {
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

	
	// TODO: This is where we should consider reading only a fixed size
	
	// However, this means conv.AddFunction(sourceFile) will need to cope with partial XML files, and then
	// with partial function/enforcer definitions
	
	// If that is a bit too hard, perhaps we need to be smarter about how much of the file we read.
	// For example, perhaps we would read the I/O, then the first ... hmm ... not sure where we could split
	// because we're talking about monolithc here.
	
	// Regardless, I'll need to take a look at the input XML files and give thought to how we could process a "leaf" at a time (maybe a single transition could be a leaf)
	
	fmt.Println("Reading file:", *inFileName)
	sourceFile, err := os.Open(*inFileName)
	if err != nil {
		fmt.Printf("Error reading file '%s' for conversion: %s\n", *inFileName, err.Error())
		return
	}

	defer sourceFile.Close()

	decoder := xml.NewDecoder(sourceFile)

	FB := rtedef.EnforcedFunction{}

	var currentPolicyIndex = 0
	for {
		t, tokenErr := decoder.Token()
		if tokenErr != nil {
			if tokenErr == io.EOF {
				break
			}
			// handle error somehow
			fmt.Errorf("decoding token: %v", err)
		}
		switch t := t.(type) {
		case xml.StartElement:
			switch t.Name.Local {
			case "EnforcedFunction":
				FB.Name = t.Attr[len(t.Attr)-1].Value
				// fmt.Println("\tFound new function:", FB.Name)
			// case "Interface":
			// 	decoder.DecodeElement(&FB.InterfaceList, &t)
			// 	fmt.Println("\tFound interface:", FB.InterfaceList.InputVars., FB.OutputVars)
			case "Input":
				decoder.DecodeElement(&FB.InputVars, &t)
				// fmt.Println("\tFound input", len(FB.InterfaceList.InputVars), ":", FB.InputVars[len(FB.InputVars)-1].Name)
			case "Output":
				decoder.DecodeElement(&FB.OutputVars, &t)
				// fmt.Println("\tFound output", len(FB.InterfaceList.OutputVars), ":",  FB.OutputVars[len(FB.OutputVars)-1].Name)
			case "Policy":
				FB.AddPolicy(t.Attr[len(t.Attr)-1].Value)
				// fmt.Println("\tFound policy", len(FB.Policies), ":",  FB.Policies[len(FB.Policies)-1].Name)
				currentPolicyIndex = len(FB.Policies)-1
			case "InternalVars":
				var internalVars []rtedef.Variable
				decoder.DecodeElement(&internalVars, &t)
				// fmt.Println("Internal vars:", internalVars)
				if (fmt.Sprintf("%v", internalVars) != "[{  false   }]") {
					FB.Policies[currentPolicyIndex].InternalVars = internalVars // This may need work to handle empty/false case
					// fmt.Println("\tFound internal vars for policy",  FB.Policies[currentPolicyIndex].Name, FB.Policies[currentPolicyIndex].InternalVars)
				}
			case "PState":
				var stateName = ""
				decoder.DecodeElement(&stateName, &t)
				FB.Policies[currentPolicyIndex].AddState(stateName)
				// fmt.Println("\tFound PState for policy",  stateName)
			case "PTransition":
				var trans rtedef.PTransition 
				decoder.DecodeElement(&trans, &t)
				// fmt.Println(trans)
				FB.Policies[currentPolicyIndex].AddTransitionObj(trans)
				// fmt.Println("\tFound PState for policy",  stateName)
			default:
				fmt.Println("Unhandled start element token:", /*t,*/ t.Name.Local)
			}

		}
	}
	
	fmt.Println("Reading file:", *inFileName)
	sourceFile2, err := ioutil.ReadFile(*inFileName)
	if err != nil {
		fmt.Printf("Error reading file '%s' for conversion: %s\n", *inFileName, err.Error())
		return
	}
	err = conv.AddFunction(sourceFile2)
	FB2 := rtedef.EnforcedFunction{}
	if err := xml.Unmarshal(sourceFile2, &FB2); err != nil {
		errors.New("Couldn't unmarshal EnforcedFunction xml: " + err.Error())
		return 
	}

	string1 := fmt.Sprintf("%v", FB)
	string2 := fmt.Sprintf("%v", FB2)
	if (string1 != string2) {
		fmt.Println("Two methods for obtaining FB are not equal!")
		fmt.Println("Piecewise:\n", string1)
		fmt.Println("All at once:\n", string2)

		differences := ""
		for i := 0; i < len(string1) && i < len(string2); i++ {
			if string1[i] != string2[i] {
				differences += string(string2[i])
			}
		}

		fmt.Println("Differences:\n", differences)

		panic("Two methods for obtaining FB are not equal!")
	}

	// conv.Funcs = append(conv.Funcs, FB)

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
