from guardlib import check as t
from guardlib import result as r
import re


def Executor(t):
    return t.ExecuteCommand("p2p debug")


def ResultHandler(t, result):

    hours = 0
    minutes = 0
    seconds = 0

    lines = result[1].splitlines()
    for line in lines:
        if line[0:6] == "Uptime":
            # Parsing uptime output of p2p debug
            v = line[8:]
            hs = v.split('h')
            hours = re.search('(\\d+)', hs[0], re.IGNORECASE).group(1)
            ms = hs[1].split('m')
            minutes = re.search('(\\d+)', ms[0], re.IGNORECASE).group(1)
            ss = ms[1].split('s')
            seconds = re.search('(\\d+)', ss[0], re.IGNORECASE).group(1)

    status = 0
    if int(minutes) < 5 and int(hours) == 0:
        t.MarkAsSucceed()
    else:
        if result[1].find('INITIALIZING') > 0 or result[1].find('WAITING') > 0:
            t.MarkAsFailed()
            status = 1
        else:
            t.MarkAsSucceed()
    
    return r.Result(t.GetComponent(), t.GetName(), status)


def Check():
    c = t.Check(0, "p2p", "connected")
    c.SetExecutor(Executor)
    c.SetHandler(ResultHandler)

    return c