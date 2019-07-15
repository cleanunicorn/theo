import json
import re
import time
from mythril.exceptions import CriticalError
from mythril.mythril import MythrilAnalyzer, MythrilDisassembler, MythrilConfig
from web3 import Web3
from theo.exploit.exploit import Exploit
from theo.exploit.exploit_item import ExploitItem


def find_exploits(rpcHTTP, rpcWS, contract, attacker) -> Exploit:
    conf = MythrilConfig()

    if re.match(r"^https", rpcHTTP):
        rpchost = rpcHTTP[8:]
        rpctls = True
    else:
        rpchost = rpcHTTP[7:]
        rpctls = False

    conf.set_api_rpc(rpchost, rpctls)

    try:
        disassembler = MythrilDisassembler(eth=conf.eth, enable_online_lookup=False)
        disassembler.load_from_address(contract)
        analyzer = MythrilAnalyzer(
            strategy="bfs",
            disassembler=disassembler,
            address=contract,
            execution_timeout=120,
            max_depth=32,
            loop_bound=3,
            disable_dependency_pruning=False,
            onchain_storage_access=True,
        )
    except CriticalError as e:
        print(e)

    report = analyzer.fire_lasers(
        modules=["ether_thief", "suicide"], transaction_count=3
    )

    exploits = []
    for ri in report.issues:
        txs = []
        issue = report.issues[ri]

        for si in issue.transaction_sequence["steps"]:
            txs.append(ExploitItem(tx_data={"input": si["input"], "value": si["value"]}))

        exploits.append(Exploit(txs=txs, w3=Web3(Web3.WebsocketProvider(rpcWS, websocket_kwargs={'timeout': 60})), contract=contract, account=attacker))

    return exploits
