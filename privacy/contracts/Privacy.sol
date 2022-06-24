// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Privacy {
    // slot 0
    bool public locked = true;
    // slot 1
    uint256 public ID = block.timestamp;
    //slot 2
    uint8 private flattening = 10;
    // slot 2
    uint8 private denomination = 255;
    // slot 2
    uint16 private awkwardness = uint16(block.timestamp);
    // slot [3, 4, 5]
    bytes32[3] private data;
    bytes32 public test;

    constructor(bytes32[3] memory _data) public {
        data = _data;
        test = data[0];
    }

    function unlock(bytes16 _key) public {
        require(_key == bytes16(data[2]));
        locked = false;
    }

    /*
    A bunch of super advanced solidity algorithms...

      ,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`
      .,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,
      *.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^         ,---/V\
      `*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.    ~|__(o.o)
      ^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'  UU  UU
  */
}
