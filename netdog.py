# !/usr/bin/env python3
# coding=utf-8
# auther:AdianGg
# Blog:http://www.e-wolf.top

import os
import socket
import sys
import threading


class Client(object):
    """
    Run as client
    """
    def __init__(self, host, port, file_send="None"):
        # get params
        self.host = host
        self.port = port
        self.file_send = file_send
        self.connect()

    def connect(self):
        # connect to server

        try:
            address = (self.host, self.port)
            self.nd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.nd_socket.connect(address)
            print('[INFO]Connected!')
        except:
            print("[ERROR]Connect field")
            self.disconnect()
            sys.exit(0)
        if self.file_send == "None":

            # create 2 threads to use full duplex transmission
            send_thread = threading.Thread(target=self.send_message)
            recv_thread = threading.Thread(target=self.accept_message)
            send_thread.start()
            recv_thread.start()
        else:
            self.send_file()

    def send_message(self):
        while True:
            message_send = input().encode("utf-8")
            self.nd_socket.send(message_send)

    def accept_message(self):
        while True:
            message_recieve = str(self.nd_socket.recv(1024), 'utf-8')
            if message_recieve == b"" or message_recieve == "":
                print("[INFO]Remote disconnect")
                sys.exit(0)
            print("[Message][Remote]" + message_recieve)

    def send_file(self):
        print("[INFO]Send File Mode")
        print("[FILE]locate:" + self.file_send)
        try:
            f = open(self.file_send, 'rb')
            self.file_stream = f.read()
            print("[INFO]Sending file")
            self.nd_socket.sendall(self.file_stream)
        except IOError:
            print("[ERROR] File Error,Please Check")
            self.disconnect()
            sys.exit(0)

    def disconnect(self):
        self.nd_socket.close()


class Server(object):
    """
    Run as Server
    """
    def __init__(self, port, file_recv="None", shell=False):
        # Get params
        self.port = port
        self.file_recv = file_recv
        self.shell = shell
        self.listen()

    def listen(self):
        self.user_list = []
        # create a socket listener
        print("[INFO]NetDog listener is listening")
        nd_address = ('localhost', self.port)
        self.nd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nd_socket.bind(nd_address)
        # listen and set max listen num
        while True:
            self.nd_socket.listen()
            conn, addr = self.nd_socket.accept()
            if addr not in self.user_list:
                self.user_list.append(addr)
            print("[Connect]Client Connect")
            if self.file_recv == "None" and self.shell == False:
                # create 2 threads to use full duplex transmission
                send_thread = threading.Thread(target=self.send_message,
                                               args=(
                                                   conn,
                                                   addr,
                                               ))
                recv_thread = threading.Thread(target=self.accept_message,
                                               args=(
                                                   conn,
                                                   addr,
                                               ))
                send_thread.start()
                recv_thread.start()
            elif self.file_recv != "None":
                # recv file
                print("[INFO]waiting for file")
                self.accept_file()
            else:
                self.shell_mode()

    def send_message(self, conn, addr):
        # send message
        while True:
            message_send = input("Send to " + addr).encode('utf-8')
            conn.sendto(message_send, addr)

    def accept_message(self, conn, addr):
        #recieve message
        while True:
            message_recieve = str(conn.recv(1024), 'utf-8')
            if message_recieve == b"" or message_recieve == "":
                print("[INFO]Remote disconnect")
                sys.exit(0)
            print("[Message][%s]%s" % (addr, message_recieve))

    def accept_file(self):
        # recieve and write files
        print("[INFO]recieve file ......")
        file_stream = self.conn.recv(1000000)
        print("[INFO]write file.........")
        f = open(self.file_recv, "wb+")
        f.write(file_stream)
        f.close()

    def shell_mode(self):
        self.conn.send(
            "[INFO]Welcome to netdog command shell console".encode("utf-8"))
        while True:
            command = str(self.conn.recv(1024), "utf-8")
            result = os.popen(command).read()
            if not result:
                result = "[INFO]Command No Result\n"
            self.conn.send(result.encode("utf-8"))

    def close(self):
        self.nd_socket.close()


class Utils(object):
    """
    tools
    """
    def usage():
        print("""
        NetDog 1.0(http://www.e-wolf.top)
        Usage:python3 netdog.py [options]

        Client Option List
            -h host   set remote host
            -p port   set romote port
            -f /file  set local file location(Optional)
        
        Server Option List
            -l port   set listen mode open and appoint port
            -f /file  set recieve file location(Optional)
        
        Util Option List
            -shell       get the system shell



        Example:

        Connect to somewhere:
        python3 netdog.py -h 10.1.1.1 -p 123

        run as a server:
        python3 netdog.py -l 123 
        """)


if __name__ == "__main__":
    try:
        # Get Parameters from shell
        parameter = sys.argv[1:]
        # check mode
        if "-help" in parameter:
            # print readme
            Utils.usage()
        elif "-l" in parameter:
            # get port
            port = int(parameter[parameter.index("-l") + 1])
            # is file function use
            if "-f" in parameter:
                recieve_file = parameter[parameter.index("-f") + 1]
                NetDog = Server(port=port, file_recv=recieve_file)
            # is shell function use
            elif "-s" in parameter:
                NetDog = Server(port=port, shell=True)
            # just connect and chat
            else:
                NetDog = Server(port)
        # connect and check is scan function use
        elif "-h" in parameter and "-p" in parameter:
            host = parameter[parameter.index("-h") + 1]
            port = int(parameter[parameter.index("-p") + 1])
            #check if the mode is scan
            if "-scan" in parameter:
                Utils.portscan(host, port)
            # check if have the file transfer
            elif "-f" in parameter:
                file_send = parameter[parameter.index("-f") + 1]
                NetDog = Client(host=host, port=port, file_send=file_send)
            else:
                # just connect
                NetDog = Client(host=host, port=port)
        else:
            Utils.usage()
    except KeyboardInterrupt as e:
        print("[EXIT]exit")
