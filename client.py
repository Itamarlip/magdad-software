import socket

def talkToServer(message):
        # get a socket connection to the server
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        connection.connect(("172.20.10.4", 1234))       # IP address and port of the server
        print("HERE")
        # send the message
        connection.send(message.encode("utf-8"))

        # shut down the send, so the server knows we're done talking
        connection.shutdown(socket.SHUT_WR)

        # get the response from the server
        msgLen = 0
        payload = ""

        while 1:        # you probably want to limit this so it doesn't block forever\
                chunk = connection.recv(1024).decode("utf-8")
                if chunk == "" or msgLen >= 1024:  # we're done... max 1024 bytes in this case
                        break
                else:
                        payload = payload + chunk
                        msgLen += len(chunk)

        connection.close()

        return payload, msgLen

if __name__ == "__main__":
        response, msgLen = talkToServer("Hello Dolly!")
        print (response)
