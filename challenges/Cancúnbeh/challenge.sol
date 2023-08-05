// SPDX-License-Identifier: MIT

//  ____
// |    |          _____
// |    |      O  // / \\
// |   ·|     /|\   /
// |____|     / \  / o o

pragma solidity ^0.8.0;

contract Door {

    uint256 private doorCode = 123456;
    bool public locked = true;

    function unlock(uint256 passwordTry) external {
        require(doorCode == passwordTry, "try again");
        locked = false;
    }
}
