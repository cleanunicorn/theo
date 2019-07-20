def private_key_to_account(pk: str):
    from eth_keys import keys
    from web3 import Web3

    account = keys.PrivateKey(Web3.toBytes(hexstr=pk))
    return account.public_key.to_checksum_address()
