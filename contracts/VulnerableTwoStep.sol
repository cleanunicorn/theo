
contract VulnerableTwoStep {
    address payable public owner;
    bool public owner_reset = false;

    constructor() public payable {
        owner = msg.sender;
    }

    function() external payable {}

    function become_owner() public payable {
        require(msg.value == 1 ether);

        if (owner_reset == false) {
            owner_reset = true;
            owner = msg.sender;
        }
    }

    function steal() public payable {
        owner.transfer(address(this).balance);
    }
}