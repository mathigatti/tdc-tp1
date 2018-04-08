from scapy.all import *

# Algunas funciones útiles
################ DEMO INTRODUCCIÓN/INSTALACIÓN ################
lsc() # muestra funciones de scapy
ls() # muestra las clases de protocolos disponibles

ls(Ether) # muestra formato del frame
help(Ether) # muestra info sobre la clase Ether
help(sniff) # muestra info sobre la función sniff

################ DEMO SNIFFING/CON SCAPY ################
# CALLBACK - Qué queremos hacer con cada paquete. Por ahora, sólo mostrarlos
def callback(pkt):                                   
    print(pkt.show())

# Usar ifconfig en la consola para saber el nombre de nuestras interfaces
# sudo ifconfig wlan0 promisc habilita el modo promiscuo en la interface wlan0
# Habilitar modo monitor va a depender de la placa de red y driver que estén usando... ¡investiguen!
# https://wiki.wireshark.org/CaptureSetup/WLAN#Linux

# En mi caso...
# sudo apt-get install aircrack-ng
# sudo airmon-ng start wlp18s0
# sudo ifconfig prism0 up

# Queremos escuchar todos los paquetes que entren a la interface loopback durante 45 segundos
packets = sniff(prn=callback, iface="lo", timeout=45)

## ping 127.0.0.1
## ping localhost
## ssh petemir@localhost

# Queremos escuchar 10.000 paquetes de protocolo ARP en la interface wlan0
packets = sniff(prn=callback, iface="wlan0", filter="arp", count=1000)


################ DEMO TRAMAS Y PAQUETES/PAQUETES EN SCAPY ################
# Queremos escuchar 10000 paquetes de todo lo que pase en wlan0
packets = sniff(prn=callback, iface="wlan0", count=1000)

# Veamos qué paquetes hay
packets

# Se pueden buscar paquetes de los protocolos específicos que nos interesen
packets[Ether]
packets[IP]
packets[ARP]

# Siguen siendo listas de paquetes (clase PacketList de scapy)
packets[Ether][TCP]
packets[Ether][Ether]

# Veamos un paquete
packets[0]
packets[Ether][0]

# Resumen
packets[0].summary()

# O, visto más lindo
packets[0].show()

# Ver el tipo del paquete, mayor que 1500

#0 - 1500 length field (IEEE 802.3 and/or 802.2)
#0x0800 IP(v4), Internet Protocol version 4
#0x0806 ARP, Address Resolution Protocol
#0x8137 IPX, Internet Packet eXchange (Novell)
#0x86dd IPv6, Internet Protocol version 6

packets[0].type

# Se pueden acceder a los campos de los headers
packets[0].src
packets[0].dst

# Ojo, es siempre del header "más afuera"
packets[0].src
# no es lo mismo que
packets[0][IP].src

# Podemos filtrar una lista de paquetes con una función lambda
# Por ejemplo, para buscar paquetes cuyo destino sea la dirección de broadcast
packets.filter(lambda x: x[Ether].dst == 'ff:ff:ff:ff:ff:ff')


################ DEMO ARP ################
# Vemos qué paquetes capturados son ARP
packets[ARP]

# Veamos alguno
packets[ARP][0]

# ¿Y si quiero ver sólo los broadcast?
packets[ARP].filter(lambda x: x.dst == 'ff:ff:ff:ff:ff:ff')
# ¿Y los unicast?
packets[ARP].filter(lambda x: x.dst != 'ff:ff:ff:ff:ff:ff')

# demo_broadcast
