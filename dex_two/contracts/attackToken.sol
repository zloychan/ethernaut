// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin2/contracts/token/ERC20/ERC20.sol";

contract AttackToken is ERC20 {
    constructor(uint256 initialSupply) ERC20("Attack", "ATTK") {
        _mint(msg.sender, initialSupply);
    }
}
