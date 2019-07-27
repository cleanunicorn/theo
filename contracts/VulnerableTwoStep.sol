// pragma solidity ^0.5.0;

contract VulnerableTwoStep {
    address public player;
    address public owner;
    bool public claimed;

    constructor() public payable {
        owner = msg.sender;
    }

    function reset() public payable {
        require(owner == msg.sender);

        player = address(0);
        claimed = false;
    }

    function() external payable {}

    function claimOwnership() public payable {
        require(msg.value == 0.1 ether);

        if (claimed == false) {
            player = msg.sender;
            claimed = true;
        }
    }

    function retrieve() public {
        require(msg.sender == player);

        msg.sender.transfer(address(this).balance);

        player = address(0);
        claimed = false;
    }
}
