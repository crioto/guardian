import sys
from p2p import p2p
from system import system
from peeros import peeros
from guardlib import check as t


# ParseCommand will try to parse arguments provided to an app
# if no arguments provided it will output help message and return non-zero status code
def ParseCommand(cmd, args):
    if cmd == 'help':
        ShowHelp()
        return 1
    if cmd == 'list':
        List(args)
        return 0
    if cmd == 'run':
        Run(args)
        return 0
    ShowHelp()
    return 1


# ShowHelp prints help message to stdout
def ShowHelp():
    print("Subutai Guardian\n")
    print("Available commands:")
    print("\thelp")
    print("\t\tshow this help screen")
    print("\tlist")
    print("\t\tlist available components and tests if component name specified")
    print("\trun")
    print("\t\trun all tests. You can specify component name to run only specific component or component.test to run specific test")
    return 0


# List is an entry point for `list` argument
def List(args):
    if len(args) > 0:
        ListComponentTests(args[0])
    else:
        ListComponents()


# ListComponents will print list of all components registered
def ListComponents():
    components = []
    print("Available components:")
    for n, test in t.CheckList.items():
        exists = False
        for c in components:
            if c == test.GetComponent():
                exists = True
                break
        if exists == False:
            components.append(test.GetComponent())
            print("\t" + test.GetComponent())
    
    return 0


# LIstComponentTests will output list of tests within provided component to stdout
def ListComponentTests(component):
    print("Available tests in " + component + ":")
    for n, test in t.CheckList.items():
        if test.GetComponent() == component:
            print("\t" + test.GetName())

    return 0


# EchoTest will send an informing line to stdout without EOL
def EchoTest(name):
    print(name + "\t", end="", flush=True)


# Run function will start test execution
# If no arguments provided all registered tests will be executed
# If a single word provided it's considered as a component name
# If argument provided in form of componentName.testName a specific test will be executed
def Run(args):
    componentName = ''
    testName = ''

    # When argument provided we consider it to be component name (single word)
    # or specific test name in a form of componaneName.testName
    if len(args) > 0:
        if args[0].find(".") > 0:
            r = args[0].split(".")
            if len(r) != 2:
                print("Wrong format for run: " + args[0])
                print("Specify component name or test name in a form componentName.testName")
                return 4
            componentName = r[0]
            testName = r[1]
        else:
            componentName = args[0]

    for name, test in t.CheckList.items():
        if componentName != "" and test.GetComponent() != componentName:
            continue
        if testName != "" and test.GetName() != testName:
            continue
        EchoTest(name)
        test.Result(test.Start())
        if test.GetStatus() == t.CheckStatus.succeed:
            print("[OK]")
        elif test.GetStatus() == t.CheckStatus.failed:
            print("[Failed]")
        else:
            print("[Error]")

    return 0
        

# Entry point
if len(sys.argv) > 1:
    rc = ParseCommand(sys.argv[1], sys.argv[2:])
    if rc != 0:
        sys.exit(rc)
else:
    ShowHelp()
    sys.exit(1)