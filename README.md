# notion-cli
Unofficial notion cli client.

There are features I wanted to see on Notion. This is a CLI tool that has that extended functionality. This CLI is built on [notion-py](https://github.com/jamalex/notion-py)

The first feature I built in was a symmetric encrypt/decrypt tool that allows you to encrypt part of a block so that you and the people you share the key with can decrypt it locally on your or their machine. This addresses the issue presented by Chet from the Notion team about why Notion doesn't support End to End Encryption: "End-to-end encrypted search is a fundamentally challenging problem. We use Elasticsearch which has all kinds of fancy language models to make your search results better. I'm not sure this is possible to do with e2e encryption. An alternative would be to have an encrypted-at-rest local elasticsearch cluster running in your desktop/mobile app. This is surely going to churn away your CPU/memory though."

This allows for your document to remain unencrypted **EXCEPT** for the sections that you choose to be encrypted. It puts the power of security in your hands, which I like. Very Niiiiice.

I have a million and two features I'd like to implement, but I just started this a couple of hours ago and I'm very tired. I'll be adding new features soon. One that I'm excited about is asymmetric cryptography support so that you can deliver data on your document to specific people and you won't have to share a key with them!

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
