from brownie import network, config, accounts


DECIMALS = 8
STARTING_PRICE = 2000 * (10**DECIMALS)
INITIAL_VALUE = 200000000000
LOCAL_NETWORKS = ["development", "ganache-local"]
FORKED_NETWORKS = ["mainnet-fork", "mainnet-fork-dev", "mainnet-fork-dev-alchemy"]


def get_account(index=None, id=None):
    account = None
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_NETWORKS
        or network.show_active() in FORKED_NETWORKS
    ):
        account = accounts[0]
        return account
    return accounts.add(config["wallets"]["from_key"])
