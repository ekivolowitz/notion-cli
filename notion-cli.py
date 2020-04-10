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
from notion_cli.download_block import download_block

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
    download_parser = subparsers.add_parser('download', help='Download a block')

    encrypt_parser.add_argument('--asymmetric', action='store_true', help='Use asymmetric encryption')
    encrypt_parser.add_argument('--symmetric', action='store_true', help='Use symmetric encryption')
    encrypt_parser.add_argument('key', type=str, help='Filepath to key to encrypt data')
    encrypt_parser.add_argument('block_id', type=str, help="Notion.so block to encrypt")

    decrypt_parser.add_argument('--asymmetric', action='store_true', help='Use asymmetric decryption')
    decrypt_parser.add_argument('--symmetric', action='store_true', help='Use symmetric decryption')
    decrypt_parser.add_argument('key', type=str, help='Filepath to key to decrypt data')
    decrypt_parser.add_argument('block_id', type=str, help='Notion.so block to decrypt')

    download_parser.add_argument('block_id', type=str, help='ID of the block to download')
    download_parser.add_argument('export_type', type=str, help='Type of the output file. Options are \'markdown\', \'pdf\', and \'html\'')
    download_parser.add_argument('--event-name', type=str, help='Notion object you\'re exporting. Defaults to \'exportBlock\'.')
    download_parser.add_argument('--recursive', action='store_true', help='Recursively download all sub-blocks of this block. Defaults to false.')
    download_parser.add_argument('--time-zone', type=str, help='Timezone you\'re in. Defaults to \"America/Chicago\"')
    download_parser.add_argument('--locale', type='str', help='Locale options. Defaults to \'en\'')
    

    key_parser.add_argument('output', help='Output file for the newly generated key.')


    key_parser.set_defaults(func=gen_key)
    encrypt_parser.set_defaults(func=encrypt)
    decrypt_parser.set_defaults(func=decrypt)
    download_parser.set_defaults(func=download_block)
    return parser.parse_args()

if __name__ == '__main__':
    args = parser()
    args.func(args)
