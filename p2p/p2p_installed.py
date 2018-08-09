from guardlib import check as t
from guardlib import result as r


def Executor(t):
    return t.ExecuteCommand("which p2p")


def ResultHandler(t, result):
    status = 0
    if result[0] != 0:
        t.MarkAsFailed()
        status = 1
    else:
        t.MarkAsSucceed()
    return r.Result(t.GetComponent(), t.GetName(), status)


def Check():
    c = t.Check(0, "p2p", "p2p_installed")
    c.SetExecutor(Executor)
    c.SetHandler(ResultHandler)

    return c