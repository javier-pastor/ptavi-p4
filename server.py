#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import json
import socketserver
import time


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    dic_addr = {}

    def handle(self):
        line = self.rfile.read().decode('utf-8')
        l_split = line.split()
        self.json2registered()
        method = l_split[0]
        sec_expires = l_split[3]
        if method == 'REGISTER':
            addr = l_split[1].split(':')[-1]
            ip_user = self.client_address[0]
            if sec_expires == 'Expires:':
                expires = time.strftime('%Y-%m-%d %H:%M:%S',
                                        time.gmtime(time.time() +
                                                    int(l_split
                                                        [4])))
                self.dic_addr[addr] = [{'address': ip_user},
                                                        {'expires': expires}]

                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        self.check_expires()
        self.register2json()
        print(self.dic_addr)

    def check_expires(self):
        expired_users = []
        for usuario in self.dic_addr:
            time_now = time.strftime('%Y-%m-%d %H:%M:%S',
                                     time.gmtime(time.time()))
            if time_now >= self.dic_addr[usuario][1]['expires']:
                expired_users.append(usuario)

        for usuario in expired_users:
            del self.dic_addr[usuario]

    def register2json(self):
        fich_json = open('registered.json', 'w')
        codigo_json = json.dumps(self.dic_addr)
        fich_json.write(codigo_json)
        fich_json.close()

    def json2registered(self):
        try:
            fich_json = open('registered.json', 'r')
            self.dic_addr = json.load(fich_json)
        except:
            pass


if __name__ == "__main__":
    serv = socketserver.UDPServer(('', int(sys.argv[1])), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
