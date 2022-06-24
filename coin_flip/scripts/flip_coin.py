from brownie import CoinFlip, network, chain
from scripts.helper import get_account, LOCAL_NETWORKS
from Crypto.Hash import keccak
from web3 import Web3, EthereumTesterProvider
from time import sleep
from brownie.exceptions import RPCRequestError




def deploy(account):
    publish = False
    if network.show_active() not in LOCAL_NETWORKS:
        publish = True
    contract = CoinFlip.deploy({"from": account}, publish_source=publish)
    print(
        f"Cotntract --Fallout-- deployed at {contract.address} from {account.address}"
    )
    return contract


def main():

    factor = 57896044618658097711785492504343953926634992332820282019728792003956564819968
    account = get_account()
    contract = deploy(account)
    for i in range(10):
        try:
            print(f"Last block number = {len(chain)}")
            guess = int(int(chain[len(chain) - 1]["hash"].hex(), 16) / factor)
            tx = contract.flip(guess, {"from": account})
            tx.wait(1)
            
        
            print(f"Consecutive Wins: {contract.consecutiveWins()}")
        except RPCRequestError:
            if network.show_active() not in LOCAL_NETWORKS:
                print("Sleeping 300")
                sleep(300)
            else:
                print("Sleeping 10")
                sleep(10)
        


if __name__ == "__main__":
    main()