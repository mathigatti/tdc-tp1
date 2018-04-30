# -*- coding: utf-8 -*-


# ATENCION: ESTO ESTA PYTHON 2.7!!

from scapy.all import *
import math

def packet_callback(a_packet):
    return a_packet.show()


# ELEGIR:

# Descomentar para sniffear manualmente:
# packets = sniff(prn=callback, iface="eth0", count=10000)

# O Descomentar para cargar de un archivo "x":
packets = rdpcap("capture.pcap")


print packets
print packets[ARP]
print packets[ARP][0].show()
print hex(packets[0].type)





# --Desde aca va el procesamiento de paquetes (Tambien se podria hacer en el callback si se captura live)--
symbol_count = {}
total_count = 0
for a_packet in packets:
    
    # No cuento los paquetes que no son ethernet (esta bien esto??)
    if Ether not in a_packet:
        continue
    
    # < BROADCAST|UNICAST, PROTOCOL(hex) >
    current_tuple = ("BROADCAST" if a_packet[Ether].dst == 'ff:ff:ff:ff:ff:ff' else "UNICAST", hex(a_packet.type))
    
    # Cuento:
    if current_tuple not in symbol_count:
        symbol_count[current_tuple] = {'count': 0}
        
    symbol_count[current_tuple]['count'] += 1
    total_count += 1


entropy = 0
for a_symbol in symbol_count:
    symbol_count[a_symbol]['probability'] = symbol_count[a_symbol]['count'] / float(total_count)
    symbol_count[a_symbol]['information'] = math.ceil(-math.log(symbol_count[a_symbol]['probability'], 2))
    entropy -= symbol_count[a_symbol]['probability'] * math.log(symbol_count[a_symbol]['probability'], 2)
    

# Printeo lindo:    
for a_symbol in symbol_count:
    print "Type: %s \t----- Count: %d --- P(e): %f ---- I(e): %d bit" % (repr(a_symbol), symbol_count[a_symbol]['count'], symbol_count[a_symbol]['probability'], symbol_count[a_symbol]['information'])
print "Source Entropy: %f" % entropy
print "Max Entropy??: %f" % math.log(len(symbol_count), 2)
# print total_count
