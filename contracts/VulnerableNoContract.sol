contract VulnerableTwoStep {
    address payable public owner;
    bool public owner_reset = false;
    uint256 public owner_set_block = 0;

    constructor() public payable {
        owner = msg.sender;
    }

    function() external payable {}

    function become_owner() public payable {
        require(msg.value == 1 ether);
        require(!isContract(msg.sender));

        if (owner_reset == false) {
            owner_reset = true;
            owner_set_block = block.number;
            owner = msg.sender;
        }
    }

    function retrieve() public payable {
        require(block.number > owner_set_block);
        require(owner_set_block > 0);
        require(!isContract(owner));

        owner.transfer(address(this).balance);
    }

    function isContract(address _addr)
        private
        view
        returns (bool)
    {
        uint32 size;
        assembly {
            size := extcodesize(_addr)
        }
        return (size > 0);
    }
}