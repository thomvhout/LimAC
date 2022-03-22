# Server from: https://realpython.com/python-sockets

import selectors
import socket
import types

import runner

HOST = "127.0.0.1"
PORT = 8082

sel = selectors.DefaultSelector()
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((HOST, PORT))
lsock.listen()
print("listening on", (HOST, PORT))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

acServer = runner.acServer(False)

# TODO fix incomplete/extra data sent: https://www.binarytides.com/receive-full-data-with-the-recv-socket-function-in-python/


def processInput(data: str):
    dataString = data.decode("utf-8")
    if dataString == "start":
        return acServer.start()
    elif dataString == "stop":
        return acServer.die()
    elif dataString[0:2] == "t;":
        acServer.changeTrack(dataString)
        return " "
    else:
        print("Command '{}' not handled".format(dataString))
        return "Could not parse command"


def accept_wrapper(sock):
    conn, addr = sock.accept()
    print("Accepted connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = ""
        try:
            recv_data = sock.recv(8192)  # Should be ready to read
        except:
            print("[EXCEPTION]: Recv crashed again lol")
            try:
                sel.unregister(sock)
                sock.close()
            except:
                print("[EXCEPTION]: Failed to close socket")
        if recv_data:
            data.outb += recv_data
        else:
            print("Closing connection to", data.addr)
            try:
                sel.unregister(sock)
                sock.close()
            except:
                print("[EXCEPTION]: Failed to close socket")
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            #print("echoing", repr(data.outb), "to", data.addr)
            print("Received", repr(data.outb), "from", data.addr)
            result = processInput(data.outb)
            # Prevent infinite data sendback
            if result == None or result == "":
                result = "No result"
            # Should be ready to write
            #   sent = sock.send(data.outb)
            print(result)
            sent = sock.send(bytes(result, 'utf-8'))
            data.outb = data.outb[sent:]


while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)
