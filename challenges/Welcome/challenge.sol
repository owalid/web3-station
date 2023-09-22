// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Welcome {
    bool public iWantFlag = false;

    function giveMeTheFlag() external {
        iWantFlag = true;
    }
}
