#!/usr/bin/env python3
from scapy.all import *
import os

packets_total = 0
packets_broadcast = 0

def broadcast_callback(packet):
    global packets_total
    global packets_broadcast

    if(Ether in packet):
        if(packet[Ether].dst == 'ff:ff:ff:ff:ff:ff'):
            packets_broadcast += 1
    
    packets_total = packets_total + 1
    
    # Limpio la pantalla
    os.system('clear')

    print("Paquetes de broadcast: ",packets_broadcast)
    print("Paquetes totales: ",packets_total)
    print("Proporcion broadcast/totales: ", float(packets_broadcast/packets_total))

# El argumento store=0 es para que no se guarden los paquetes en memoria; con 10.000 paquetes no va a pasar nada, pero en caso de capturas de varios GB puede llegar a molestar
packets = sniff(prn=broadcast_callback, iface="wlan0", store=0)
