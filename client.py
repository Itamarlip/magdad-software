from time import sleep
import pickle
import socket
import struct

import cv2

def talkToServer():
        # get a socket connection to the server
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        connection.connect(("10.148.17.116", 1234))       # IP address and port of the server
        cam = cv2.VideoCapture(0)
        print("Connected to server, sending frames...")
        cam.set(3, 320);
        cam.set(4, 240);

        img_counter = 0

        while True:
                ret,frame=cam.read()
                # Serialize frame
                data = pickle.dumps(frame)

                # Send message length first
                message_size = struct.pack("L", len(data)) ### CHANGED
                print("Sending frame {} of size {}".format(img_counter, len(data)))
                message = struct.pack(">I", len(data)) + data
                connection.sendall(message)
        
        connection.shutdown(socket.SHUT_WR)



if __name__ == "__main__":
        talkToServer()
