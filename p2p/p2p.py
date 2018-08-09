from p2p import p2p_installed
from p2p import p2p_daemon
from p2p import p2p_status
from p2p import connected
from guardlib import check as t 

t.RegisterCheck(p2p_installed.Check, "Check if P2P is installed")
t.RegisterCheck(p2p_daemon.Check, "Check if P2P daemon is running")
t.RegisterCheck(p2p_status.Check, "Checking P2P status")
t.RegisterCheck(connected.Check, "Checking P2P for broken connections")