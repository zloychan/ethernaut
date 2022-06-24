from brownie import network, Vault
from scripts.helpful import get_account, LOCAL_NETWORKS
import web3


def deploy(account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = Vault.deploy(32167, {"from": account}, publish_source=publish)
    print(
        f"Cotntract --Vault-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def main():
    owner_account = get_account()
    contract = deploy(owner_account)
    print(f"Contrackt lockacge: {contract.locked()}")
    if network.show_active() in LOCAL_NETWORKS:
        w3 = web3.Web3(web3.HTTPProvider("http://127.0.0.1:8545"))
    elif network.show_active() == "rinkeby":
        w3 = web3.Web3(
            web3.HTTPProvider(
                "https://rinkeby.infura.io/v3/bfcd4b27a9ae4840be1375009f61b8c9"
            )
        )
    else:
        print(network.show_active())
        raise f"No HTTP provider for network {network.show_active()}"
    password = w3.eth.getStorageAt(contract.address, 1).hex()
    print(f"our password is: {int(password, 16)}")
    tx = contract.unlock(password)
    tx.wait(1)
    print(f"Contrackt lockacge: {contract.locked()}")


if __name__ == "__main__":
    main()
