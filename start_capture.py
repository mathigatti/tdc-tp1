# -*- coding: utf-8 -*-


# ATENCION: ESTO ESTA PYTHON 2.7!!

from scapy.all import *

def packet_callback(a_packet):
    return a_packet.show()

def callback(pkt):                                   
    print(pkt.show())

# ELEGIR:

# Descomentar para sniffear manualmente:
packets = sniff(prn=callback, iface="wlp3s0", count=10000)
wrpcap("capture_labo6_2018-04-18_19-06hs.pcap", packets)

# O Descomentar para cargar de un archivo "x":
#packets = rdpcap("capture.pcap")


print packets
print packets[ARP]
print packets[ARP][0].show()
print hex(packets[0].type)


wrpcap("capture_labo6_2018-04-18_18-39hs.pcap", packets)


# --Desde aca va el procesamiento de paquetes (Tambien se podria hacer en el callback si se captura live)--
symbol_count = {}

for a_packet in packets:
    
    # No cuento los paquetes que no son ethernet (esta bien esto??)
    if Ether not in a_packet:
        continue
    
    # < BROADCAST|UNICAST, PROTOCOL(hex) >
    current_tuple = ("BROADCAST" if a_packet[Ether].dst == 'ff:ff:ff:ff:ff:ff' else "UNICAST", hex(a_packet.type))
    
    # Cuento:
    if current_tuple not in symbol_count:
        symbol_count[current_tuple] = 0
        
    symbol_count[current_tuple] += 1


# Printeo lindo:    
for a_symbol in symbol_count:
    print "%s \t----- %d" % (repr(a_symbol), symbol_count[a_symbol])
