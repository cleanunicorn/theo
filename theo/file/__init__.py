import json
from web3 import Web3
from theo.exploit.exploit import Exploit
from theo.exploit.exploit_item import ExploitItem


def load_file(file, rpcHTTP=None, rpcWS=None, rpcIPC=None, contract="", account="", account_pk=""):
    with open(file) as f:
        exploit_list = json.load(f)

    if rpcIPC is not None:
        print("Connecting to IPC: {rpc}.".format(rpc=rpcIPC))
        w3 = Web3(
            Web3.IPCProvider(rpcIPC)
        )
    elif rpcWS is not None:
        print("Connecting to WebSocket: {rpc}.".format(rpc=rpcWS))
        w3 = Web3(
            Web3.WebsocketProvider(rpcWS)
        )
    else:
        print("Connecting to HTTP: {rpc}.".format(rpc=rpcHTTP))
        w3 = Web3(
            Web3.HTTPProvider(rpcHTTP)
        )

    exploits = []
    for exploit in exploit_list:
        txs = []
        for tx in exploit:
            txs.append(
                ExploitItem(
                    tx_data={"input": tx.get("input", "0x"), "value": tx.get("value", "")}
                )
            )

        exploits.append(
            Exploit(
                txs=txs,
                w3=w3,
                contract=contract,
                account=account,
                account_pk=account_pk,
            )
        )

    return exploits
