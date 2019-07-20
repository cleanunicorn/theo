from argparse_prompt import PromptParser
import argparse
import code
import json
from theo.server import Server
from theo.scanner import exploits_from_mythril
from theo.file import exploits_from_file
from theo import private_key_to_account


def main():
    parser = PromptParser(
        description="Monitor contracts for balance changes or tx pool.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # RPC connection type
    # Required HTTP connection
    parser.add_argument(
        "--rpc-http", help="Connect to this HTTP RPC", default="http://127.0.0.1:8545"
    )
    # Optional connections
    rpc = parser.add_argument_group("RPC connections")
    rpc.add_argument("--rpc-ws", help="Connect to this WebSockets RPC", default=None)
    rpc.add_argument("--rpc-ipc", help="Connect to this IPC RPC", default=None)

    # Account to use for attacking
    parser.add_argument("--account-pk", help="The account's private key", secure=True)

    # Contract to monitor
    parser.add_argument(
        "--contract", help="Contract to monitor", type=str, metavar="ADDRESS"
    )

    # Exploits to load
    source = parser.add_argument_group("Where to load exploits from")
    source.add_argument(
        "--source",
        choices=["mythril", "file", None],
        help="Choose between: mythril (find transactions automatically with mythril), file (use the transactions specified in a JSON file).",
        default=None,
    )
    source.add_argument(
        "--file",
        help="The file which contains the transactions to frontrun",
        metavar="FILE",
    )

    args = parser.parse_args()

    # Get account from the private key
    args.account = private_key_to_account(args.account_pk)

    start_repl(args)


def start_repl(args):
    exploits = []

    # Transactions to frontrun
    if args.source == "mythril":
        print(
            "Scanning for exploits in contract: {contract}".format(
                contract=args.contract
            )
        )
        exploits = exploits_from_mythril(
            rpcHTTP=args.rpc_http,
            rpcWS=args.rpc_ws,
            rpcIPC=args.rpc_ipc,
            contract=args.contract,
            account_pk=args.account_pk,
        )
    if args.source == "file":
        exploits = [
            exploits_from_file(
                file=args.txs_file,
                rpcHTTP=args.rpc_http,
                rpcWS=args.rpc_ws,
                rpcIPC=args.rpc_ipc,
                contract=args.contract,
                account_pk=args.account_pk,
            )
        ]

    if len(exploits) == 0:
        print(
            "No exploits found. You're going to need to load some exploits with one of:"
        )
        print(
            'load_file(file="/path/to/file.json", rpcHTTP="http://localhost:8545", contract="0xContractAddress", account_pk="0xYourPrivateKey")'
        )
        print(
            'load_mythril(rpcHTTP="http://localhost:8545", contract="0xContractAddress", account_pk="0xYourPrivateKey")'
        )
    else:
        print("Found exploits(s)", exploits)

    # Load history
    history_path = "./.theo_history"
    def save_history(historyPath=history_path):
        import readline

        readline.write_history_file(history_path)

    import os
    import readline
    if os.path.isfile(history_path):
        readline.read_history_file(history_path)
    # Trigger history save on exit
    import atexit
    atexit.register(save_history)
    # Load variables
    vars = globals()
    vars.update(locals())
    # Start REPL
    import rlcompleter
    readline.set_completer(rlcompleter.Completer(vars).complete)
    readline.parse_and_bind("tab: complete")
    del os, atexit, readline, rlcompleter, save_history
    code.InteractiveConsole(vars).interact()

    print("Shutting down")
