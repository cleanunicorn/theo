import json
from web3 import Web3
from theo.exploit.exploit import Exploit
from theo.exploit.exploit_item import ExploitItem


def load_file(file, rpcHTTP, rpcWS, contract, account):
    with open(file) as f:
        exploit_list = json.load(f)

    exploits = []
    for exploit in exploit_list:
        txs = []
        for tx in exploit:
            txs.append(ExploitItem(tx_data={"input": tx.get("input", ""), "value": tx.get("value", "")}))

        exploits.append(Exploit(txs=txs, w3=Web3(Web3.WebsocketProvider(rpcWS, websocket_kwargs={'timeout': 60})), contract=contract, account=account))

    return exploits
