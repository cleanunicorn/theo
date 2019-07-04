from web3 import Web3
import time


class TxPool:
    rpc = None
    w3 = None

    def __init__(self, rpc):
        self.rpc = rpc
        self.w3 = Web3(Web3.HTTPProvider(self.rpc))

    def wait_for_attack(self, contract, input):
        found_txs = []

        while len(found_txs) == 0:
            time.sleep(1)
            pending_txs = self.w3.txpool.content["pending"]

            for v in pending_txs:
                t = pending_txs[v]
                for idx in t:
                    if (t[idx]["to"] == contract) and (t[idx]["input"] == input):
                        found_txs.append(t[idx])

        return pending_txs

    def send_tx(self, tx):
        # Make sure the address is checksummed.
        tx["from"] = Web3.toChecksumAddress(tx["from"])
        tx["to"] = Web3.toChecksumAddress(tx["to"])

        tx_hash = self.w3.eth.sendTransaction(tx)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash, timeout=300)

        return tx_receipt
