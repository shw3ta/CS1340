"""
client wants to attempt one single mcq
"""

import socket


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# local host IP
client_socket.connect(('127.0.0.1', 5545))
reply = client_socket.recv(1024).decode()
print(reply)
choice = input("Enter here: ")
client_socket.send(choice.encode())

if choice == '3':
    print("Disconnecting from server...")

else:
    # receiving something from server if not disconnected
    if choice == '1':

        mcq = client_socket.recv(1024).decode()
        mcq_lock = client_socket.recv(1024).decode()
        print(mcq)
        if mcq_lock == '1':
            # {
            chosen_option = input("Enter appropriate alphabet (a/b/c/d) to answer:")
            while chosen_option not in 'abcdABCD':
                chosen_option = input("Invalid option, enter again: ")
            client_socket.send(chosen_option.encode())
            # } buggy

        # response from server about answer
        s_response = client_socket.recv(1024).decode()
        mcq_counter = 1
        print(s_response)

    if choice == '2':
        s_response = client_socket.recv(1024).decode()
        print(s_response)

client_socket.close()