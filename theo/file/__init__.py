import json
from web3 import Web3
from theo.exploit.exploit import Exploit
from theo.exploit.tx import Tx
from theo import private_key_to_account


def exploits_from_file(
    file, rpcHTTP=None, rpcWS=None, rpcIPC=None, contract="", account_pk="", timeout=300
):
    with open(file) as f:
        exploit_list = json.load(f)

    if rpcIPC is not None:
        print("Connecting to IPC: {rpc}.".format(rpc=rpcIPC))
        w3 = Web3(Web3.IPCProvider(rpcIPC, timeout=timeout))
    elif rpcWS is not None:
        print("Connecting to WebSocket: {rpc}.".format(rpc=rpcWS))
        w3 = Web3(Web3.WebsocketProvider(rpcWS, websocket_kwargs={"timeout": timeout}))
    else:
        print("Connecting to HTTP: {rpc}.".format(rpc=rpcHTTP))
        w3 = Web3(Web3.HTTPProvider(rpcHTTP, request_kwargs={"timeout": timeout}))

    exploits = []

    for exploit in exploit_list:
        txs = []
        for tx in exploit:
            txs.append(
                Tx(
                    data=tx.get("data", "0x"),
                    value=tx.get("value", 0),
                    name=tx.get("name", ""),
                )
            )

        exploits.append(
            Exploit(
                txs=txs,
                w3=w3,
                contract=contract,
                account=private_key_to_account(account_pk),
                account_pk=account_pk,
            )
        )

    return exploits
