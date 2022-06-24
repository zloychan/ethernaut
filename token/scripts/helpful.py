from brownie import network, config, accounts


DECIMALS = 8
STARTING_PRICE = 2000 * (10**DECIMALS)
INITIAL_VALUE = 200000000000
LOCAL_NETWORKS = ["development", "ganache-local"]
FORKED_NETWORKS = ["mainnet-fork", "mainnet-fork-dev", "mainnet-fork-dev-alchemy"]


def get_account(index=None, id=None):
    account = None
    if index:
        if network.show_active() in LOCAL_NETWORKS:
            return accounts[index]
        if network.show_active() not in LOCAL_NETWORKS and index == 0:
            return accounts.add(config["wallets"]["owner"])
        if network.show_active() not in LOCAL_NETWORKS and index == 1:
            return accounts.add(config["wallets"]["attacker"])
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_NETWORKS
        or network.show_active() in FORKED_NETWORKS
    ):
        account = accounts[0]
        return account
    return accounts.add(config["wallets"]["owner"])