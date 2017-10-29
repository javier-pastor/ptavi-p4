#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import time
import json

PORT = int(sys.argv[1])



class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    addr_dic = {}
    json_dic = {}

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        self.wfile.write(b"Hemos recibido tu peticion\r\n")
        #print('CLIENT IP ',self.client_address[0])
        #print('CLIENT PORT: ',self.client_address[1])

        while 1: # Read line by line what the client sent us

            line = self.rfile.read()
            if not line:
                break
            l_split = line.split()
            method = str(l_split[0])[2:-1]
            sec_expires = int((l_split[4]))
            dupla_addr = str(l_split[1])[2:-1].split(':')
            addr = dupla_addr[1]
            if method == 'REGISTER':

                self.addr_dic[addr] = self.client_address[0]
                self.json_dic[addr] = "address: " + self.client_address[0]
                self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
            if sec_expires == 0:
                del self.addr_dic[addr]

        print ("Registro de direcciones:\r\n"+str(self.addr_dic))
        self.register2json(addr, sec_expires);

    def register2json(self, addr, sec_expires):
        strings = time.strftime("%Y,%m,%d,%H,%M,%S")
        t = strings.split(',')
        numbers = [ int(x) for x in t ] # año mes dia hora minuto segundo 0 - 5
        hour = str(numbers[2]) + "-" + str(numbers[1]) + "-" + str(numbers[0]) + " " + str(numbers[3]) + ":" + str(numbers[4]) + ":" + str(numbers[5])
        self.json_dic[addr] = str(self.json_dic[addr]) + " expires: " + hour + " +" + str(sec_expires)
        #nice = self.addr_dic + numbers

        with open("registered.json", 'w') as file:
            json.dump(str(self.json_dic), file)

        self.json2registered()

    def json2registered(self):
        try:
            users = json.load(open('registered.json'))
            print(users)
        except:
            print("El fichero no existe")



if __name__ == "__main__":
    # Listens at localhost ('') and port PORT
    # and calls the SIPRegisterHandler class to manage the request
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)

    print("Lanzando servidor UDP de eco...")

    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
