// make sure ganache is running
// to run: truffle exec token_interactions_development.js --network development

const web3          = require( 'web3' );
const DosPunks1155 = artifacts.require( 'DosPunks1155' );

module.exports = async function( callback ) {

	//const owner  = "0xC59B4c100c19530E3bd4c616CA0352793FaeFB88"; 
	//const other  = "0x447E9B80E31f5A91d5d15247aD33E90b94F00f77"; 
	//const owner  = "0x9cE079EfEAFF3D855Cc82DAC1a7510d5807f1B00"; 

	// dev 
	const owner = "0xF94c1EB34e8704Af51ba9ef43078008489d38dBA";
	const other = "0x2C3277dBe74c6FBf3f0Ad409713e3e70eee3E052";
	const burn  = "0x000000000000000000000000000000000000D3ad";

	let contract_address_1155 = '0x124FAd2784a1eaf3B7B419141335eadEA07619d7';

	let token = await DosPunks1155.at( contract_address_1155 );

	let token1 = "86183687183603793108320826266155603664391186218806717785568405633101373374465";
	let token2 = "86183687183603793108320826266155603664391186218806717785568405634200885002241";
	let token3 = "86183687183603793108320826266155603664391186218806717785568405635300396630017";

	console.log( "Get other (minter) balance token 1: should be 1" ); 
	let res01 = await token.balanceOf( owner, token1, { "from" : other } );
	console.log( res01 );
	console.log( "Get other (minter) balance token 2: should be 1" ); 
	let res02 = await token.balanceOf( owner, token1, { "from" : other } );
	console.log( res02 );
	console.log( "Get other (minter) balance token 3: should be 1" ); 
	let res03 = await token.balanceOf( owner, token1, { "from" : other } );
	console.log( res03 );

	console.log( "Get burn balance token 1: should be 0" ); 
	let res11 = await token.balanceOf( burn, token1, { "from" : other } );
	console.log( res11 );
	console.log( "Get burn balance token 2: should be 0" ); 
	let res12 = await token.balanceOf( burn, token1, { "from" : other } );
	console.log( res12 );
	console.log( "Get burn balance token 3: should be 0" ); 
	let res13 = await token.balanceOf( burn, token1, { "from" : other } );
	console.log( res13 );

	console.log( "END" ); 
}
