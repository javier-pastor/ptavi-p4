#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys

PORT = int(sys.argv[1])



class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    addr_dic = {}

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        self.wfile.write(b"Hemos recibido tu peticion\r\n")
        print('CLIENT IP ',self.client_address[0])
        print('CLIENT PORT: ',self.client_address[1])

        while 1: # Read line by line what the client sent us
            line = self.rfile.read()
            if not line:
                break
            l_split = line.split()
            l_split_method = str(l_split[0])[2:-1]
            l_split_addr = str(l_split[1])[2:-1]
            if l_split_method == 'REGISTER':
                addr = l_split_addr.split(':')
                self.addr_dic[addr[1]] = self.client_address[0]
                self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')

        print ("Diccionario de direcciones:\r\n"+str(self.addr_dic))


if __name__ == "__main__":
    # Listens at localhost ('') and port PORT
    # and calls the SIPRegisterHandler class to manage the request
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
