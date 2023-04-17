# Introduction 
 This repo contains the DOS punks migration smart contract and supporting Python Web3 implementation to test the migration code.

# Core Contents
 The main functionality of this repo is the following
 - `DosPunks0721` - ERC 721 contract *to* which we will migrate.
 - `DosPunks1155` - ERC 1155 contract *from* which we will migrate.  This is a *test contract only*.  On the main net, this will be replaced by the Open Sea contract.
 - `dos_punks_migration_test.py` - Contains python code to demonstrate migration functionality.

# Installation
 Dependencies include:

 1. eth_utils - for creating checksummed wallet addresses
 2. web3 - for contract interaction 

 These can be installed as follows:

 `pip -r requirements.txt`

# Running Test Migration

 There are three primary steps required to run the migration example:

 1. Deploy the DosPunks1155 contract.
 2. Deploy the Dospunks0721 contract.
 3. Run functionality in dos_punks_migration_test.py

## Deploy DosPunks1155
## Deploy DosPunks0721
## Run the Python Code
