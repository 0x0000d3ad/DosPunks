# DOS Punks 721
DOS Punks 721 an ERC 721 contract to which tokens from the [Open Sea](https://opensea.io/) ERC 1155 contract for [DOS Punks](https://opensea.io/collection/dos-punks) by [Max Capacity](https://twitter.com/maxcapacity) are migrated.  This contract should be viewed for educational purposes only.  Use at your own risk.

# Prerequisites
1. NPM v6.14.8
2. Truffle v5.5.9
3. Solidity Compiler v.0.8.4 (to be specified in truffle-config.js)
4. Ganache v2.5.4

# Initial Steps
First, you must set up a project using truffle.  On the command line, type:

> truffle init DosPunks0721 

This will create a directory with a file structure containing (among other things):

1. "contracts" directory - this is where the code will live
2. truffle-config.js - config file specifying details for compilation and deployment

## Copy Contract Code
Replace the default "DosPunks0721.sol" in the "contracts" folder with the one in this repository.

## Token ID's
Note that the `getTokenId` function is crucial to the correct mapping between the Open Sea contract and the ERC 721 contract.  If there is an error, the NFT's will not align.  There were certain aspects to the DOS Punks Open Sea contract which required some bespoke implementation.  Therefore, if you try to recycle this code for an arbitrary contract, it will not work.  For more information on the mapping between the Open Sea ID and the token ID, read [this article](https://medium.com/coinmonks/opensea-tokenid-explained-f420401f5109) about the token ID and [this article](https://cyberdoggos.medium.com/migrating-from-opensea-cfe9aab47d3) about migrating from Open Sea.

## Edit Config
The truffle-config.js must be edit with the following:

1. Your infura link (if you want to deploy to mainnet/testnets)
2. Change the compiler version to "0.8.4"

## Create a .secret File
Create a file called '.secret' in the parent directory (same directory as truffle-config.js).  In this directory you will place the 12 word mnemonic for your development account.  You cannot deploy to the mainnet or testnet without this.  Do not upload the .secret file or check it in anywhere (this is your secret key).

# Compiling
In the parent directory, type:

> truffle compile

If you have done everything correctly you should see something like the following:

Compiling your contracts...

===========================

\> Compiling .\contracts\DosPunks0721.sol

\> Compiling .\contracts\Migrations.sol

\> Artifacts written to C:\Users\13212\OneDrive\Desktop\Solidity\DosPunks0721\build\contracts

\> Compiled successfully using:
\   - solc: 0.8.4+commit.c7e474f2.Emscripten.clang

# Testing
Before deploying, we recommend thoroughly testing the contract.  Truffle provides a test suite that can automate unit tests provided in the "test" directory.  Test cases are written in .js files.  You can have one or more test files in the test directory, which will all be executed by simply typing:

> truffle test

We recommend testing on the local testnet with Ganache, then deploying to one or more testnets e.g. Ropsten or Rinkeby, before deploying to mainnet.

# Deploying
Before deploying the code, we need to create a file named "2_deploy_contracts.js" in the "migrations" directory, which will specify the contract to the deployer.  Once you've done this, simply type:

> truffle deploy --network \<network\>
  
where \<network\> corresponds to a network specified in your truffle-config.js file.  For example "truffle deploy --network development" should deploy to your local Ganache instance.  "truffle deploy --network ropsten" will deploy to the Ropsten test network (assuming you have specified this properly in truffle-config.js).  To deploy to mainnet, use "truffle deploy --network mainnet".
