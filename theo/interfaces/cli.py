import argparse
from theo.server import Server


def main():
    parser = argparse.ArgumentParser(
        description="Monitor contracts for balance changes or tx pool."
    )

    # Server
    # TODO: listen to this and save them to the postgres database
    server = parser.add_argument_group("Server")
    server.add_argument(
        "--server",
        help="Start server and save new vulnerabilities in the database.",
        metavar="",
    )
    server.add_argument(
        "--port", help="Port to listen on.", metavar="PORT_NUMBER", default=8080
    )
    server.add_argument(
        "--host", help="Address to listen on.", metavar="IP_ADDRESS", default="0.0.0.0"
    )

    # Postgres
    # TODO: login to PostgreSQL
    postgres = parser.add_argument_group("Postgres")
    postgres.add_argument(
        "--postgres",
        help="Connect to this PostgreSQL database.",
        metavar="postgresql://someone@example.com/database?connect_timeout=10",
    )

    # Check balance
    # TODO: monitor contract balance
    balance = parser.add_argument_group("Monitor balance")
    balance.add_argument(
        "--balance", help="Enable balance monitoring for the contracts", metavar=""
    )

    # Check tx pool
    # TODO: monitor tx pool
    tx_pool = parser.add_argument_group("Monitor transaction pool")
    tx_pool.add_argument("--tx-pool", help="", metavar="")

    # Run mode
    run_mode = parser.add_argument(
        "run_mode",
        choices=["balance", "tx-pool", "server"],
        help="Choose between: balance (monitor contract balance changes), tx-pool (if any transactions want to call methods) or server (save new vulnerabilities in the database).",
    )

    args = parser.parse_args()
    print(args.__dict__)

    if args.run_mode == "server":
        exec_server(args)


def exec_server(args):
    print("Running server")
    server = Server(args.host, args.port)
    server.start()
    print("Shutting down")
