#!/usr/bin/env python
import argparse
import os
from notion.client import NotionClient
from notion.block import *
from pprint import pprint
import time
import requests
TOKEN_V2 = os.environ['TOKEN_V2']

def update_text(record):
    print(record.title)


def download_url(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

if __name__ == '__main__':
    client = NotionClient(TOKEN_V2)
    #children = client.search_blocks("Notion API")[0].children

    obj = client.get_block("2245e4f7-b75f-4927-82f6-87db1ae0fa49")
    obj.title = f"SHAMALAMADINGDONG"
    
    data = {
        "task" : {
            "eventName" : "exportBlock",
            "request" : {
                "blockId" : "2245e4f7-b75f-4927-82f6-87db1ae0fa49",
                "recursive" : False,
                "exportOptions" : {
                    "exportType" : "markdown",
                    "timeZone" : "America/Chicago",
                    "locale" : "en"
                }
            }
        }
    }

    task_id = client.post("enqueueTask", data).json()['taskId']
    response = client.post("getTasks", {"taskIds" : [task_id]})
    task = response.json()
    pprint(task)
    while 'exportURL' not in task['results'][0]['status']:
        time.sleep(0.1)
        response = client.post('getTasks', {'taskIds' : [task_id]})
        task = response.json()
    url = task['results'][0]['status']['exportURL']
    download_url(url, "test.zip")
