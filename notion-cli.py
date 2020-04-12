#!/usr/bin/env python
import argparse
import os
import sys
import time
import requests
import logging


from notion_cli.crypto import encrypt, decrypt
from notion_cli.genkey import gen_key
from notion_cli.download_block import download_block

try:
    TOKEN_V2 = os.environ['TOKEN_V2']
except:
    logging.error("Must provide a token to access notion with.")
    sys.exit(1)
try:
    if os.environ['LOG_LEVEL'] == '0':
        logging.disable()
    else:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
except:
    logging.info("No LOG_LEVEL environment variable set. Defaulting to logging all outputs")


def parser():
    parser = argparse.ArgumentParser(prog='notion-cli')

    subparsers = parser.add_subparsers(help='Sub commands of notion-cli')

    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt sub command')
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt sub command')
    download_parser = subparsers.add_parser('download', help='Download a block')
    key_parser = subparsers.add_parser('gen-key', help='Generate a key to encrypt or decrypt (assuming you will encrypt with the same key) with.')
 
    encrypt_parser.add_argument('--asymmetric', action='store_true', help='Use asymmetric encryption')
    encrypt_parser.add_argument('--symmetric', action='store_true', help='Use symmetric encryption')
    encrypt_parser.add_argument('key', type=str, help='Filepath to key to encrypt data')
    encrypt_parser.add_argument('block_id', type=str, help="Notion.so block to encrypt")

    decrypt_parser.add_argument('--asymmetric', action='store_true', help='Use asymmetric decryption')
    decrypt_parser.add_argument('--symmetric', action='store_true', help='Use symmetric decryption')
    decrypt_parser.add_argument('key', type=str, help='Filepath to key to decrypt data')
    decrypt_parser.add_argument('block_id', type=str, help='Notion.so block to decrypt')

    download_parser.add_argument('block_id', type=str, help='ID of the block to download')
    download_parser.add_argument('--export_type', type=str, help='Type of the output file. Options are \'markdown\', \'pdf\', and \'html\'')
    download_parser.add_argument('--event-name', type=str, help='Notion object you\'re exporting. Defaults to \'exportBlock\'.')
    download_parser.add_argument('--recursive', action='store_true', help='Recursively download all sub-blocks of this block. Defaults to false.')
    download_parser.add_argument('--time-zone', type=str, help='Timezone you\'re in. Defaults to \"America/Chicago\"')
    download_parser.add_argument('--locale', type=str, help='Locale options. Defaults to \'en\'')
    download_parser.add_argument('--disable-page-block-only', action='store_true', help="Will download any type of block, not just page blocks.")
    

    key_parser.add_argument('output', help='Output file for the newly generated key.')
    key_parser.add_argument('--asymmetric', action='store_true', help='Use asymmetric decryption')
    key_parser.add_argument('--symmetric', action='store_true', help='Use symmetric decryption')
 

    key_parser.set_defaults(func=gen_key)
    encrypt_parser.set_defaults(func=encrypt)
    decrypt_parser.set_defaults(func=decrypt)
    download_parser.set_defaults(func=download_block)

    return parser.parse_args(), parser

if __name__ == '__main__':
    args, parser = parser()
    try:
        args.func(args)
    except AttributeError:
        parser.print_help()
