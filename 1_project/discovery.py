#!/usr/bin/env python3

import argparse
import logging
import ping3
import ipaddress
import socket
import nmap

def setup_logging():
    logging.basicConfig(filename='discover.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def validate_ip_range(ip_range):
    try:
        ipaddress.ip_network(ip_range, strict=False)
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"Invalid IP range: {e}")
    return ip_range

def scan_network(ip_range):
    active_hosts = []
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_range, arguments='-sn')  # perform ping scan only

    print(nm.all_hosts())

    for host in nm.all_hosts():
        ip = host
        try:
            result = ping3.ping(ip, timeout=3)  # timeout set to 3 seconds
            if result is not None:
                hostname = nm[host].hostname() if nm[host].hostname() else 'Unknown'
                active_hosts.append((ip, hostname))
            else:
                logging.info(f"IP address {ip} not discovered (timeout)")
        except Exception as e:
            logging.error(f"Error scanning {ip}: {e}")
    return active_hosts

def save_to_file(active_hosts, filename):
    with open(filename, 'w') as f:
        for ip, hostname in active_hosts:
            f.write(f"{ip}\t{hostname}\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Network Scanner')
    parser.add_argument('ip_range', type=validate_ip_range,
                        help='IP range or CIDR notation (e.g., 192.168.1.0/24)')
    parser.add_argument('-o', '--output', default='active_hosts.txt',
                        help='Output file (default: active_hosts.txt)')
    args = parser.parse_args()

    setup_logging()
    ip_range = args.ip_range
    output_file = args.output

    active_hosts = scan_network(ip_range)
    save_to_file(active_hosts, output_file)
    print(f"Active hosts with IP and hostname saved to {output_file}")
