from brownie import network, Dex, SwappableToken
from scripts.helpful import get_account, LOCAL_NETWORKS
import web3


def deploy_dex(account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = Dex.deploy({"from": account}, publish_source=publish)
    print(f"Cotntract --Dex-- deployed at {contract.address} from {account.address}\n")
    return contract


def deploy_token(account, address, name, symbol, supply):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = SwappableToken.deploy(
        address, name, symbol, supply, {"from": account}, publish_source=publish
    )
    print(
        f"Cotntract --{name} {symbol}-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def main():
    owner_account = get_account(0)
    attacker_acount = get_account(1)
    contract_dex = deploy_dex(owner_account)
    token_1 = deploy_token(owner_account, contract_dex.address, "TOKEN1", "TKN1", 110)
    token_2 = deploy_token(owner_account, contract_dex.address, "TOKEN2", "TKN2", 110)
    print("Adding tokens")
    tx = contract_dex.setTokens(token_1.address, token_2.address)
    tx.wait(1)
    print(
        f"Contract owner balance Token 1: {contract_dex.balanceOf(token_1.address, owner_account.address)}",
        f"Contract owner balance Token 2: {contract_dex.balanceOf(token_2.address, owner_account.address)}",
    )
    print(
        f"Contract attacker balance Token 1: {contract_dex.balanceOf(token_1.address, attacker_acount.address)}",
        f"Contract attacker balance Token 2: {contract_dex.balanceOf(token_2.address, attacker_acount.address)}",
    )
    print("Transferin 10 tokens to attacker account")
    tx = token_1.approve(contract_dex.address, 1000)
    tx.wait(1)
    tx = token_2.approve(contract_dex.address, 1000)
    tx.wait(1)
    tx = token_1.transfer(attacker_acount.address, 10, {"from": owner_account.address})
    tx.wait(1)
    tx = token_2.transfer(attacker_acount.address, 10, {"from": owner_account.address})
    tx.wait(1)
    print(
        f"Contract owner balance Token 1: {contract_dex.balanceOf(token_1.address, owner_account.address)}",
        f"Contract owner balance Token 2: {contract_dex.balanceOf(token_2.address, owner_account.address)}",
    )
    print(
        f"Contract attacker balance Token 1: {contract_dex.balanceOf(token_1.address, attacker_acount.address)}",
        f"Contract attacker balance Token 2: {contract_dex.balanceOf(token_2.address, attacker_acount.address)}",
    )
    print("Approving transactions")

    print("Transferin 100 tokens to contract address")
    # tx = token_1.transfer(contract_dex.address, 100, {"from": owner_account.address})
    # tx.wait(1)
    # tx = token_2.transfer(contract_dex.address, 100, {"from": owner_account.address})
    # tx.wait(1)
    tx = contract_dex.addLiquidity(
        token_1.address, 100, {"from": owner_account.address}
    )
    tx.wait(1)
    tx = contract_dex.addLiquidity(
        token_2.address, 100, {"from": owner_account.address}
    )
    tx.wait(1)
    print(
        f"Contract owner balance Token 1: {contract_dex.balanceOf(token_1.address, owner_account.address)}",
        f"Contract owner balance Token 2: {contract_dex.balanceOf(token_2.address, owner_account.address)}",
    )
    print(
        f"Contract balance Token 1: {contract_dex.balanceOf(token_1.address, contract_dex.address)}",
        f"Contract balance Token 2: {contract_dex.balanceOf(token_2.address, contract_dex.address)}",
    )
    print(
        f"Contract attacker balance Token 1: {contract_dex.balanceOf(token_1.address, attacker_acount.address)}",
        f"Contract attacker balance Token 2: {contract_dex.balanceOf(token_2.address, attacker_acount.address)}",
    )
    print("\n\n\n <<<<<<<<<<<<<<<<< ATTACKING >>>>>>>>>>>>>>>>>>> \n\n\n")
    # print(
    #     f"Allowance Token 1 owner: {token_1.allowance(owner_account.address, owner_account.address)}"
    # )
    # print(
    #     f"Allowance Token 2 owner: {token_1.allowance(owner_account.address, owner_account.address)}"
    # )
    # print(
    #     f"Allowance Token 1 attacker: {token_1.allowance(owner_account.address, attacker_acount.address)}"
    # )
    # print(
    #     f"Allowance Contract T1: {token_1.allowance(owner_account.address, contract_dex.address)}"
    # )
    # print(
    #     f"Allowance Token 2 attacker: {token_2.allowance(owner_account.address, attacker_acount.address)}"
    # )
    # print(
    #     f"Allowance Contract T2: {token_2.allowance(owner_account.address, contract_dex.address)}"
    # )

    # print(f"Price: {contract_dex.getSwapPrice(token_1.address, token_2.address, 10)}")
    # tx = contract_dex.swap(
    #     token_1.address, token_2.address, 10, {"from": attacker_acount.address}
    # )
    # print(
    #     f"Contract balance Token 1: {contract_dex.balanceOf(token_1.address, contract_dex.address)}",
    #     f"Contract balance Token 2: {contract_dex.balanceOf(token_2.address, contract_dex.address)}",
    # )
    # print(
    #     f"Contract attacker balance Token 1: {contract_dex.balanceOf(token_1.address, attacker_acount.address)}",
    #     f"Contract attacker balance Token 2: {contract_dex.balanceOf(token_2.address, attacker_acount.address)}",
    # )
    # print(f"Price: {contract_dex.getSwapPrice(token_1.address, token_2.address, 10)}")

    print(
        f"Contract owner balance Token 1: {contract_dex.balanceOf(token_1.address, owner_account.address)}",
        f"Contract owner balance Token 2: {contract_dex.balanceOf(token_2.address, owner_account.address)}",
    )
    print(
        f"Contract balance Token 1: {contract_dex.balanceOf(token_1.address, contract_dex.address)}",
        f"Contract balance Token 2: {contract_dex.balanceOf(token_2.address, contract_dex.address)}",
    )
    print(
        f"Contract attacker balance Token 1: {contract_dex.balanceOf(token_1.address, attacker_acount.address)}",
        f"Contract attacker balance Token 2: {contract_dex.balanceOf(token_2.address, attacker_acount.address)}",
    )


if __name__ == "__main__":
    main()
