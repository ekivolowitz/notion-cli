#!/usr/bin/env python
import argparse
import os
from notion.client import NotionClient
from notion.block import *
from pprint import pprint
import time
import requests
import logging


from notion_cli.crypto import encrypt, decrypt
from notion_cli.genkey import gen_key

if os.environ['LOG_LEVEL'] == '0':
    logging.disable()
else:
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def parser():
    parser = argparse.ArgumentParser(prog='notion-cli')

    subparsers = parser.add_subparsers(help='Sub commands of notion-cli')

    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt sub command')
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt sub command')
    key_parser = subparsers.add_parser('gen-key', help='Generate a key to encrypt with.')

    encrypt_parser.add_argument('--asymmetric', action='store_true', help='Use asymmetric encryption')
    encrypt_parser.add_argument('--symmetric', action='store_true', help='Use symmetric encryption')
    encrypt_parser.add_argument('key', type=str, help='Filepath to key to encrypt data')
    encrypt_parser.add_argument('block_id', type=str, help="Notion.so block to encrypt")

    decrypt_parser.add_argument('--asymmetric', action='store_true', help='Use asymmetric decryption')
    decrypt_parser.add_argument('--symmetric', action='store_true', help='Use symmetric decryption')
    decrypt_parser.add_argument('key', type=str, help='Filepath to key to decrypt data')
    decrypt_parser.add_argument('block_id', type=str, help='Notion.so block to decrypt')


    key_parser.add_argument('output', help='Output file for the newly generated key.')


    key_parser.set_defaults(func=gen_key)
    encrypt_parser.set_defaults(func=encrypt)
    decrypt_parser.set_defaults(func=decrypt)
    return parser.parse_args()

if __name__ == '__main__':
    args = parser()
    args.func(args)
