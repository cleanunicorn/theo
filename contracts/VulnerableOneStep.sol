
contract Vulnerable {
    address public owner;
    bool public claimed;

    constructor() public payable {
        owner = msg.sender;
    }

    function() external payable {}

    function retrieve() public payable {
        require(msg.value >= 1 ether);

        msg.sender.transfer(address(this).balance);
    }
}