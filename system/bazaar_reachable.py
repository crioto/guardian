from guardlib import check as t
from guardlib import result as r


# Request login page here, since root will return 303 status code
def Executor(t):
    return t.ExecuteHTTPSRequestGET("bazaar.subutai.io", "/login")


def ResultHandler(t, result):
    status = 0
    if result[0] != 200:
        t.MarkAsFailed()
        status = 1
    else:
        t.MarkAsSucceed()
    return r.Result(t.GetComponent(), t.GetName(), status)


def Check():
    c = t.Check(0, "system", "bazaar_reachable")
    c.SetExecutor(Executor)
    c.SetHandler(ResultHandler)

    return c