// SPDX-License-Identifier: MIT

//           .
//          .'.
//          |o|       -; to the moooooonACO !
//         .'o'.
//         |.-.|
//         '   '
//          ( )
//           )
//          ( )
//           (
//         _____
//     ,-:` \;',`'-, 
//   .'-;_,;  ':-;_,'.
//  /;   '/    ,  _`.-\
// | '`. (`     /` ` \`|
// |:.  `\`-.   \_   / |
// |     (   `,  .`\ ;'|
//  \     | .'     `-'/
//   `.   ;/        .'
//     `'-._____.-'`

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract PedestrainDonutSellerStock is ERC721 {

    enum Buyables { DONUT, CHOUCHOU, CHICHI, ICE_CREAM }
    address public owner; 

    constructor() ERC721("SellerInventory", "SIE") {
        owner = msg.sender;
        _mint(msg.sender, uint256(Buyables.DONUT));
        _mint(msg.sender, uint256(Buyables.CHOUCHOU));
        _mint(msg.sender, uint256(Buyables.CHICHI));
        _mint(msg.sender, uint256(Buyables.ICE_CREAM));
    }

    function buy() public payable {
        uint256 amount = msg.value;

        require(amount >= 500 wei, "Hola amigos, tu vas me le donner ton argent ?");
        amount -= 500 wei;
        _transfer(owner, msg.sender, uint256(Buyables.DONUT));

        require(amount >= 0.75 gwei, "Pas si pauvre... Mes chouchous te restent hors de portee !");
        amount -= 0.75 gwei;
        _transfer(owner, msg.sender, uint256(Buyables.CHOUCHOU));

        require(amount >= 1.5 ether, "1.5 ether, vous savez combien ca fait 1.5 milliards de milliards Larmina ?");
        amount -= 1.5 ether;
        _transfer(owner, msg.sender, uint256(Buyables.CHICHI));

        require(amount == 0, "Tu n'es pas capable de faire l'appoint ??? J'allais pourtant t'offrir de la glace");
        _approve(msg.sender, uint256(Buyables.ICE_CREAM));
    }
}
