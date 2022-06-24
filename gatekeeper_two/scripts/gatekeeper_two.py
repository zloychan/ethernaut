from brownie import network, GatekeeperTwo, Attack
from scripts.helpful import get_account, LOCAL_NETWORKS
import web3


def deploy_gate(account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = GatekeeperTwo.deploy({"from": account}, publish_source=publish)
    print(
        f"Cotntract --GatekeeperTwo-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def deploy_key(account, addr):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = Attack.deploy(addr, {"from": account}, publish_source=publish)
    print(
        f"Cotntract --Attack-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def main():
    owner_account = get_account(0)
    attacker_account = get_account(1)
    contract_gate = deploy_gate(owner_account)
    print(f"Owner address: {owner_account}")
    print(f"Attacker address: {attacker_account}")
    print(f"Gate owner: {contract_gate.entrant()}")
    contract_key = deploy_key(attacker_account, contract_gate.address)
    print(f"Gate owner: {contract_gate.entrant()}")


if __name__ == "__main__":
    main()
