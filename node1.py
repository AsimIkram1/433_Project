from socket import *
import keygen
import encryption
import yaml

REQ_PORT = 35000            # Port for TOR connections
RES_PORT = 35001
FORWARD_TO = None

initial_address = []

def read_IP():
    global FORWARD_TO
    with open('./node_config.yaml', 'r') as f:
        ips = yaml.full_load(f)
        FORWARD_TO = ips['NEXT']

def get_layer():
    layer = None
    with open('./node_config.yaml', 'r') as f:
        temp_layer = yaml.full_load(f)
        layer = temp_layer['layer']

    return layer
    

def recvall(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data

def accept_connection(check, key, counter):
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.bind(('', REQ_PORT))
        sock.listen()
        while True:
            conn, addr = sock.accept()
            initial_address.append(addr[0])
            print("Connection accepted from:", addr)
            while True:
                # Receive data from client
                # data = conn.recv(1024)
                data = recvall(conn)
                if not data:
                    break
                # Send data to next node
                if check == 'incoming':
                    data = encryption.decrypt(data, key, counter)
                    send_msg(data, FORWARD_TO, REQ_PORT)
                    check = 'outgoing'
                else:
                    data = encryption.encrypt(data, key, counter)
                    print(data)
                    send_msg(data, initial_address[0], REQ_PORT)
                    check = 'incoming'


def send_msg(msg, host, port):
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((host, port))
        # Convert message to bytes
        # msg = msg.encode('utf-8')
        sock.send(msg)
        sock.shutdown(SHUT_WR)


read_IP()
layer = get_layer()
temp_key1, counter1 = keygen.generate_secret(layer)
accept_connection('incoming', temp_key1, counter1)
