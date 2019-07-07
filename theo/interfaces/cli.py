import argparse
import psycopg2
import code
import json
from theo.server import Server
from theo.scanner import find_exploits
from theo.file import load_file


def main():
    parser = argparse.ArgumentParser(
        description="Monitor contracts for balance changes or tx pool."
    )

    # Monitor tx pool
    tx_pool = parser.add_argument_group("Monitor transaction pool")
    tx_pool.add_argument(
        "--rpc", help="Connect to this RPC", default="http://127.0.0.1:8545"
    )
    tx_pool.add_argument("--account", help="Use this account to send transactions from")

    # Contract to monitor
    parser.add_argument(
        "--contract", help="Contract to monitor", type=str, metavar="ADDRESS"
    )

    # Transactions to frontrun
    tx_monitor = parser.add_argument_group("Transactions to wait for")
    tx_monitor.add_argument(
        "--txs",
        choices=["mythril", "file"],
        help="Choose between: mythril (find transactions automatically with mythril), file (use the transactions specified in a JSON file).",
        default="mythril",
    )
    tx_monitor.add_argument(
        "--txs-file",
        help="The file which contains the transactions to frontrun",
        metavar="FILE",
    )

    # Run mode
    parser.add_argument(
        "run_mode",
        choices=["tx-pool"],
        help="Choose between: balance (not implemented: monitor contract balance changes), tx-pool (if any transactions want to call methods).",
    )

    args = parser.parse_args()
    # print(args.__dict__)

    if args.run_mode == "tx-pool":
        exec_tx_pool(args)


def exec_tx_pool(args):

    # Transactions to frontrun
    if args.txs == "mythril":
        print(
            "Scanning for exploits in contract: {contract}".format(
                contract=args.contract
            )
        )
        exploits = find_exploits(args.rpc, args.contract, args.account)
    if args.txs == "file":
        exploits = load_file(
            file=args.txs_file,
            rpc=args.rpc,
            contract=args.contract,
            account=args.account,
        )

    if len(exploits) == 0:
        print("No exploits found")
        return

    print("Found exploits(s)", exploits)

    # Start interface
    code.interact(local=locals())

    print("Shutting down")
