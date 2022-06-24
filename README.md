Here solutions to https://ethernaut.openzeppelin.com with brownie and python scripts.


Installation:
  1) Install python 3.9.5 or greater
  2) Install Ganache from https://trufflesuite.com/ganache
  3) Create venv "python -m venv venv"
  4) Activate venv "source venv/bin/activate"(Linux, MacOs) or "venv\Scripts\activate"(Windows)
  5) Install reqirements "pip intall -r requirements.txt"
  
Run Scripts:
  Example: re_entrancy
  1) cd re_entrancy
  2) brownie run scripts/re_entrancy.py
  3) If yuo want to use rinkeby test net you can modify re_entrancy/.env
    export PRIVATE_KEY = with owner wallet private key
    export ATTACKER_PRIVATE_KEY = with attacker wallet private key
    export WEB3_INFURA_PROJECT_ID = with https://infura.io project id
    export ETHERSCAN_TOKEN = etherscan token
    
    and "run brownie run scripts/re_entrancy.py --network=rinkeby"
   4) Read output
