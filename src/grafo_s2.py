# -*- coding: utf-8 -*-

# ATENCION: ESTO ESTA PYTHON 2.7!!

import sys
from scapy.all import *
import math
from grafo import *

def packet_callback(a_packet):
    return a_packet.show()

def arp_operation(pkt):
    if pkt[ARP].op == 1:  # who-has (request)
        return 'who-has'
    if pkt[ARP].op == 2:  # is-at (response)
        return 'is-at'
    raise Exception('Valor de ARP Op inesperado: ' + pkt[ARP].op)

def run(file):
    
    packets = rdpcap(file)

    #data = ['data/hogar_ethernet.pcap']
    #data = ['data/starbucks.pcap']
    
    #packets = rdpcap(data[0])

    # --Desde aca va el procesamiento de paquetes (Tambien se podria hacer en el callback si se captura live)--
    symbol_count = {}
    total_count = 0
    for a_packet in packets[ARP]:
        if a_packet[ARP].op == 1:
            current_tuple = (a_packet.psrc, a_packet.pdst)

            # Cuento:
            if current_tuple not in symbol_count:
                symbol_count[current_tuple] = 0

            symbol_count[current_tuple] += 1
            total_count += 1

    edges = map(lambda x: (x[0][0],x[0][1],x[1]), symbol_count.items())

    grafo_dirigido(list(edges))

if __name__ == "__main__":
   run(sys.argv[1])    