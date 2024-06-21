### Tutorial: Installing Squid DNS Proxy on Ubuntu 22.04 in a DMZ

This tutorial will guide you through the installation and configuration of Squid, a caching and forwarding web proxy, on Ubuntu 22.04. We will set up Squid to act as a web proxy, and we'll also configure a DNS server to serve all computers in a secure zone. 

### Prerequisites
- A server running Ubuntu 22.04 in our DMZ.
- Root or sudo access to the server.
- Basic understanding of network configurations and DNS.

### Step 1: Update System Packages

Start by updating your package list and upgrading your existing packages:

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 2: Install Squid Proxy

Install Squid using the package manager:

```bash
sudo apt install squid -y
```

### Step 3: Configure Squid Proxy

The main configuration file for Squid is located at `/etc/squid/squid.conf`. Before making changes, it's a good idea to back up the original configuration file:

```bash
sudo cp /etc/squid/squid.conf /etc/squid/squid.conf.backup
```

Open the configuration file with a text editor:

```bash
sudo vim /etc/squid/squid.conf
```

You can configure Squid to allow traffic from your secure zone by adding the following lines. In our case, we use the network address of our secure zone:

```bash
acl localnet src 10.0.0.0/27
http_access allow localnet
http_access deny all
```

You may also want to configure Squid to listen on a specific network interface. Look for the `http_port` directive and specify your interface:

```bash
http_port 3128
```

Save and close the file.

### Step 4: Start and Enable Squid Service

Start the Squid service and enable it to start on boot:

```bash
sudo systemctl start squid
sudo systemctl enable squid
```

### Step 5: Install and Configure DNS Server (Bind9)

Next, we will install and configure `bind9` to serve as a DNS server.

Install `bind9`:

```bash
sudo apt install bind9 -y
```

### Step 6: Configure Bind9

The main configuration files for `bind9` are located in `/etc/bind/`. We'll configure it to act as a caching DNS server.

Open the `named.conf.options` file for editing:

```bash
sudo vim /etc/bind/named.conf.options
```

Uncomment and edit the following lines to allow queries from your secure zone:

```bash
options {
    directory "/var/cache/bind";

    // Forwarding to upstream DNS servers
    forwarders {
        8.8.8.8;  // Google DNS
        8.8.4.4;  // Google DNS
    };

    // Allow queries from secure zone
    allow-query { any; };

    // Enable recursion
    recursion yes;

    dnssec-validation auto;

    auth-nxdomain no;    # conform to RFC1035
    listen-on-v6 { any; };
};
```

Save and close the file.

Restart the Bind9 service:

```bash
sudo systemctl restart bind9
sudo systemctl enable bind9
```

### Step 7: Configure Firewall
If you are using `firewalld` as your firewall, allow traffic to Squid (port 3128) and Bind9 (port 53 for DNS):

```bash
sudo apt install firewalld -y
sudo systemctl enable firewalld
sudo systemctl status firewalld

sudo firewall-cmd --zone=public --permanent --add-service=http
sudo firewall-cmd --zone=public --permanent --add-service=https
sudo firewall-cmd --zone=public --permanent --add-service=dns

sudo firewall-cmd allow port=3128/tcp
sudo firewall-cmd allow port=53/tcp
sudo firewall-cmd allow port=53/udp

sudo firewall-cmd --restart
```

### Step 8: Configure Clients

Configure the computers in your secure zone to use your Squid server as their web proxy and your Bind9 server as their DNS server.

For DNS, set the DNS server address in the network settings of each client to the IP address of your server.

For web proxy settings, configure the web browsers or the network settings on each client to use the IP address of your server on port 3128.

### Conclusion

You have successfully installed and configured Squid as a web proxy and Bind9 as a DNS server on Ubuntu 22.04. Your server is now ready to serve the secure zone in your DMZ. Regularly monitor and update your configurations to ensure optimal performance and security.