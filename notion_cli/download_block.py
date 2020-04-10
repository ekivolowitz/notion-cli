import time
import os
from requests import Session, HTTPError, get
from zipfile import ZipFile

def _get_task_id(response):
    """
    When you export a file, notion creates a task to make the file with the 'enqueueTask' endpoint.
    Then another method looks at the task ID and returns the file when the task finishes.
    So, we need to save the taskId into a variable. This is a helper function to do that.
    """
    return response.json()['taskId']

# Source from https://requests.readthedocs.io/en/master/user/quickstart/#raw-response-content
def _download_url(url, save_path, chunk_size=128):
    """
    Downloads the zip file and saves it to a file.
    url - string of the url from which to download.
    save_path - string of the file name to output the zip file into.
    chunk_size = size of the chunk. This is adjustable. See the documentation for more info.
    """
    r = get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

def _unzip_file(file, delete=True):
    """
    Helper function to unzip the zipped download.
    file - string of the zip file name
    delete - delete the zip file or not.
    """
    with ZipFile(file) as zipObj:
        zipObj.extractall()
    if delete:
        os.remove(file)


def download_block(client, block_id, export_type, event_name="exportBlock", recursive=False, time_zone="America/Chicago", locale="en"):
    """
    block_id - id of the block. Should be a string.
    export_type - Type of the output file. The options are 'markdown', 'pdf', 'html'
    eventName - notion object you're exporting. I haven't seen anything other than exportBlock yet.
    recursive - include sub pages or not.
    time_zone - I don't know what values go here. I'm in the Chicago timezone (central) and this is what I saw in the request.
    locale - client explanatory.
    TODO: If export_type are 'pdf' or 'html', there is another field in exportOptions called 'pdfFormat'. It should be set to "Letter".
          This needs to be implemented.
    TODO: Add support for downloading a list of blocks
    TODO: Review this code. Does it suck? Error handling? This is version 0 of this method and my first open source contribution.
          Give me some criticisms so I can improve as a programmer!
    """
    tmp_zip = 'tmp.zip'
    data = {
        "task" : {
            "eventName" : event_name,
            "request" : {
                "blockId" : block_id,
                "recursive" : recursive,
                "exportOptions" : {
                    "exportType" : export_type,
                    "timeZone" : time_zone,
                    "locale" : locale
                }
            }
        }
    }

    task_id = client.post("enqueueTask", data).json()['taskId']
    response = client.post("getTasks", {"taskIds" : [task_id]})

    task = response.json()

    # This is a simple way to ensure that we're getting the data when it's ready.
    while 'status' not in task['results'][0]:
        time.sleep(0.1)
        response = client.post('getTasks', {'taskIds' : [task_id]})
        task = response.json()

    while 'exportURL' not in task['results'][0]['status']:
        time.sleep(0.1)
        response = client.post('getTasks', {'taskIds' : [task_id]})
        task = response.json()

    url = task['results'][0]['status']['exportURL']

    _download_url(url, tmp_zip)
    _unzip_file(tmp_zip)
