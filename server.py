import pickle
import socket
import struct

import cv2


class socketServer:
        def __init__(self):
                # create an INET, STREAMing socket to listen on
                self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.serversocket.settimeout(1000)  # you'll want to handle this better
                print("socket created")
                # bind the socket to public host and port
                self.serversocket.bind(("0.0.0.0", 1234))  # 1234 is the port used here, but whatever you like
                print(socket.gethostbyname(socket.gethostname()))
                # become a server socket, for 10 connections max
                self.serversocket.listen(10)
                print("socket now listening")
                while 1:
                        # do something with that connection
                        (clientsocket, address) = self.serversocket.accept()
                        self.process(clientsocket, address)

        def process(self, clientsocket, address):
                conn = clientsocket
                print("Got connection from", address)
                data = b''
                payload_size = struct.calcsize("L")

                while True:
                        while len(data) < payload_size:
                                data += conn.recv(4096)
                                print("Recv: {}".format(len(data)))

                        packed_msg_size = data[:payload_size]
                        data = data[payload_size:]
                        msg_size = struct.unpack(">I", packed_msg_size)[0]
                        print("msg_size: {}".format(msg_size))
                        
                        # Retrieve all data based on message size
                        while len(data) < msg_size:
                                data += conn.recv(4096)

                        frame_data = data[:msg_size]
                        data = data[msg_size:]

                        frame = pickle.loads(frame_data)
                        print("received frame of size {}".format(len(frame_data)))
                        # Display
                        cv2.imshow('frame', frame)
                        cv2.waitKey(1)

if __name__ == "__main__":
        a = socketServer()  # this will block
		