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
    bool private unlocked = false;
    bool private moneySent = false;

    constructor() payable {
      require(msg.value == 1 ether);
    }

    function isSolved() public view returns (bool) {
        return moneySent && unlocked;
    }

    function unlock(bytes16 _key) public {
        require(bytes16(uint128(uint256(keccak256(abi.encodePacked(uint256(uint160(address(tx.origin)))))) ^ 42) ^ uint128(0x6170743432)) == _key, "Invalid key");
        unlocked = true;
    }

    function transfer(address payable _toAddr) public {
        require(moneySent == false, "Money already sent");
        require(unlocked, "The offshore bank is locked");
        require(tx.origin != msg.sender, "Only the offshore bank can transfer funds");

        (bool sent, ) = _toAddr.call{value: 1 ether}("");
        moneySent = sent;
        require(sent, "Failed to send Ether");
    }
}