from guardlib import check as t

def Executor(t):
    return t.ExecuteCommand("p2p status")


def ResultHandler(t, result):
    if result[0] == 0:
        t.MarkAsSucceed()
    else:
        t.MarkAsFailed()


def Check():
    c = t.Check(0, "p2p", "status")
    c.SetExecutor(Executor)
    c.SetHandler(ResultHandler)

    return c