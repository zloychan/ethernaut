from brownie import network, Privacy
from scripts.helpful import get_account, LOCAL_NETWORKS
import web3


def deploy(account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    w3 = web3.Web3(web3.HTTPProvider("http://127.0.0.1:8545"))
    data = [w3.toBytes(text=str("testing string to bytes")), 3333, 12345]
    contract = Privacy.deploy(data, {"from": account}, publish_source=publish)
    print(
        f"Cotntract --Privacy-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def main():
    owner_account = get_account()
    contract = deploy(owner_account)
    print(f"Contract lockage: {contract.locked()}")
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
    secret = w3.eth.getStorageAt(contract.address, 5).hex()
    print(f"Secret type: {type(secret)}")
    print(f"Secret: {secret}")
    # secret = w3.toBytes(text=str(secret))
    print("\n\n\n<<<<< UNLOCKING >>>>>\n\n\n")
    # Странное дельце, но обрезается задняя часть 32 байт и остается передняя, та что с 00000
    tx = contract.unlock(0x0)
    tx.wait(1)
    print(f"Contract lockage: {contract.locked()}")
    test_string = contract.test().hex().rstrip("0")  # Отрезаем линие нулю справа
    print(f"Test string: {test_string}")
    if len(test_string) % 2 != 0:
        print("len of test_string % != 0")
        test_string = test_string + "0"
    test_string = bytes.fromhex(test_string).decode("utf8")
    print(f"String: {test_string}")


if __name__ == "__main__":
    main()
