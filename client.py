#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import socket
import sys

# Constantes. Dirección IP del servidor y contenido a enviar
SERVER = sys.argv[1]
PORT = int(sys.argv[2])
frase = ''

METHOD = sys.argv[3].upper()
ADDR = sys.argv[4]

LINE = METHOD + ' sip:' + ADDR + ' SIP/2.0\r\n\r\n'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PORT))
    print("Enviando:", LINE)
    my_socket.send(bytes(LINE+ '\r\n', 'utf-8'))
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))

print("Socket terminado.")
