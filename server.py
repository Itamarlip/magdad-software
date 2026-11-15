import socket


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
                # receive info from client
                print("Connection from: " + str(address))
                msgLen = 0
                payload = ""

                while 1:  # you probably want to limit this so it doesn't block forever
                        chunk = clientsocket.recv(1024).decode("utf-8")

                        if chunk == "" or msgLen >= 1024:  # we're done... max 1024 bytes in this case
                                break
                        else:
                                payload = payload + chunk
                                msgLen += len(chunk)

                # we now have info from the client
                response = self.doSomething(payload)

                # send response
                clientsocket.sendall(response.encode("utf-8"))

                clientsocket.close()

        def doSomething(self, payload):
                print("payload: " + payload)
                return "this is the response to the client"


if __name__ == "__main__":
        a = socketServer()  # this will block
		