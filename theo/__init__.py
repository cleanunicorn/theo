import time, json


def private_key_to_account(pk: str):
    from eth_keys import keys
    from web3 import Web3

    account = keys.PrivateKey(Web3.toBytes(hexstr=pk))
    return account.public_key.to_checksum_address()


def dump(ob=None, filename=None):
    """Dumps the provided object to a file in json format.
    """
    if filename is None:
        filename = "{name}.json".format(name=time.time_ns())

    pickled = json.dumps(ob)
    with open(filename, "w") as f:
        f.write(pickled)
