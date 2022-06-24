from brownie import network, config, Zero
from scripts.helpful_scripts import get_account, LOCAL_NETWORKS


def deploy(account, password):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    zero = Zero.deploy(password, {"from": account}, publish_source=publish)
    print(f"Zero Chalange Deployed at =>>> {zero.address} from {account.address}")
    return zero


def main():
    password = "pass"
    account = get_account()
    contract = deploy(account, password)
    print(f"The password is: {contract.password()}")
    print(f"The infoNum is: {contract.infoNum()}")
    print(f"The info is: {contract.info()}")
    print(f"The info1 is: {contract.info1()}")
    print(f"The info2 is: {contract.info2('hello')}")
    print(f"The info42 is: {contract.info42()}")
    print(f"The method7123949 is: {contract.method7123949()}")
    print(f"The cleared is: {contract.getCleared()}")
    print(f"Autentificating with password: {password}")
    tx = contract.authenticate(password)
    tx.wait(1)
    print(f"The cleared is: {contract.getCleared()}")


if __name__ == "__main__":
    main()
