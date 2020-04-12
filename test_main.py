from notion_cli.download_block import download_block

import os.path

class Args():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def test_download():

    test_block_page = 'c5e4f16d-2b4b-4321-942f-624025710f52' 
    test_block_page_name = 'Test Block.md'
    args = Args(block_id=test_block_page)

    assert download_block(args)
    assert os.path.exists(test_block_page_name)
