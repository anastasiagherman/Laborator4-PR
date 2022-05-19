#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from threading import current_thread

client_nr = 0
def unique_client_name():
    global client_nr
    client_nr += 1
    return "user nr " + str(client_nr)

def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        addresses[client] = client_address
        Thread(target=handle_client, name=unique_client_name(), args=(client,)).start()


def handle_client(client):
    thread = current_thread()
    client_name = thread.name
    welcome = 'Welcome %s! If you ever want to quit, type exit.' % client_name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % client_name
    broadcast(bytes(msg, "utf8"))
    clients[client] = client_name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("exit", "utf8"):
            broadcast(msg, client_name+": ")
        else:
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % client_name, "utf8"))
            break


def broadcast(msg, prefix=""):  
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 100
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    accept_thread = Thread(target=accept_incoming_connections)
    accept_thread.start()
    accept_thread.join()
    SERVER.close()
