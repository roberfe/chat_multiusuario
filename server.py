#!/usr/bin/env python3

import socket
import threading

def client_thread(client_socket,clients,usernames):

    username = client_socket.recv(1024).decode()
    usernames[client_socket] = username

    print(f"\nEl usuario {username} se ha conectado al chat")

    for client in clients:
        if client is not client_socket:
            client.sendall(f"\nEl usuario {username} ha entrado al chat\n".encode())

    while True:
        try:
            message = client_socket.recv(1024).decode()

            if not message:
                break

            for client in clients:
                if client is not client_socket:
                    client.sendall(f"{message}\n".encode())
        except:
            break
    
    client_socket.close()
    clients.remove(client_socket)
    del clients[client_socket]

def server_program():

    host = ''
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #TIME_WAIT
    server_socket.bind((host,port))
    server_socket.listen()

    print(f"\nEl servidor esta escucha de conexiones entrantes...")

    clients = [] 
    usernames = {}

    while True:

        client_socket, address = server_socket.accept()
        clients.append(client_socket)

        print(f"\nSe ha conectado un nuevo cliente: {address}")

        thread = threading.Thread(target=client_thread, args=(client_socket,clients,usernames))
        thread.daemon = True
        thread.start()
    
    server_socket.close()

if __name__ == '__main__':
    server_program()