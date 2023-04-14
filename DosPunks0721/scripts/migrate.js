// make sure ganache is running
// to run: truffle exec token_interactions_development.js --network development

const web3          = require( 'web3' );
const DosPunks = artifacts.require( 'DosPunks' );

module.exports = async function( callback ) {

	//const owner  = "0xC59B4c100c19530E3bd4c616CA0352793FaeFB88"; 
	//const other  = "0x447E9B80E31f5A91d5d15247aD33E90b94F00f77"; 
	//const owner  = "0x9cE079EfEAFF3D855Cc82DAC1a7510d5807f1B00"; 

	// dev 
	const owner = "0xF94c1EB34e8704Af51ba9ef43078008489d38dBA";
	const other = "0x2C3277dBe74c6FBf3f0Ad409713e3e70eee3E052";
	const burn  = "0x000000000000000000000000000000000000D3ad";

	let contract_address_1155 = '0x124FAd2784a1eaf3B7B419141335eadEA07619d7';
	let contract_address_721 = '0xDca788af54AE0a5F72b03D5A58aCc151C59f62bB';

	let token = await DosPunks.at( contract_address_721 );

	let token1 = "86183687183603793108320826266155603664391186218806717785568405633101373374465";
	let token2 = "86183687183603793108320826266155603664391186218806717785568405634200885002241";
	let token3 = "86183687183603793108320826266155603664391186218806717785568405635300396630017";

	console.log( "set dos punks 1155 address" );
	let res0 = await token.setDosPunksAddress( contract_address_1155 );
	console.log( res0 );

	console.log( "migrate 1" ); 
	let res1 = await token.migrateToken( token1, { from : owner } );
	console.log( "migrate 2" ); 
	let res2 = await token.migrateToken( token2, { from : owner } );
	console.log( "migrate 3" ); 
	let res3 = await token.migrateToken( token3, { from : owner } );
	console.log( "END" ); 
}
