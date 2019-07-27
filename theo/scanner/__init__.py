import json
import re
from mythril.exceptions import CriticalError
from mythril.mythril import MythrilAnalyzer, MythrilDisassembler, MythrilConfig
from mythril.ethereum.interface.rpc.client import EthJsonRpc
from web3 import Web3
from theo.exploit.exploit import Exploit
from theo.exploit.tx import Tx
from theo import private_key_to_account


def exploits_from_mythril(
    rpcHTTP="http://localhost:8545",
    rpcWS=None,
    rpcIPC=None,
    timeout=300,
    contract="",
    account_pk="",
    strategy="bfs",
    modules=["ether_thief", "suicide"],
    transaction_count=3,
    execution_timeout=120,
    max_depth=32,
    loop_bound=3,
    disable_dependency_pruning=False,
    onchain_storage_access=True,
    enable_online_lookup=False,
):
    if re.match(r"^https", rpcHTTP):
        host, port = rpcHTTP[8:].split(":")
        rpc_tls = True
    else:
        host, port = rpcHTTP[7:].split(":")
        rpc_tls = False

    try:
        # Disassembler
        disassembler = MythrilDisassembler(
            eth=EthJsonRpc(host=host, port=port, tls=rpc_tls),
            solc_version=None,
            solc_args=None,
            enable_online_lookup=enable_online_lookup,
        )
        disassembler.load_from_address(contract)
        # Analyzer
        analyzer = MythrilAnalyzer(
            strategy=strategy,
            disassembler=disassembler,
            address=contract,
            execution_timeout=execution_timeout,
            max_depth=max_depth,
            loop_bound=loop_bound,
            disable_dependency_pruning=disable_dependency_pruning,
            onchain_storage_access=onchain_storage_access,
        )
        # Generate report
        report = analyzer.fire_lasers(
            modules=modules, transaction_count=transaction_count
        )
    except CriticalError as e:
        print(e)
        return []

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

    for ri in report.issues:
        txs = []
        issue = report.issues[ri]

        for si in issue.transaction_sequence["steps"]:
            txs.append(Tx(data=si["input"], value=si["value"], name=si["name"]))

        exploits.append(
            Exploit(
                txs=txs,
                w3=w3,
                contract=contract,
                account=private_key_to_account(account_pk),
                account_pk=account_pk,
                title=issue.title,
                description=issue.description,
                swc_id=issue.swc_id,
            )
        )

    return exploits
