from Crypto.Cipher import AES

def encrypt(msg, key, counter):
    key = key.to_bytes(16, 'little')
    counter = counter.to_bytes(16, 'little')

    crypto = AES.new(key, AES.MODE_CTR, counter=lambda:counter)
    encryped = crypto.encrypt(msg)
   
    return encryped

def decrypt(msg, key, counter):
    key = key.to_bytes(16, 'little')
    counter = counter.to_bytes(16, 'little')

    crypto = AES.new(key, AES.MODE_CTR, counter=lambda:counter)
    decrypted = crypto.decrypt(msg)
   
    return decrypted