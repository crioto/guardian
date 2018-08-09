# Main class for checks
# Each performing test must create an instance of Test class
# Test class provides several methods that can perform activities on user machine:
# ExecuteCommand - executes a CLI command, gathers exit code, stdout and stderr
# TODO: add ExecuteREST and possible other use cases for other components
#
# Result of each executor will be handled by Result() method which will run user defined
# callback to provide output of expected format


import time
import subprocess
from enum import Enum
import http.client

# undefinedCallback is a dummy callback function
def undefinedCallback(result):
    print("Undefined callback")

# Possible statuses (states) of test
CheckStatus = Enum('CheckStatus', 'succeed failed pending running')

CheckList = {}

class Check:
    name = "Unnamed"
    component = ""
    createDate = 0
    startDate = 0
    endDate = 0
    executorCallback = undefinedCallback
    handlerCallback = undefinedCallback
    status = CheckStatus.pending


    def __init__(self, config, component, name):
        self.name = name
        self.component = component
        self.createDate = time.time()
        self.config = config
        self.status = CheckStatus.pending


    # GetComponent returns component name
    def GetComponent(self):
        return self.component


    # GetName returns Check name
    def GetName(self):
        return self.name


    # GetSTatus returns current status of the Check
    def GetStatus(self):
        return self.status
    

    # SetExecutor will set main Check function callback
    def SetExecutor(self, cb):
        self.executorCallback = cb


    # SetHandler will set a handler callback
    def SetHandler(self, cb):
        self.handlerCallback = cb


    # Start will initiate Check execution and run executor callback function
    def Start(self):
        self.startDate = time.time()
        self.status = CheckStatus.running
        return self.executorCallback(self)


    # Stop will finish Check
    def Stop(self):
        self.endDate = time.time()
        return 0

    
    # ExecuteCommand will execute a syscall with specified command and arguments and return a tuple 
    # of three elements: status code, stdout, stderr
    def ExecuteCommand(self, command):
        p = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        return [p.returncode, out.decode('utf-8'), err.decode('utf-8')]


    # ExecuteHTTPSRequestGET will execute GET request over HTTPS to the `host` and `uri`
    # Returns a tuple of status code, reason, headers list and decoded response
    def ExecuteHTTPSRequestGET(self, host, uri):
        connection = http.client.HTTPSConnection(host)
        connection.request("GET", uri)
        response = connection.getresponse()
        headers = response.getheaders()
        return [response.status, response.reason, headers, response.read().decode()]


    # Result will run ResultHandler callback
    def Result(self, result):
        return self.handlerCallback(self, result)

    
    def MarkAsSucceed(self):
        self.status = CheckStatus.succeed


    def MarkAsFailed(self):
        self.status = CheckStatus.failed

    

# RegisterCheck will add Check described as `name` to the queue
# executor is a main Check entry point
# resultHandler will parse result of executor
def RegisterCheck(newCheck, name):
    CheckList[name] = newCheck()