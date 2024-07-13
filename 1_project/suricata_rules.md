# Rules for my suricata
alert icmp any any -> 172.16.17.0/24 any (msg:"viking ping"; itype:8; content:"viking"; sid:7001001; rev:1;)


