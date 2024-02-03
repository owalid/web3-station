// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.24;

contract Proposal {

    enum VOTE_STATUS {
        NOT_VOTED,
        VOTED_FOR,
        VOTED_AGAINST
    }

    bytes32 public reason;
    address public initiator;
    address public receiver;
    uint public positiveVoteCount;
    uint public negativeVoteCount;
    mapping(address => VOTE_STATUS) public votes;
    address public immutable owner;

    constructor(bytes32 _reason, address _receiver) {
        reason = _reason;
        initiator = msg.sender;
        receiver = _receiver;
        positiveVoteCount = 1;
        votes[msg.sender] = VOTE_STATUS.VOTED_FOR;
        owner = tx.origin;
    }

    modifier onlyOwner() {
        require(tx.origin == owner, "You are not the initiator of the proposal");
        _;
    }

    function invalidate_vote(address _a) public onlyOwner {
        if (votes[_a] == VOTE_STATUS.VOTED_FOR) {
            positiveVoteCount -= 1;
        }
        else if (votes[_a] == VOTE_STATUS.VOTED_AGAINST) {
            negativeVoteCount -= 1;
        }
        votes[_a] = VOTE_STATUS.NOT_VOTED;
    }

    function vote(address voter, bool status) public onlyOwner {
        require(votes[voter] == VOTE_STATUS.NOT_VOTED);
        if (status == true) {
            votes[voter] = VOTE_STATUS.VOTED_FOR;
            positiveVoteCount += 1;
        }
        else {
            votes[voter] = VOTE_STATUS.VOTED_AGAINST;
            negativeVoteCount += 1;
        }
    }

}

contract Elections {

    mapping(address => bool) public allowed_voters;
    mapping(address => mapping(uint => uint256)) public address_to_points;
    uint public month_index;
    uint public voter_amount;
    bool public be_voter;
    Proposal[] public proposals;

    constructor(address[] memory _allowed_voters, uint256[] memory _current_points) {
        for (uint i = 0; i < _allowed_voters.length; i++) {
            allowed_voters[_allowed_voters[i]] = true;
            address_to_points[_allowed_voters[i]][0] = _current_points[i];
            voter_amount += 1;
        }
    }

    modifier onlyVoter {
        require(allowed_voters[msg.sender] == true, "You are not a voter.");
        _;
    }

    function becomeVoter() public {
        require(be_voter == false);
        allowed_voters[msg.sender] = true;
        voter_amount += 1;
        be_voter = true;
    }

    function addPoint(address a) private {
        address_to_points[a][month_index] += 1;
    }

    function isSelfProposal(address _proposal) public view returns (bool, uint256) {
        for (uint i = 0; i < proposals.length; i++) {
            if (proposals[i] == Proposal(_proposal)) {
                return (true, i);
            }
        }
        return (false, 0);
    }

    function invalidate_votes(address _a) private {
        for (uint i = 0; i < proposals.length; i++) {
            proposals[i].invalidate_vote(_a);
        }
    }

    function vote(address _proposal, bool status) public onlyVoter {
        Proposal proposal = Proposal(_proposal);

        proposal.vote(msg.sender, status);

        if (proposal.positiveVoteCount() > voter_amount / 2) {
            if (proposal.reason() == "ADD") {
                allowed_voters[proposal.receiver()] = true;
                voter_amount += 1;
            }
            else if (proposal.reason() == "REMOVE") {
                allowed_voters[proposal.receiver()] = false;
                voter_amount -= 1;
                invalidate_votes(proposal.receiver());
            }
            else if (proposal.reason() == "ENDMONTH") {
                endMonth();
            }
            else {
                addPoint(proposal.receiver());
            }
        }
    }

    function createProposal(address receiver, bytes32 reason) public onlyVoter returns (address) {
        Proposal proposal = new Proposal(reason, receiver);
        proposals.push(proposal);
        return address(proposal);
    }

    function endMonth() private {
        month_index += 1;
    }

    function isVoter(address _a) public view returns (bool) {
        return allowed_voters[_a];
    }

    function getTotalPoints(address _a) public view returns (uint256) {
        uint256 counter = 0;
        
        for (uint i = 0; i <= month_index; i++) {
            counter += getPointsByMonth(_a, i);
        }
        return counter;
    }

    function getPointsByMonth(address _a, uint _m) public view returns (uint256) {
        return address_to_points[_a][_m];
    }

    function getPoints(address _a) public view returns (uint256) {
        return address_to_points[_a][month_index];
    }

}
