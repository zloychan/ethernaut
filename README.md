Here solutions to [Ethernaut](https://ethernaut.openzeppelin.com) with [brownie](https://eth-brownie.readthedocs.io/en/stable/) and python scripts.


## Installation:
  1) Install [python](https://www.python.org) 3.9.5 or greater
  2) Install [Ganache](https://trufflesuite.com/ganache)
  3) Create venv `python -m venv venv`
  4) Activate venv `source venv/bin/activate`(Linux, MacOs) or `venv\Scripts\activate`(Windows)
  5) Install reqirements `pip intall -r requirements.txt`
  
## Run Scripts:<br>
  Example: re_entrancy
  1) `cd re_entrancy`
  2) `brownie run scripts/re_entrancy.py`
  3) If you want to use rinkeby test net you can modify re_entrancy/.env<br>
    export PRIVATE_KEY = with owner wallet private key<br>
    export ATTACKER_PRIVATE_KEY = with attacker wallet private key<br>
    export WEB3_INFURA_PROJECT_ID = with [Infura](https://infura.io) project id<br>
    export ETHERSCAN_TOKEN = with [etherscan](https://etherscan.io) token<br>
  
   4) run `brownie run scripts/re_entrancy.py --network=rinkeby`
   5) Read output
