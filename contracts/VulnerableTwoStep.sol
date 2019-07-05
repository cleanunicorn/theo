
contract VulnerableTwoStep {
    address payable public owner;
    bool public claimed;

    constructor() public payable {
        owner = msg.sender;
    }

    function() external payable {}

    function become_owner() public payable {
        require(msg.value == 1 ether);

        if (address(this).balance == 1 ether) {
            owner = msg.sender;
        }
    }

    function steal() public payable {
        require(msg.value >= 1 ether);

        owner.transfer(address(this).balance);
    }
}