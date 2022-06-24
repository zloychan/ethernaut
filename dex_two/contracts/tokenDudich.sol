// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin2/contracts/token/ERC20/ERC20.sol";

contract DudichToken is ERC20 {
    constructor(uint256 initialSupply) ERC20("Dudich", "DDCH") {
        _mint(msg.sender, initialSupply);
    }
}
