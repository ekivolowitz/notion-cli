import logging

from Crypto.PublicKey import RSA
from cryptography.fernet import Fernet

def gen_symmetric_key(args):
    logging.info("Generating key")
    key = Fernet.generate_key()
    with open(args.output, 'wb') as f:
        f.write(key)
    logging.info("Generated key and placed it into {}".format(args.output))

def gen_asymmetric_key(args):
    ''' 
    args - should have output. Refer to it with args.output

    TODO Use Crypto library like this:
    https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html
    To support generating a pub key / priv key combo. 

    The code should look pretty similar to gen_symmetric_key.

    The output of this code should be two files:

    args.output
    args.output.pub

    Where (args.output) is the private key file and (args.output).pub is the public key.

    '''
    logging.info("Generating asymmetric key combo")

    key = RSA.generate(2048)
   
    with open(args.output, 'wb') as f:
        f.write(key.export_key('PEM'))
    with open(args.output + '.pub', 'wb') as f:
        f.write(key.publickey().export_key('PEM'))
    logging.info(f'Generated pub/priv key combo: {args.output}, {args.output}.pub')

def gen_key(args):
    if args.symmetric:
        gen_symmetric_key(args)
    elif args.asymmetric:
        gen_asymmetric_key(args)
    else:
        logging.error("No sym or asym flag")
        print("Must specify symmetric or asymmetric cryptography.")
