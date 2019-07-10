import json
import re
import time

from mythril.exceptions import CriticalError
from mythril.mythril import MythrilAnalyzer, MythrilDisassembler, MythrilConfig
from theo.exploit.exploit import Exploit
from theo.exploit.exploit_item import ExploitItem


def find_exploits(rpc, contract, account, account_pk) -> Exploit:
    conf = MythrilConfig()

    if re.match(r"^https", rpc):
        rpchost = rpc[8:]
        rpctls = True
    else:
        rpchost = rpc[7:]
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
            txs.append(ExploitItem({"input": si["input"], "value": si["value"]}, rpc))

        exploits.append(Exploit(txs, rpc, contract, account, account_pk))

    return exploits
