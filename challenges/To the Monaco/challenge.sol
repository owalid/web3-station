// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract PedestrainDonutSellerStock is ERC721 {

    enum Buyables { DONUT, CHOUCHOU, CHICHI }
    address public owner; 

    constructor() ERC721("SellerInventory", "SIE") {
        owner = msg.sender;
        _mint(msg.sender, uint256(Buyables.DONUT));
        _mint(msg.sender, uint256(Buyables.CHOUCHOU));
        _mint(msg.sender, uint256(Buyables.CHICHI));
    }

    function buy() public payable {
        uint256 amount = msg.value;

        require(amount >= 500 wei, "Hola amigos, tu va me le donner ton argent ou quoi ?");
        amount -= 500 wei;
        _transfer(owner, msg.sender, uint256(Buyables.DONUT));

        require(amount >= 0.75 gwei, "Pas si pauvre... Mais mes chouchous te restent hors de portee");
        amount -= 0.75 gwei;
        _transfer(owner, msg.sender, uint256(Buyables.CHOUCHOU));

        require(amount >= 1.5 ether, "1.5 ether, vous savez combien ca fait 1.5 milliards de milliards Larmina");
        amount -= 1.5 ether;
        _transfer(owner, msg.sender, uint256(Buyables.CHICHI));

        require(amount == 0, "tu n'es pas capable de faire l'appoint ???");
    }
}