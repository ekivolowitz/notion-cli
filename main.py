#!/usr/bin/env python
from notion.client import NotionClient
import os
TOKEN_V2 = os.environ['TOKEN_V2']

if __name__ == '__main__':
    client = NotionClient(TOKEN_V2)


