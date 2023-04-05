import struct, socket
INT_SIZE = 4

class Server:
    def __init__(self) -> None:
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        self.socket.connect((host, port))

    def recieve_message(self, length):
        buffer = b''
        bytesRead = 0
        while (bytesRead < length):
            nextBytes = self.socket.recv(length - bytesRead)
            bytesRead += len(nextBytes)
            buffer += nextBytes

        return buffer

    def get_message(self):
        length = struct.unpack("!I", self.recieve_message(INT_SIZE))[0]
        buffer = self.recieve_message(length)
        return buffer 

    def put_message(self, message: str):
        if len(message.strip()) == 0:
            return
        
        # convert message to ASCII encoded byte string
        length = len(message)
        bmessage = bytes(message, 'ASCII')

        # send length of message
        lengthMessage = struct.pack("!I", length)
        bytesSent = 0
        while (bytesSent < INT_SIZE):
            bytesSent += self.socket.send(lengthMessage[bytesSent:])

        # send actual message
        bytesSent = 0
        while (bytesSent < length):
            bytesSent += self.socket.send(bmessage[bytesSent:])


    def close(self):
        self.socket.close()