from socket import *
import keygen
import encryption
import yaml
import sys

GUARD_IP = None
RES_PORT = 35001            # Port for TOR connections
REQ_PORT = 35000

def read_IP():
    """Read IP of next node
    """
    global GUARD_IP
    with open('./config.yaml', 'r') as f:
        ips = yaml.full_load(f)
        GUARD_IP = ips['NEXT']

def get_layers():
    """Get number of layers for encryption

    Returns
    -------
    list
        List of parameters to use for each encryption layer
    """
    layer_list = []
    with open('./config.yaml', 'r') as f:
        layers = yaml.full_load(f)
        layer_list = layers['layers']

    return layer_list


# Ref; https://stackoverflow.com/a/17697651
def recvall(sock):
    """Get data from socket

    Parameters
    ----------
    sock : int
        Socket descriptor

    Returns
    -------
    bytes
        Received data from socket
    """
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data


def connect_to_guard(msg):
    """Connect to guard node

    Parameters
    ----------
    msg : string
        Message to send
    """
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((GUARD_IP, REQ_PORT))
        # Convert message to bytes
        sock.send(msg)
        sock.shutdown(SHUT_WR)

def accept_connection(secrets_list):
    """Listen for responses

    Parameters
    ----------
    secrets_list : list
        List of secrets to use for decryption
    """
    with socket(AF_INET, SOCK_STREAM) as sock2:
        sock2.bind(('', REQ_PORT))
        sock2.listen()
        while True:
            conn, addr = sock2.accept()
            print("Connection accepted from:", addr)
            while True:
                # data = conn.recv(1024)
                data = recvall(conn)
                if not data:
                    break
                for secret in secrets_list:
                    for key, counter in secret.items():
                        data = encryption.decrypt(data, key, counter)
                print("New data recevied: ", data.decode('ISO-8859-1'))

layer = sys.argv[1]
print("Sending data: ", layer)


layer_list = get_layers()

secrets_list = []

# Add secrets to dictionary and encrypt each layer.
# Done in reverse to the innermost encryption layer will be decrypted at the last node
check = 0
for i in range(len(layer_list)-1, -1, -1):
    key, counter = keygen.generate_secret(layer_list[i])
    secrets_dict = {key:counter}
    secrets_list.append(secrets_dict)
    layer = encryption.encrypt(layer, key, counter)
    check += 1

read_IP()

connect_to_guard(layer)
accept_connection(secrets_list)