# Example test that checks p2p daemon status

from guardlib import check as t
from guardlib import result as r

# Executor is the main entry point for a test
# This function 
def Executor(t):
    return t.ExecuteCommand("systemctl status subutai-p2p.service")


# ResultHandler will handle result returned by executor
# In case of p2p daemon we expect it to have 'active' word in 
# systemctl status command output
def ResultHandler(t, result):
    status = -1
    if 'running' in result[1]:
        t.MarkAsSucceed()
        status = 0
    else:
        t.MarkAsFailed()
        status = 1
    
    result = r.Result(t.GetComponent(), t.GetName(), status)
    # If you have additional data for results, you can use r.append(key, value) method
    # All extra fields will be added to payload field of resulting YAML
    return result

# Check creates an instance of `Check` class, sets callbacks and returns it
# for later registration
def Check():
    c = t.Check(0, "p2p", "daemon")
    c.SetExecutor(Executor)
    c.SetHandler(ResultHandler)

    return c