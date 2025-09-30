#
Installation
#
## Update system
##
```sudo apt update && sudo apt upgrade -y
```
## Install Mininet
##
```sudo apt install mininet -y
```
## Install Open vSwitch
##
```sudo apt install openvswitch-switch -y
```
## Install Ryu
##
```sudo apt install python3-ryu -y
```
#
Case 1: Simple Switch with Ryu

Ryu has built-in apps located inside ryu/app/.
We use simple_switch_13 which implements a learning switch in OpenFlow 1.3.
#
##Start Ryu Controller
##
```ryu-manager ryu.app.simple_switch_13
```
##Start Mininet Topology
##
```sudo mn --topo single,3 --controller=remote,ip=127.0.0.1 --switch ovsk,protocols=OpenFlow13
```

--topo single,3 → 1 switch, 3 hosts (h1,h2,h3)

--controller=remote → connect Mininet to external Ryu controller

--switch ovsk,protocols=OpenFlow13 → use OVS with OpenFlow 1.3

##

### 
test connectivity
###
```mininet> pingall
```

##
Case 2: Simple firewall
##

### 
run it
###
```
ryu-manager firewall.py
```
###
In terminal 2
###
```
sudo mn --topo single,3 --controller=remote,ip=127.0.0.1 --switch ovsk,protocols=OpenFlow13
```
