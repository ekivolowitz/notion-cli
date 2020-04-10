import logging

from cryptography.fernet import Fernet

def gen_key(args):
    logging.info("Generating key")
    key = Fernet.generate_key()
    with open(args.output, 'wb') as f:
        f.write(key)
    logging.info("Generated key and placed it into {}".format(args.output))

