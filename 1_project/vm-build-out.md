# VMWare Project Work Week Ending May 4, 2024
## M01 Individual Task (1): Network Diagram
### #01. I turned in an almost complete diagram
- [x] I need to pull the public IPs off the internal devices
    - [x] Interconnect firewall
    - [x] Routers
    - [x] The internal routers can be gateways.
    - [ ] I need to redo the IP addresses to something much smaller. Even brother Wickern was like, "that's a lot of addresses."
- [ ] Resubmit the diagram for review

Here's a possible breakdown:

1. **Subnet Mask**: /24 (255.255.255.0)
2. **Total IP Addresses**: 256

Now, let's divide this into four VLANs:

1. **VLAN Secure**:    
    - Subnet: 10.0.0.0/26
    - Usable IP Range: 10.0.0.1 - 10.0.0.62
    - Broadcast Address: 10.0.0.63
    - Total IPs: 64 (62 usable)

1. **VLAN Internal**:
    - Subnet: 10.0.0.64/26
    - Usable IP Range: 10.0.0.65 - 10.0.0.126
    - Broadcast Address: 10.0.0.127
    - Total IPs: 64 (62 usable)

1. **VLAN DMZ**:
    - Subnet: 10.0.0.128/26
    - Usable IP Range: 10.0.0.129 - 10.0.0.190
    - Broadcast Address: 10.0.0.191
    - Total IPs: 64 (62 usable)

1. **VLAN Interconnect**:
    - Subnet: 10.0.0.192/26
    - Usable IP Range: 10.0.0.193 - 10.0.0.254
    - Broadcast Address: 10.0.0.255
    - Total IPs: 64 (62 usable)

DMZ
10.0.0.129, 10.0.0.130, 10.0.0.131
Alpine
Ubuntu
Windows Server

# M01 Individual AAB Task (1): Create Own Related Task (I can sniff for open ports)
# M01 Individual AAB Task (2): Local GNS3
# M01 Individual AAB Task (3): Wireshark Capture Network Traffic
# M01 Team Task (1): Build Server VMs
# M01 Team Task (2): Build Firewalls
