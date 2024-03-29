import scapy.all as scapy
import os
import sys
import optparse

parser=optparse.OptionParser()

parser.add_option("-i","--interface",dest="interface",help="Enter the network interface")

(options,arguments)=parser.parse_args()
interface=options.interface

def sniff(interface):
	scapy.sniff(iface=interface,store=False,prn=process_sniffed_packet)

def process_sniffed_packet(packet):
	if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op==2:
		try:
			real_mac = get_mac(packet[scapy.ARP].psrc)
			respone_mac = packet[scapy.ARP].hwsrc
			print(real_mac,respone_mac)
			if real_mac != respone_mac:
				print("[+] We are under attack.....!")
				sys.exit()
		except IndexError:
			pass

def get_mac(ip):
	arp_request=scapy.ARP(pdst=ip)
	broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	arp_request_broadcast=broadcast/arp_request
	respone_list=scapy.srp(arp_request_broadcast,timeout=1,verbose=0)[0]
	return respone_list[0][1].hwsrc

sniff(interface)

