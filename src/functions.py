import subprocess
import json

def getBalance(wallet_addr):
    _, balance = getUTXOData(wallet_addr)
    return balance

def getUTXOData(wallet_addr):
    txin = utxo(wallet_addr)
    balance = 0
    alltxns = ""
    for tx in txin:
        alltxns += tx[0] + "#" + tx[1] + " --tx-in "
        balance += int(tx[2]) # lovelaces
    alltxns = alltxns[:-9]
    return alltxns, balance

def utxo(wallet_addr):
    """
    Returns a list of all avaiable tx hashes.
    """
    utxoArgs = [
        "cardano-cli",
        "query",
        "utxo",
        "--allegra-era",
        "--cardano-mode",
        "--mainnet",
        "--address",
        wallet_addr
    ]
    function = subprocess.check_output(utxoArgs)
    transactions = function.decode('utf-8').split('\n')[2:-1]
    txin = []
    for trxn in transactions:
        _temp = trxn.split(' ')
        txin.append(list(filter(lambda a: a != '', _temp)))
    return txin
