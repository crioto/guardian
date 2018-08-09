from guardlib import check as t 
from system import bazaar_reachable

t.RegisterCheck(bazaar_reachable.Check, "Checking if Bazaar is reachable")