import os
from notion.client import NotionClient

def get_client():
    token_v2 = os.environ['TOKEN_V2']
    return NotionClient(token_v2)
