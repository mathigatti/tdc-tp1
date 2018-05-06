# -*- coding: utf-8 -*-

# ATENCION: ESTO ESTA PYTHON 2.7!!

import sys
from scapy.all import *
import math
import csv

def packet_callback(a_packet):
    return a_packet.show()

def arp_operation(pkt):
    if pkt[ARP].op == 1:  # who-has (request)
        return 'who-has'
    if pkt[ARP].op == 2:  # is-at (response)
        return 'is-at'
    raise Exception('Valor de ARP Op inesperado: ' + pkt[ARP].op)

def run(file):

    # ELEGIR:

    # Descomentar para sniffear manualmente:
    # packets = sniff(prn=callback, iface="eth0", count=10000)

    # O Descomentar para cargar de un archivo "x":
    packets = rdpcap(file)

    print packets
    print packets[ARP]
    print packets[ARP][0].show()
    print hex(packets[0].type)

    # --Desde aca va el procesamiento de paquetes (Tambien se podria hacer en el callback si se captura live)--
    symbol_count = {}
    total_count = 0
    for a_packet in packets[ARP]:
        if a_packet[ARP].op == 1:  # who-has (request)
    #        current_tuple = (arp_operation(a_packet), a_packet.psrc, a_packet.pdst)
    #        current_tuple = (arp_operation(a_packet), a_packet.psrc)
            current_tuple = (arp_operation(a_packet), a_packet.pdst)

            # Cuento:
            if current_tuple not in symbol_count:
                symbol_count[current_tuple] = {'count': 0}
                
            symbol_count[current_tuple]['count'] += 1
            total_count += 1

    entropy = 0
    for a_symbol in symbol_count:
        symbol_count[a_symbol]['probability'] = symbol_count[a_symbol]['count'] / float(total_count)
        symbol_count[a_symbol]['information'] = -math.log(symbol_count[a_symbol]['probability'], 2)
        entropy -= symbol_count[a_symbol]['probability'] * math.log(symbol_count[a_symbol]['probability'], 2)

    # Printeo lindo:
    for a_symbol in symbol_count:
        print "Type: %s \t----- Count: %d --- P(e): %f ---- I(e): %d bit" % (repr(a_symbol), symbol_count[a_symbol]['count'], symbol_count[a_symbol]['probability'], symbol_count[a_symbol]['information'])
    print "Source Entropy: %f" % entropy
    print "Max Entropy: %f" % math.log(len(symbol_count), 2)
    # print total_count

    with open(file.replace('.pcap', '_S2_output.csv'), 'w') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(['Symbol', 'Count', 'Probability', 'Information'])
        for a_symbol in symbol_count:
            writer.writerow([repr(a_symbol), symbol_count[a_symbol]['count'], symbol_count[a_symbol]['probability'], symbol_count[a_symbol]['information']])


if __name__ == "__main__":
   run(sys.argv[1])    