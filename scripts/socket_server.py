import socket
import sys
from time import sleep


def send_code(user_socket, code):
    print(f'Sending {code}')
    user_socket.send(bytes(code + '\n', "utf-8"))

if __name__ == '__main__':

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('localhost', 9999))
    s.listen(5)

    while True:
        # now our endpoint knows about the OTHER endpoint.
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established.")

        sleep_time = 0.005
        for _ in range(100):
            sleep(sleep_time)
            send_code(clientsocket, 'M3 S2000')
            sleep(sleep_time)
            send_code(clientsocket, 'M123')
            sleep(sleep_time)
            send_code(clientsocket, 'M3 S4000')
            sleep(sleep_time)
            send_code(clientsocket, 'M123')



