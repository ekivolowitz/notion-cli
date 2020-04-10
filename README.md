# notion-cli
Unofficial notion cli client.

There are features I wanted to see on Notion. This is a CLI tool that has that extended functionality. This CLI is built on [notion-py](https://github.com/jamalex/notion-py)

## Usage
### Quickstart
* Obtain the `token_v2` cookie in your browser while on Notion and export it like so:
```
$ export TOKEN_V2=<your_token_here>
```
* Make `notion-cli.py` executable
```
$ chmod +x notion-cli.py
```

This code looks for single blocks with text in between `begin-encrypt` and `end-encrypt`. Take the following block named Test-Block:

```
begin-encrypt
This is a test
end-encrypt
```

We will first need a symmetric key to encrypt with. We can get one with the following command:
```
$ ./notion-cli.py gen-key my-key
```
You should now have a file called `my-key`. Don't lose this file, or the contents of your encrypted section will be gone forever *gasp*!

You can get the ID by using `notion-py`'s `client.search_block("Test-Block")` command. You can then print out the ID of the block.

```
$ python3
Python 3.8.2 (default, Apr  4 2020, 21:08:09) 
[GCC 7.5.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from notion.client import NotionClient
>>> client = NotionClient("your_token_here")
>>> client.search_blocks("Test-Block")[0].children
[
  <TextBlock (id='e64f85da-ec00-4fbe-aeb3-711bf814c2c2', title='begin-encrypt\nThis is a test message\nend-encrypt')>,
  <TextBlock (id='346eb41e-1c5d-4341-9dd0-ac2a2e320612')>,
]
```

The TextBlock with the title is what we want. So let's take that ID. Now I'll run the command that will encrypt that Block. It will look like garbled crap to you, but I can decrypt it with the key that I generated.

```
$ ./notion-cli.py encrypt --symmetric my-key e64f85da-ec00-4fbe-aeb3-711bf814c2c2
```
Which turned the Block into:
```
begin-encrypt
gAAAAABekAMPM4RjH3V7OioKQp_-V9miudqHqYmmYan9o9CQwWk52Sx_T8wnhpICMoCtpYgHoAkdNXxO0GikrB-4-TWtZLXf56QG_7qY4dilGsT_aueqVzY=
end-encrypt
```

Now to read the encrypted portion on my local machine:
```
$ ./notion-cli.py decrypt --symmetric my-key e64f85da-ec00-4fbe-aeb3-711bf814c2c2
This is a test message
```
