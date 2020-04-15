import os
import logging
import re

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from cryptography.fernet import Fernet
from .client import get_client

START = "begin-encrypt"
END = "end-encrypt"

def _get_key(filepath):
    fp = os.path.expanduser(os.path.expandvars(filepath))

    logging.info(f"_get_key filepath is: {fp}")

    if not os.path.exists(fp):
        logging.error("filepath does not exist")
        return None

    with open(filepath, 'rb') as f:
        return f.read()

def _symmetric_encrypt_plaintext(key, plaintext):
    f = Fernet(key)

    if type(plaintext) == str:
        logging.info("Type of args.plaintext is string")
        plaintext = bytes(plaintext, encoding='utf8') 
    elif type(plaintext) == bytes:
        logging.info("Type of args.plaintext is bytes")
    else:
        logging.error("plaintext is neither string or bytes.")
        return None

    cipher = f.encrypt(plaintext).decode('utf-8')

    logging.info(f"Ciphertext generated: {cipher}") 

    return cipher

def _symmetric_decrypt_ciphertext(key, ciphertext):
    f = Fernet(key)

    if type(ciphertext) == str:
        logging.info("Type of ciphertext is string")
        ciphertext = bytes(ciphertext, encoding='utf8')
    elif type(plaintext) == bytes:
        logging.info("Type of ciphertext is bytes")

    plaintext = f.decrypt(ciphertext)

    return plaintext

def _asymmetric_encrypt_plaintext(key, plaintext):
    pass

def _asymmetric_decrypt_ciphertext(key, ciphertext):
    pass

def _find_text_to_use(block):
    text = block.title

    if text.count(START) > 1 or text.count(END) > 1:
        logging.error("More than one start or end token")
        return None, None, None
    #logging.info(f"Block title is {text}")
    
    start = text.find(START) + len(START)
    end = text.find(END)

    return text[start + 1: end - 1]

def symmetric_encrypt(args):
    client = get_client()
    key = _get_key(args.key)
    if key is None:
        logging.error("Key does not exist.")
        print(f"The key: \"{args.key}\" does not exist. Please generate a key with the gen-key command and retry")
        return None
    if type(key) != bytes:
        logging.error("Type of key is not bytes.")
        return None

    block = client.get_block(args.block_id)

    plaintext = _find_text_to_use(block)

    if plaintext != None:
        block.title = block.title.replace(plaintext, _symmetric_encrypt_plaintext(key, plaintext))


def symmetric_decrypt(args):
    client = get_client()
    key = _get_key(args.key)
    if key is None:
        logging.error("Key does not exist")
        return None
    if type(key) != bytes:
        logging.error("Type of key is not bytes.")
        return None
    
    block = client.get_block(args.block_id)

    ciphertext = _find_text_to_use(block)

    print(_symmetric_decrypt_ciphertext(key, ciphertext).decode('utf8'))

def asymmetric_encrypt(args):
    print("No yet supported")
    '''
    client = get_client()

    key = _get_key(args.key)
    
    if key is None:
        logging.error('Key does not exist')
        return None

    if type(key) != bytes:
        logging.error("Type of key is not bytes.")
        return None
    
    block = client.get_block(args.block_id)

    plaintext = _find_text_to_use(block)

    if plaintext != None:
        data = _asymmetric_encrypt_plaintext(key, plaintext)
        print(data.decode('cp1252'))
        # block.title = block.title.replace(plaintext, _asymmetric_encrypt_plaintext(key, plaintext))
    '''
    

def asymmetric_decrypt(args):
    print("Not yet supported")


def encrypt(args):
    if args.symmetric:
        symmetric_encrypt(args)
    elif args.asymmetric:
        asymmetric_encrypt(args)
    else:
        logging.error("Encryption must be symmetric or asymmetric")
        print("You must specify either --symmetric or --asymmetric")

def decrypt(args):
    if args.symmetric:
        symmetric_decrypt(args)
    elif args.asymmetric:
        asymmetric_decrypt(args)
    else:
        logging.error("Encryption must be symmetric or asymmetric")
        print("You must specify either --symmetric or --asymmetric")
