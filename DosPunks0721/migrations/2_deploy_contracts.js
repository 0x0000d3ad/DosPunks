const { time } = require( '@openzeppelin/test-helpers' );

var DosPunks = artifacts.require( "DosPunks.sol" );

module.exports = function( deployer ) {
	const addresses = web3.eth.getAccounts();
	var res2 = deployer.deploy( DosPunks );
}
