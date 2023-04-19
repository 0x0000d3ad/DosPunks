# Introduction 
 This repo contains the DOS punks migration smart contract and supporting Python Web3 implementation to test the migration code.

# Core Contents
 The main functionality of this repo is the following
 - `DosPunks0721` - ERC 721 contract *to* which we will migrate.
 - `DosPunks1155` - ERC 1155 contract *from* which we will migrate.  This is a *test contract only*.  On the main net, this will be replaced by the Open Sea contract.
 - `dos_punks_migration_test.py` - Contains python code to demonstrate migration functionality.

# Private Key Disclaimer
 No mention of private keys would be complete without an obligatory disclaimer on the safety of your [mnemonic phrase](https://docs.safepal.io/safepal-hardware-wallet/security-features/software-security/mnemonic-phrase).  For this project, you will need *two* addresses, one for the deployer, one for the NFT owner.  They will be stored in the following files:

 1. `.devsecret` - Deployer mnemonic
 2. `.secret` - NFT recipient mnemonic

 Note that it is *possible* to use the same wallet, but the deployer wallet does have some priviledges (see the [Solidity modifier](https://www.freecodecamp.org/news/what-are-solidity-modifiers/) `onlyOwner`).  Thus it is better to test any public-facing functionality on a *separate* wallet.

 It is *highly* recommended that you do not use an existing wallet for dev purposes.  In other words, your dev wallets should be used for dev purposes *only* and do not contain any real assets other than perhaps test net Ethereum.

# Installation
 Dependencies include:

 1. eth_utils - for creating checksummed wallet addresses
 2. web3 - for contract interaction 

 These can be installed as follows:

 `pip -r requirements.txt`

# Running Test Migration
 There are three primary steps required to run the migration example:

 1. Start Ganache 
 2. Deploy the DosPunks1155 contract.
 3. Deploy the Dospunks0721 contract.
 4. Run functionality in dos_punks_migration_test.py

## Start Ganache
 Here, we are using ganache-cli, the command line tool, but you can get the same results with the GUI tool.  To start it, simply run on the command line:

 `ganache-cli`

 NOTE: ganache-cli will use a randomly generated private key every time it is started.  It is highly recommended that you use a consistent private key for dev operations, as this will minimize updating [.devsecret](https://www.oreilly.com/library/view/mastering-blockchain-programming/9781839218262/fd4b11b7-274c-4cd7-b15e-a18c1d17da3b.xhtml) later.  To use the dev mnemonic specified in `.devsecret`:

 `ganache-cli -m path/to/.devsecret`

## Deploy DosPunks1155
 We will need to deploy the ERC 1155 contract.  This mimics the OpenSea contract, but is *not* the real thing.  It is simply a 'dummy' contract to test operations.

 To deploy the ERC 1155 contract, cd into the DosPunks1155 directory, and run:

 `truffle deploy --network development`

 Observe that deploying this contract will mint tokens to the specified wallet address when the constructor is called.  Change this wallet address to a wallet for which you have the private key.  Put the mnemonic to this private key in a space-delimited file called `.secret`.  Change the `mint_to_address` wallet address at line [1085](https://github.com/0x0000d3ad/DosPunks/blob/ef5defc3c6555250e2963cec251120a8907aac01/DosPunks1155/contracts/DosPunks1155.sol#L1085):

 `address public mint_to_address = <your address>;`

 NOTE: Preconditions exist and are necessary for deployment, including creating a `truffle-config.js` file.  Read more in the [DosPunks1155 README](./DosPunks1155/README.md).

## Deploy DosPunks0721
 Next, we must deploy the ERC 721 contract.  This is the contract *to which* we are migrating.

 To deploy the ERC 721 contract, cd into the DosPunks0721 directory, and run:

 `truffle deploy --network development`

 NOTE: As before, preconditions exist and are necessary for deployment, including creating a `truffle-config.js` file.  Read more in the [DosPunks0721 README](./DosPunks0721/README.md).

## Run the Python Code
 The migration functionality is facilitated by the Python script: `dos_punks_migration_test.py`.  This will set up accounts, read balances, set and check approvals, and will perform the actual migration.  This is just a demonstration of functionality for demo and testing purposes.

### Prerequisites
 Make sure you create files for the mnemonics of your test accounts in the root directory:

 1. `.devsecret` - Mnemonic to the account that deployed the contract on the testnet. 
 2. `.secret` - Mnemonic to the account to which the test 1155 tokens will be transferred.  Make sure you have specified the wallet address of this account in [DosPunks1155.sol](./DosPunks1155/contracts/DosPunks1155.sol).

### Step 1 - Fund Account
 First, you need to send ETH from the development (.devsecret) testnet to the account (.secret) that the 1155 tokens were transferred.  To do this, run the python script with the corresponding arguments:

 `python dos_punks_migration_test.py -A -e`

### Step 2 - Set Approved
 Next, you will need to call the setApprovedForAll function such that the ERC 721 contract has the permission to burn tokens from the 1155 contract.

 `python dos_punks_migration_test.py -s`

 NOTE: if you want to check whether this has been set already, simply run:

 `python dos_punks_migration_test.py -a`

### Step 3 - Migrate Tokens
 Now for the meat of the operation: migrating tokens.  This will burn tokens from our originating ERC 1155 contract and mint the respective token on the ERC 721 contract.

 `python dos_punks_migration_test.py -m`


 NOTE: the balance of both the ERC 1155 and ERC 721 tokens will be displayed before and after the migration transaction, so that you can see that the ERC 1155 tokens were indeed burned, and the ERC 721 tokens were minted.  However, if you want to check this balance at any time, run:

 `python dos_punks_migration_test.py -b`

# More on Migrations
 Note that the `getTokenId` function in the [ERC 721 contract](./DosPunks0721/contracts/ERC0721.sol) is crucial to the correct mapping between the Open Sea contract and the ERC 721 contract.  If there is an error in this mapping, the NFT's will not align.  There were certain aspects to the DOS Punks Open Sea contract which required some bespoke implementation.  Therefore, if you try to recycle this code for an arbitrary contract, it will not work.  For more information on the mapping between the Open Sea ID and the token ID, read [this article](https://medium.com/coinmonks/opensea-tokenid-explained-f420401f5109) about the token ID and [this article](https://cyberdoggos.medium.com/migrating-from-opensea-cfe9aab47d3) about migrating from Open Sea.
