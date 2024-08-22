# Socket server program

# import threading
# import socket

# def handle_client(client_socket):
#     while True:
#         data = client_socket.recv(1024).decode()
#         if not data:
#             break
#         print("from connected user: " + str(data))
#         data = input(' jayalakshmi> ')
#         client_socket.send(data.encode())  

#     client_socket.close()  

# def server_program():
#     # host = "192.168.1.58"
#     host = "138.68.140.83"
#     # host = socket.gethostname()
#     print(host)
#     port = 5039 

#     server_socket = socket.socket()  
#     server_socket.bind((host, port))  

#     server_socket.listen(14)
#     client_sockets = []

#     while True:
#         # Accept incoming connections
#         client_socket, address = server_socket.accept()
#         print("Connection from: " + str(address))
#         client_sockets.append(client_socket)
#         threading.Thread(target=handle_client, args=(client_socket,)).start()

# if __name__ == '__main__':
#     server_program()

import socket as Socket
import threading as Threading

Client_sockets_dict = {}
HOST = '138.68.140.83'
PORT = 5645

Server_socket = Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM)

Server_socket.bind((HOST, PORT))
Server_socket.listen(5)
print("Server is listening on ", HOST, ":", PORT)

def Handle_client(Client_socket):
    try:
        Name = Client_socket.recv(1024)
        Client_sockets_dict[Client_socket] = Name.decode()
        while True:

            Data = Client_socket.recv(1024)
            if not Data:
                break

            Message = Data.decode()

            if Message == 'exit':

                Client_socket.send(Message.encode())
                Client_sockets_dict.pop(Client_socket)
            else:

                print("Received message: \n" + Client_sockets_dict[Client_socket] + ": " + Message + "\n")

                for Key in Client_sockets_dict.keys():
                    if Key != Client_socket:
                        Key.send(((Client_sockets_dict[Client_socket] + ": " + Message).encode()))
    except ConnectionResetError:
        print("Conection closed")
        Client_sockets_dict.pop(Client_socket)
        Client_socket.close()

while True:

    Client_socket, Client_address = Server_socket.accept()
    print("Accepted connection from", Client_address)

    client_handler = Threading.Thread(target = Handle_client, args = (Client_socket,))
    client_handler.start()

