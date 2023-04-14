#!/usr/bin/python

###########################################################################
#
# name          : dos_punks_migration_test.py
#
# purpose       : test dos punks migration
#
# usage         : python dos_punks_migration_test.py <args>
#
# description   :
#
###########################################################################

import datetime
import json
import logging
import os
import pandas
import sys

from eth_utils import keccak, to_checksum_address
from web3 import HTTPProvider, Web3

dos_punks_1155 = to_checksum_address( "0x124FAd2784a1eaf3B7B419141335eadEA07619d7" )
dos_punks_0721 = to_checksum_address( "0xDca788af54AE0a5F72b03D5A58aCc151C59f62bB" )

wallet_address = to_checksum_address( "0x2C3277dBe74c6FBf3f0Ad409713e3e70eee3E052" )

abi_file_dos_punks_1155 = "../DosPunks1155/build/contracts/DosPunks1155.json" 
abi_file_dos_punks_0721 = "build/contracts/DosPunks.json" 

id1 = 86183687183603793108320826266155603664391186218806717785568405633101373374465
id2 = 86183687183603793108320826266155603664391186218806717785568405634200885002241
id3 = 86183687183603793108320826266155603664391186218806717785568405635300396630017

logging.basicConfig( 
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler( "logs_%s.log" % datetime.datetime.now().strftime( "%Y%m%d%H%M%S" ) ),
        logging.StreamHandler( sys.stdout )
    ]
)


def get_abi() :
    abi_1155 = None
    abi_0721 = None
    data = None

    with open( abi_file_dos_punks_1155, 'r' ) as f :
        data = json.load( f )
    abi_1155 = data[ "abi" ]

    with open( abi_file_dos_punks_0721, 'r' ) as f :
        data = json.load( f )
    abi_0721 = data[ "abi" ]

    return abi_1155, abi_0721


def set_up_wallet( mnemonic_file=".secret" ) :
    web3_inst = Web3()
    web3_inst.eth.account.enable_unaudited_hdwallet_features()
    string = None
    with open( mnemonic_file, 'r' ) as f :
        string = f.read().strip()
    account = web3_inst.eth.account.from_mnemonic( string )
    return account


def send_eth( address_to=wallet_address ) :
    logging.info( f"Sending ETH to: {address_to}" )

    from_account = set_up_wallet( mnemonic_file=".devsecret" )

    web3_inst = Web3()

    # get eth balance before transaction
    eth_balance = web3_inst.eth.getBalance( address_to )
    logging.info( f"Before ETH Balance: {eth_balance}" )

    #get the nonce.  Prevents one from sending the transaction twice
    nonce = web3_inst.eth.getTransactionCount( from_account.address )

    #build a transaction in a dictionary
    tx = {
        'nonce': nonce,
        'to': address_to,
        'value': web3_inst.toWei(.5, 'ether'),
        'gas': 2000000,
        'gasPrice': web3_inst.toWei('50', 'gwei')
    }

    #sign the transaction
    signed_tx = web3_inst.eth.account.sign_transaction( tx, from_account.key )

    #send transaction
    tx_hash = web3_inst.eth.sendRawTransaction( signed_tx.rawTransaction )

    #get transaction hash
    logging.info( f"Transaction hash: {web3_inst.toHex(tx_hash)}" )

    # get eth balance after transaction
    eth_balance = web3_inst.eth.getBalance( address_to )
    logging.info( f"After ETH Balance: {eth_balance}" )


