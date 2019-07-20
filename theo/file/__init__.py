import json
from web3 import Web3
from theo.exploit.exploit import Exploit
from theo.exploit.tx import Tx
from theo import private_key_to_account


def exploits_from_file(
    file, rpcHTTP=None, rpcWS=None, rpcIPC=None, contract="", account_pk=""
):
    with open(file) as f:
        transaction_list = json.load(f)

    if rpcIPC is not None:
        print("Connecting to IPC: {rpc}.".format(rpc=rpcIPC))
        w3 = Web3(Web3.IPCProvider(rpcIPC))
    elif rpcWS is not None:
        print("Connecting to WebSocket: {rpc}.".format(rpc=rpcWS))
        w3 = Web3(Web3.WebsocketProvider(rpcWS))
    else:
        print("Connecting to HTTP: {rpc}.".format(rpc=rpcHTTP))
        w3 = Web3(Web3.HTTPProvider(rpcHTTP))

    txs = []
    for tx in transaction_list:
        txs.append(Tx(data=tx.get("input", "0x"), value=tx.get("value", 0)))

    exploit = Exploit(
        txs=txs,
        w3=w3,
        contract=contract,
        account=private_key_to_account(account_pk),
        account_pk=account_pk,
    )

    return exploit
