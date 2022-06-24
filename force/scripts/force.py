from brownie import network, Force, Attack
from pytest import PytestAssertRewriteWarning
from scripts.helpful import get_account, LOCAL_NETWORKS
import web3


def deploy_force(account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = Force.deploy({"from": account}, publish_source=publish)
    print(
        f"Cotntract --Force-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def deploy_attack(address, account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = Attack.deploy(address, {"from": account}, publish_source=publish)
    print(
        f"Cotntract --Force-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def main():
    owner = get_account(0)
    attacker = get_account(1)
    contract_force = deploy_force(owner)
    print(f"Contract balance: {contract_force.balance()}")
    contract_attack = deploy_attack(contract_force.address, attacker)
    print(f"Contract balance: {contract_force.balance()}")
    tx = contract_attack.attack({"from": attacker.address, "value": 1})
    tx.wait(1)
    print(f"Contract balance: {contract_force.balance()}")


if __name__ == "__main__":
    main()
