// SPDX-License-Identifier: MIT

//         _._._                       _._._
//        _|   |_                     _|   |_
//        | ... |_._._._._._._._._._._| ... |
//        | ||| |  o OFFSHORE BANK o  | ||| |
//        | """ |  """    """    """  | """ |
//   ())  |[-|-]| [-|-]  [-|-]  [-|-] |[-|-]|  ())
//  (())) |     |---------------------|     | (()))
// (())())| """ |  """    """    """  | """ |(())())
// (()))()|[-|-]|  :::   .-"-.   :::  |[-|-]|(()))()
// ()))(()|     | |~|~|  |_|_|  |~|~| |     |()))(()
//    ||  |_____|_|_|_|__|_|_|__|_|_|_|_____|  ||
// ~ ~^^ @@@@@@@@@@@@@@/=======\@@@@@@@@@@@@@@ ^^~ ~
//      ^~^~                                ~^~^


pragma solidity ^0.8.0;

contract OffShoreAccount {
    address public offshoreAddress;
    bytes16 public key;
    bool private unlocked = false;

    constructor() payable {
        offshoreAddress = msg.sender;
        key = bytes16(uint128(uint256(keccak256(abi.encodePacked(uint256(uint160(address(msg.sender)))))) ^ 42) ^ uint128(0x6170743432));
    }

    function unlock(bytes16 _key) public {
        require(key == _key, "Invalid key");
        unlocked = true;
    }

    function transfer(address payable _toAddr) public {
        require(unlocked, "The offshore bank is locked");
        require(tx.origin == address(this), "Only the offshore bank can transfer funds");

        (bool sent, ) = _toAddr.call{value: 1 ether}("");
        require(sent, "Failed to send Ether");
    }
}