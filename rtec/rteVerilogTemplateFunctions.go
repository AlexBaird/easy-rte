package rtec

import (
	"bufio"
	"encoding/xml"
	"fmt"
	"io/ioutil"
	"os"
	"strings"

	"github.com/PRETgroup/easy-rte/rtedef"
)

//VerilogECCTransition is used with getVerilogECCTransitionCondition to return results to the template
type VerilogECCTransition CECCTransition

//getVerilogECCTransitionCondition returns the C "if" condition to use in state machine next state logic and associated events
// returns "full condition", "associated events"
func getVerilogECCTransitionCondition(function rtedef.EnforcedFunction, trans string) VerilogECCTransition {
	if trans != "Default" {
		return VerilogECCTransition{IfCond: trans, AssEvents: nil}
	}
	return VerilogECCTransition{"Default", nil} // Could do something here to make clearer default and handle in template?
}

//getVerilogType returns the VHDL type to use with respect to an IEC61499 type
func getVerilogType(ctype string) string {
	return "reg " + getVerilogWidthArrayForType(ctype)
}

func getVerilogWidthArrayForType(ctype string) string {
	verilogType := ""

	switch strings.ToLower(ctype) {
	case "bool":
		verilogType = ""
	case "char":
		verilogType = "[7:0]"
	case "uint8_t":
		verilogType = "[7:0]"
	case "uint16_t":
		verilogType = "[15:0]"
	case "uint32_t":
		verilogType = "[31:0]"
	case "uint64_t":
		verilogType = "[63:0]"
	case "int8_t":
		verilogType = "signed [7:0]"
	case "int16_t":
		verilogType = "signed [15:0]"
	case "int32_t":
		verilogType = "signed [31:0]"
	case "int64_t":
		verilogType = "signed [63:0]"
	case "float":
		panic("Float type not allowed in conversion")
	case "double":
		panic("Double type not allowed in conversion")
	case "dtimer_t":
		verilogType = "[63:0]"
	case "rtimer_t":
		panic("rtimer type not allowed in conversion")
	default:
		panic("Unknown type: " + ctype)
	}

	return verilogType
}

func isDefault(str string) bool {
	return str == "Default"
}

type Recover struct {
	Signal string `xml:"Signal"`
	Value  string `xml:"Value"`
}

type Row struct {
	// XMLName			xml.Name	`xml:"Row"`
	Recovery    string    `xml:"Recovery"`
	RecoveryKey string    `xml:"RecoveryKey"`
	Recovers    []Recover `xml:"Recover"`
}

type SelectLUT struct {
	// XMLName		xml.Name	`xml:"SelectLUT"`
	Rows []Row `xml:"Row"`
}

type EnforcedFunction struct {
	// Interface	string	`xml:"Interface"`
	// Policies	[]string	`xml:"Policy"`
	LUT SelectLUT `xml:"SelectLUT"`
}

func boolStrToIntStr(boolStr string) string {
	if boolStr == "True" {
		return "1"
	} else if boolStr == "False" {
		return "0"
	} else {
		return ""
	}
}

func isNone(boolStr string) bool {
	if boolStr == "None" {
		return true
	} else {
		return false
	}
}

func getLUT(blockName string) string {
	var filename = "example/" + blockName + "/" + blockName + "_modified.xml"
	fmt.Println(filename)

	// Open our xmlFile
	xmlFile2, err2 := os.Open(filename)
	// if we os.Open returns an error then handle it
	if err2 != nil {
		fmt.Println("\nError:", err2)
		fmt.Println("\nCommonly projects have a different [Folder] and [Blockname].")
		fmt.Println("\texample/[Folder]/[Blockname]_modified.xml")
		fmt.Println("If your [Folder] != [Blockname] please enter a new [Folder] name here (followed by Enter/Return key):")
		reader := bufio.NewReader(os.Stdin)
		// ReadString will block until the delimiter is entered
		input, err := reader.ReadString('\n')
		if err != nil {
			fmt.Println("An error occurred while reading input. Please try again", err)
			return "error"
		}
		input = strings.TrimSuffix(input, "\n")
		filename = "example/" + input + "/" + blockName + "_modified.xml"
		fmt.Println("You gave me:", input)
		fmt.Println("New filename:", filename)
	}
	xmlFile2.Close()

	xmlFile, err := os.Open(filename)
	if err != nil {
		return "error"
	}

	fmt.Println("Successfully Opened " + filename)
	// defer the closing of our xmlFile so that we can parse it later on
	defer xmlFile.Close()

	// read our opened xmlFile as a byte array.
	byteValue, _ := ioutil.ReadAll(xmlFile)

	var q EnforcedFunction

	xml.Unmarshal(byteValue, &q)

	// fmt.Println(q)
	// fmt.Println(q.LUT)
	// fmt.Println(q.LUT.Rows)

	// For each row
	// Add to case statement!
	var caseStatement string = ""
	for i, row := range q.LUT.Rows {
		if i != 0 {
			caseStatement += "\t\t\t"
		}
		caseStatement += fmt.Sprint(len(row.RecoveryKey)) + "'b" + row.RecoveryKey + ": begin\n"
		for _, signal := range row.Recovers {
			if (!isNone(signal.Value)) {
				caseStatement += "\t\t\t\t" + signal.Signal + " = " + boolStrToIntStr(signal.Value) + ";\n"
			}
		}
		caseStatement += "\t\t\t\tend\n"
	}
	fmt.Println(caseStatement)

	return caseStatement
}

func getMaxRecoveryReference(policy rtedef.Policy) int {
	var maxRecoveryRef uint = 0
	for _, transition := range policy.Transitions {
		if transition.RecoveryReference > maxRecoveryRef {
			maxRecoveryRef = transition.RecoveryReference
		}
	}
	// fmt.Println(maxRecoveryRef)

	return int(maxRecoveryRef) + 1 // Quick fix for getVerilogWidthArray not working quite as expected
}

func add1IfClock(ctype string) string {
	if ctype == "dtimer_t" {
		return " + 1"
	}
	if ctype == "rtimer_t" {
		panic("rtimer type not allowed in conversion")
	}
	return ""
}

func getVerilogWidthArray(l int) string {
	cl2 := ceilLog2(uint64(l)) - 1
	if cl2 >= 1 {
		return fmt.Sprintf("[%v:0]", cl2)
	}
	return ""
}

var t = [6]uint64{
	0xFFFFFFFF00000000,
	0x00000000FFFF0000,
	0x000000000000FF00,
	0x00000000000000F0,
	0x000000000000000C,
	0x0000000000000002,
}

//ceilLog2 performs a log2 ceiling function quickly
func ceilLog2(x uint64) int {

	y := 0
	if (x & (x - 1)) != 0 {
		y = 1
	}
	j := 32
	var i int

	for i = 0; i < 6; i++ {
		k := 0
		if (x & t[i]) != 0 {
			k = j
		}
		y += k
		x >>= uint64(k)
		j >>= 1
	}

	return y
}

func add(a, b int) int {
	return a + b
}

func subtract(a, b int) int {
	return a - b
}

func equal(a, b int) int {
	if a == b {
		return 1
	}
	return 0
}

func equal_str(a, b string) int {
	if a == b {
		return 1
	}
	return 0
}
