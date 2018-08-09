from guardlib import check as t 
from peeros import agent_installed

t.RegisterCheck(agent_installed.Check, "Checking Subutai Installation")