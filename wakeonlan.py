import argparse
import re
import socket

def make_magic_pkg(addr: str):
    return bytes.fromhex(f'{"F" * 12}{addr.replace(addr[2], "") * 16}')

def mac_type(mac: str,
             pat = re.compile(r'^(([a-f0-9A-F]{2}[-:\.]){5}[a-f0-9A-F]{2}){1}$')):
    if not pat.match(mac):
        raise argparse.ArgumentTypeError("Invalid MAC address")
    return mac

def ip_type(ip: str,
            pat = re.compile(r'^((\d{1,3}\.){3}\d{1,3}){1}$')):
    if not pat.match(ip):
        raise argparse.ArgumentTypeError("Invalid ip address")
    return ip

def dn_type(dn: str,
            pat = re.compile(r'^(\w+\.)+\w+$')):
    if not pat.match(dn):
        raise argparse.ArgumentTypeError("Invalid domain name")
    return dn

def parse_argument() -> tuple[str, str]:
    parser = argparse.ArgumentParser(prog="wakeonlan",
                                     description="Wake On LAN using Python script")
    parser.add_argument("mac_addr",
                        help="MAC address of target machine",
                        type=mac_type)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i",
                       "--ip",
                       help="IP of target on the Internet",
                       type=ip_type)
    group.add_argument("-n",
                       "--domain_name",
                       help="Domain name of target on the Internet",
                       type=dn_type)
    parser.add_argument("-p",
                        "--ports",
                        help="Port list that interface is monitoring",
                        nargs='*',
                        type=int)
    args = parser.parse_args()
    return args.mac_addr, args.ip, args.domain_name, args.ports

def choose_dst_ip(ip: str, dn: str) -> str:
    if ip is None:
        if dn is not None:
            ip = socket.gethostbyname(dn)
        else:
            ip = "255.255.255.255"
    return ip

def send_pkg(pkg: str, dst_ip: str, ports: list[int] = [9, ]):
    for port in ports:
        with socket.socket(family=socket.AF_INET,
                           type=socket.SOCK_DGRAM,
                           proto=socket.IPPROTO_UDP) as s: # UDP
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # broadcast
            s.sendto(pkg, (dst_ip, port))

def wakeonlan():
    mac, ip, dn, ports = parse_argument()
    pkg = make_magic_pkg(mac)
    ip = choose_dst_ip(ip, dn)
    if ports is not None:
        send_pkg(pkg, ip, ports)
    else:
        send_pkg(pkg, ip)

if __name__ == '__main__':
    wakeonlan()