if __name__ == "__main__" : 
    import optparse
    parser = optparse.OptionParser()
    parser.add_option( '-A', '--address',     dest='address',     action='store_true', help='Get web3 address' )
    parser.add_option( '-e', '--eth',         dest='eth',         action='store_true', help='Send ETH to wallet' )
    parser.add_option( '-b', '--balance',     dest='balance',     action='store_true', help='Check token balance' )
    parser.add_option( '-m', '--migration',   dest='migration',   action='store_true', help='Do full migration' )
    parser.add_option( '-B', '--batch',       dest='batch',       action='store_true', help='Migrate batch' )
    parser.add_option( '-a', '--approved',    dest='approved',    action='store_true', help='Is approved for all' )
    parser.add_option( '-s', '--set',         dest='set',         action='store_true', help='Set approved for all' )
    ( options, args ) = parser.parse_args()

    abi_1155, abi_0721 = get_abi()

    web3_inst = Web3( Web3.HTTPProvider( "http://127.0.0.1:8545" ) )
    contract_1155 = web3_inst.eth.contract( address=dos_punks_1155, abi=json.dumps( abi_1155 ) )
    contract_0721 = web3_inst.eth.contract( address=dos_punks_0721, abi=json.dumps( abi_0721 ) )

    if options.address :
        account = set_up_wallet()
        logging.info( f"Account address: {account.address}" )

    if options.balance :
        balance_1155_1 = contract_1155.functions.balanceOf( wallet_address, id1 ).call()
        balance_1155_2 = contract_1155.functions.balanceOf( wallet_address, id2 ).call()
        balance_1155_3 = contract_1155.functions.balanceOf( wallet_address, id3 ).call()
        balance_0721   = contract_0721.functions.walletOfOwner( wallet_address ).call()
        logging.info( f"Balance 1155 token 1 {balance_1155_1}" )
        logging.info( f"Balance 1155 token 2 {balance_1155_2}" )
        logging.info( f"Balance 1155 token 3 {balance_1155_3}" )
        logging.info( f"Balance 0721 token   {len(balance_0721)}" )

    if options.eth :
        send_eth( address_to=account.address )

    if options.approved :
        res = contract_1155.functions.isApprovedForAll( wallet_address, dos_punks_0721 ).call()
        logging.info( f"Is approved for all: '%s'" % str( res ) )

    if options.set :
        # get wallet 
        account = set_up_wallet()
        logging.info( f"Account address: {account.address}" )

        # call isApprovedForAll
        res = contract_1155.functions.isApprovedForAll( wallet_address, dos_punks_0721 ).call()
        logging.info( f"Before: Is approved for all: '%s'" % str( res ) )

        # set up transaction
        nonce = web3_inst.eth.getTransactionCount( account.address )
        txn_args = { 
            "from" : wallet_address, 
            "nonce" : nonce, 
            'gas': 100000, 
            'gasPrice': web3_inst.toWei('50', 'gwei') 
        }
        tx = contract_1155.functions.setApprovalForAll( dos_punks_0721, True ).buildTransaction( txn_args )

        # sign transaction
        signed_txn = web3_inst.eth.account.signTransaction( tx, private_key=account.key )

        # send transaction
        web3_inst.eth.sendRawTransaction( signed_txn.rawTransaction )
        logging.info( f"Approval set..." )

        # call isApprovedForAll
        res = contract_1155.functions.isApprovedForAll( wallet_address, dos_punks_0721 ).call()
        logging.info( f"After: Is approved for all: '%s'" % str( res ) )

    if options.migration :

        # get wallet that holds the dos punks 1155
        account = set_up_wallet()
        logging.info( f"Account address: {account.address}" )

        # get balances before the transaction
        balance_1155_1 = contract_1155.functions.balanceOf( account.address, id1 ).call()
        balance_1155_2 = contract_1155.functions.balanceOf( account.address, id2 ).call()
        balance_1155_3 = contract_1155.functions.balanceOf( account.address, id3 ).call()
        balance_0721   = contract_0721.functions.walletOfOwner( account.address ).call()
        logging.info( f"Before: Balance 1155 token 1 {balance_1155_1}" )
        logging.info( f"Before: Balance 1155 token 2 {balance_1155_2}" )
        logging.info( f"Before: Balance 1155 token 3 {balance_1155_3}" )
        logging.info( f"Before: Balance 0721 token   {len(balance_0721)}" )

        # determine if approved
        res = contract_1155.functions.isApprovedForAll( account.address, dos_punks_0721 ).call()
        logging.info( f"Is approved for all: '%s'" % str( res ) )

        # if not approval, send approval
        if not res :
            logging.info( "Not approved.  Setting approval" )

            # set up transaction
            nonce = web3_inst.eth.getTransactionCount( account.address )
            txn_args = { 
                "from" : account.address, 
                "nonce" : nonce, 
                'gas': 100000, 
                'gasPrice': web3_inst.toWei('50', 'gwei') 
            }
            tx = contract_1155.functions.setApprovalForAll( dos_punks_0721, True ).buildTransaction( txn_args )

            # sign transaction
            signed_txn = web3_inst.eth.account.signTransaction( tx, private_key=account.key )

            # send transaction
            web3_inst.eth.sendRawTransaction( signed_txn.rawTransaction )
            logging.info( f"Approval set..." )

            # call isApprovedForAll
            res = contract_1155.functions.isApprovedForAll( wallet_address, dos_punks_0721 ).call()
            logging.info( f"After: Is approved for all: '%s'" % str( res ) )

        logging.info( f"Migrating token 1..." )

        # set up transaction
        nonce = web3_inst.eth.getTransactionCount( account.address )
        txn_args = { 
            "from" : account.address, 
            "nonce" : nonce, 
            'gas': 100000, 
            'gasPrice': web3_inst.toWei('50', 'gwei') 
        }
        tx = contract_1155.functions.migrateToken( id1 ).buildTransaction( txn_args )

        # sign transaction
        signed_txn = web3_inst.eth.account.signTransaction( tx, private_key=account.key )

        # send transaction
        web3_inst.eth.sendRawTransaction( signed_txn.rawTransaction )
        logging.info( f"Approval set..." )

        # get balances after the transaction 
        balance_1155_1 = contract_1155.functions.balanceOf( account.address, id1 ).call()
        balance_1155_2 = contract_1155.functions.balanceOf( account.address, id2 ).call()
        balance_1155_3 = contract_1155.functions.balanceOf( account.address, id3 ).call()
        balance_0721   = contract_0721.functions.walletOfOwner( account.address ).call()
        logging.info( f"After: Balance 1155 token 1 {balance_1155_1}" )
        logging.info( f"After: Balance 1155 token 2 {balance_1155_2}" )
        logging.info( f"After: Balance 1155 token 3 {balance_1155_3}" )
        logging.info( f"After: Balance 0721 token   {len(balance_0721)}" )

    if options.batch :

        # get wallet that holds the dos punks 1155
        account = set_up_wallet()
        logging.info( f"Account address: {account.address}" )

        # get balances before the transaction
        balance_1155_1 = contract_1155.functions.balanceOf( account.address, id1 ).call()
        balance_1155_2 = contract_1155.functions.balanceOf( account.address, id2 ).call()
        balance_1155_3 = contract_1155.functions.balanceOf( account.address, id3 ).call()
        balance_0721   = contract_0721.functions.walletOfOwner( account.address ).call()
        logging.info( f"Before: Balance 1155 token 1 {balance_1155_1}" )
        logging.info( f"Before: Balance 1155 token 2 {balance_1155_2}" )
        logging.info( f"Before: Balance 1155 token 3 {balance_1155_3}" )
        logging.info( f"Before: Balance 0721 token   {len(balance_0721)}" )

        # determine if approved
        res = contract_1155.functions.isApprovedForAll( account.address, dos_punks_0721 ).call()
        logging.info( f"Is approved for all: '%s'" % str( res ) )

        # if not approval, send approval
        if not res :
            logging.info( "Not approved.  Setting approval" )

            # set up transaction
            nonce = web3_inst.eth.getTransactionCount( account.address )
            txn_args = { 
                "from" : account.address, 
                "nonce" : nonce, 
                'gas': 100000, 
                'gasPrice': web3_inst.toWei('50', 'gwei') 
            }
            tx = contract_1155.functions.setApprovalForAll( dos_punks_0721, True ).buildTransaction( txn_args )

            # sign transaction
            signed_txn = web3_inst.eth.account.signTransaction( tx, private_key=account.key )

            # send transaction
            web3_inst.eth.sendRawTransaction( signed_txn.rawTransaction )
            logging.info( f"Approval set..." )

            # call isApprovedForAll
            res = contract_1155.functions.isApprovedForAll( wallet_address, dos_punks_0721 ).call()
            logging.info( f"After: Is approved for all: '%s'" % str( res ) )

        logging.info( f"Migrating token 1..." )

        # set up transaction
        nonce = web3_inst.eth.getTransactionCount( account.address )
        txn_args = { 
            "from" : account.address, 
            "nonce" : nonce, 
            'gas': 100000, 
            'gasPrice': web3_inst.toWei('50', 'gwei') 
        }
        tx = contract_1155.functions.migrateBatch( [ id1, id2 ] ).buildTransaction( txn_args )

        # sign transaction
        signed_txn = web3_inst.eth.account.signTransaction( tx, private_key=account.key )

        # send transaction
        web3_inst.eth.sendRawTransaction( signed_txn.rawTransaction )
        logging.info( f"Approval set..." )

        # get balances after the transaction 
        balance_1155_1 = contract_1155.functions.balanceOf( account.address, id1 ).call()
        balance_1155_2 = contract_1155.functions.balanceOf( account.address, id2 ).call()
        balance_1155_3 = contract_1155.functions.balanceOf( account.address, id3 ).call()
        balance_0721   = contract_0721.functions.walletOfOwner( account.address ).call()
        logging.info( f"After: Balance 1155 token 1 {balance_1155_1}" )
        logging.info( f"After: Balance 1155 token 2 {balance_1155_2}" )
        logging.info( f"After: Balance 1155 token 3 {balance_1155_3}" )
        logging.info( f"After: Balance 0721 token   {len(balance_0721)}" )
