import json
from theo.exploit.exploit import Exploit
from theo.exploit.exploit_item import ExploitItem


def load_file(file, rpc, contract, account, account_pk):
    with open(file) as f:
        exploit_list = json.load(f)

    exploits = []
    for exploit in exploit_list:
        txs = []
        for tx in exploit:
            txs.append(ExploitItem({"input": tx["input"], "value": tx["value"]}, rpc))

        exploits.append(Exploit(txs, rpc, contract, account, account_pk))

    return exploits
