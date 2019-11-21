# from argparse_prompt import PromptParser
import argparse
import code
import getpass
from web3 import Web3
from theo.version import __version__
from theo.scanner import exploits_from_mythril
from theo.file import exploits_from_file
from theo import *


def main():
    parser = argparse.ArgumentParser(
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
    rpc.add_argument("--rpc-ws", help="connect to this WebSockets RPC", default=None)
    rpc.add_argument("--rpc-ipc", help="connect to this IPC RPC", default=None)
    rpc.add_argument("--timeout", help="timeout for RPC connections", default=300)

    # Account to use for attacking
    parser.add_argument("--account-pk", help="the account's private key")

    # Contract to monitor
    parser.add_argument(
        "--contract", help="contract to interact with", metavar="ADDRESS"
    )

    # Find exploits with Mythril
    parser.add_argument(
        "--skip-mythril",
        help="skip scanning the contract with Mythril",
        default=False,
        action="store_true",
    )

    # Load exploits from file
    parser.add_argument(
        "--load-file", help="load exploit from file", default=None
    )

    # Print version and exit
    parser.add_argument(
        "--version", action="version", version="Version: {}".format(__version__)
    )

    # Parse all arguments
    args = parser.parse_args()

    # Get account from the private key
    if args.account_pk is None:
        args.account_pk = getpass.getpass(
            prompt="The account's private key (input hidden)\n> "
        )
    args.account = private_key_to_account(args.account_pk)

    if args.contract is None:
        args.contract = input("Contract to interact with\n> ")

    args.contract = Web3.toChecksumAddress(args.contract)
    args.account = Web3.toChecksumAddress(args.account)

    start_repl(args)


def start_repl(args):
    exploits = []

    # Transactions to frontrun
    if args.skip_mythril is False:
        print(
            "Scanning for exploits in contract: {contract}".format(
                contract=args.contract
            )
        )
        exploits += exploits_from_mythril(
            rpcHTTP=args.rpc_http,
            rpcWS=args.rpc_ws,
            rpcIPC=args.rpc_ipc,
            contract=args.contract,
            account_pk=args.account_pk,
            timeout=args.timeout,
        )
    if args.load_file is not None:
        exploits += exploits_from_file(
            file=args.load_file,
            rpcHTTP=args.rpc_http,
            rpcWS=args.rpc_ws,
            rpcIPC=args.rpc_ipc,
            contract=args.contract,
            account_pk=args.account_pk,
            timeout=args.timeout,
        )

    if len(exploits) == 0:
        print("No exploits found. You're going to need to load some exploits.")
    else:
        print("")
        print("Found exploits(s):")
        print(exploits)

    # Add local tools for console
    w3 = Web3(
        Web3.HTTPProvider(args.rpc_http, request_kwargs={"timeout": args.timeout})
    )
    from theo.exploit.exploit import Exploit
    from theo.exploit.tx import Tx

    # Imports for REPL
    import os, atexit, readline, rlcompleter

    # Load history
    history_path = os.path.join(os.environ["HOME"], ".theo_history")
    if os.path.isfile(history_path):
        readline.read_history_file(history_path)
    # Trigger history save on exit
    atexit.register(readline.write_history_file, history_path)
    # Load variables
    vars = globals()
    vars.update(locals())
    # Start REPL
    readline.set_completer(rlcompleter.Completer(vars).complete)
    readline.parse_and_bind("tab: complete")
    del os, atexit, readline, rlcompleter
    code.InteractiveConsole(vars).interact(
        banner="""
Tools available in the console:
- `exploits` is an array of loaded exploits found by Mythril or read from a file
- `w3` an initialized instance of web3py for the provided HTTP RPC endpoint
- `dump()` writing a json representation of an object to a local file

Check the readme for more info:
https://github.com/cleanunicorn/theo

Theo version {version}.

""".format(
            version=__version__
        )
    )

    print("Shutting down")
