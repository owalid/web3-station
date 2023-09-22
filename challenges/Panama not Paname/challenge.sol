// SPDX-License-Identifier: MIT

//           _.====.._
//         ,:._       ~-_
//             `\        ~-_
//               | _  _  |  `.
//             ,/ /_)/ | |    ~-_
//    -..__..-''  \_ \_\ `_      ~~--..__...----.____..---...

pragma solidity ^0.8.0;

contract SurfSequence {

    enum Location { HOTEL, BEACH, LINEUP, RIDING_WAVE }

    Location public location;
    bool public tookWave;
    bytes29 private gettingToLineUpSequence;
    bytes31 private ridingTheWaveSequence;

    constructor(bytes29 _gettingToLineUpSequence, bytes31 _ridingTheWaveSequence) {
        location = Location.HOTEL;
        gettingToLineUpSequence = _gettingToLineUpSequence;
        ridingTheWaveSequence = _ridingTheWaveSequence;
    }

    function goToBeach() external {
        location = Location.BEACH;
    }

    function goToLineUp(bytes29 armRotationSequence) public {
        require(location == Location.BEACH);
        require(armRotationSequence == gettingToLineUpSequence);
        location = Location.LINEUP;
    }

    function takeWave(bytes31 armRotationSequence) external {
        require(location == Location.LINEUP);
        require(armRotationSequence == ridingTheWaveSequence);
        location = Location.RIDING_WAVE;
        tookWave = true;
    }
}

// ps: pour ce challenge tu aura besoin d'utiliser d'autres logiciels que remix, tu peux pour cela utiliser web3py, exemple d'utilisation:
// $ pip3 install web3
// >>> from web3 import Web3
// >>> w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
// >>> w3.eth.get_code('0x6B7B103B0E86705358f403bA220461696569Ea76')
