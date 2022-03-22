import socket

HOST = "127.0.0.1"
PORT = 8082


def sendToServer(data: str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        try:
            server.connect((HOST, PORT))
            server.sendall(data.encode("utf-8"))
        except:
            return "Unable to contact server"
        data = server.recv(8192)
        print("Received: " + data.decode('utf-8'))
        return data.decode('utf-8')
