const { time } = require( '@openzeppelin/test-helpers' );

var DosPunks1155 = artifacts.require( "DosPunks1155.sol" );

module.exports = function( deployer ) {
	const addresses = web3.eth.getAccounts();
	var res2 = deployer.deploy( DosPunks1155 );
}
