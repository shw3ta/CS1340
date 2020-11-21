"""
server with threading
"""

import socket
import getmac
import datetime
from threading import Thread


def time_in_range(mode):
    start = datetime.time(14, 50)
    end = datetime.time(16, 20)
    now = datetime.datetime.now().time()
    t = datetime.time(now.hour, now.minute, now.second)

    if mode == "within":
        if start <= t <= end:
            print(t)
            return True
        else:
            return False
    if mode == "after":
        if t > end:
            return True
        else:
            return False


def count():
    a, b, c, d = 0, 0, 0, 0
    for key, value in answers:
        if value in 'aA':
            a = a+1
        if value in 'bB':
            b = b+1
        if value in 'cC':
            c = c+1
        if value in 'dD':
            d = d+1
    result = "The number of responses each option has received is :-\na: " + str(a) + " b: " + str(b) + " c: " \
             + str(c) + " d: " + str(d)
    return result


def proc(csocket, ip):
    response = ''
    mac = getmac.get_mac_address(ip=ip)

    welcome_message = "We are running a quiz. You can participate in the quiz any time between " \
                      "2:50 PM - 4:20 PM.\n Reply with a `1' if you want to participate now" \
                      " (time of connection MUST be between 2:50 PM - 4:20 PM);\n Reply with a `2' if you " \
                      "want to see the results (time of connection MUST be after 4:20 PM);" \
                      "\n Reply with a `3' otherwise."
    csocket.send(welcome_message.encode())

    # receiving client choice
    choice = csocket.recv(1024).decode()

    if choice == '1':

        if time_in_range("within"):
            # re-trial from same client disallowed
            if mac not in answers:
                mcq = "\n\nWhat does HTTP stand for? " \
                      "\na. Hat Trick Time Protocol" \
                      "\nb. Hyperactive Tungsten Tachyon Phaser" \
                      "\nc. Hyper-Text Transfer Protocol " \
                      "\nd. Hyper-Text Tracking Protocol\n"
                csocket.send(mcq.encode())
                conf = '1'
                csocket.send(conf.encode())

                answer = csocket.recv(1024).decode()

                answers.update({mac: answer})
                response = "\nThank you for participating.\nYour response is registered against your MAC address: " + str(
                    mac)

            else:
                response = "Whoops! No second tries allowed. Server disconnecting from socket..."

        else:
            response = "You cannot participate in the quiz at the moment."

    if choice == '2':
        if time_in_range("after"):
            response = count()

        else:
            response = "The quiz is not over yet."

    csocket.send(response.encode())
    print("Server disconnecting from socket...\nListening again...")
    csocket.close()


answers = {}  # dictionary keyed by MAC, value = answer

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 5546))
server_socket.listen()
print(f"Quiz Server listening at port {5546}!")

# server is always listening
while True:
    (csocket, address) = server_socket.accept()
    ip = address[0]
    port = address[1]
    Thread(target=proc, args=(csocket, ip)).start()
