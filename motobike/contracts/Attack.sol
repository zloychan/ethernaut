// SPDX-License-Identifier: MIT

pragma solidity <0.7.0;

contract BikeExy {
    function initialize() external {
        selfdestruct(payable(msg.sender));
    }
}
