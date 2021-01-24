# dChat
An unrestricted and decentralized communication platform. Each message is sent as part of the meta data for a transaction. Expect messages to arrive on the ledger about 20 seconds after submission.

## This will always be an open source project. 
## Chat wallets are always controlled by the user.

### Requirements
> Fully synced cardano-node, python, bash, and Ubuntu 20.

## Create a chat wallet
Pull the dchat git into the ${CNODE_HOME} folder.

>git clone https://github.com/logicalmechanism/dChat

Inside the dChat directory is the new_addr.sh file. Run this file with this command:

>bash ${CNODE_HOME}/dChat/new_addr.sh

This will create a wallet with payment/stake keys inside the dChat directory in the folder called main_user. This wallet will allow the user to send messages on dChat. 

It will also prompt the user to input the return wallet address as well. This will allow the user to extract funds. The return wallet address is storeed inside the dChat directory in the return_user folder inside the return_base.addr file.

> new_addr.sh will only create a single address so it will not overwrite hot keys for a wallet. If you are worried then run new_addr.sh and copy the keys onto a cold store device.

dChat provides the chat wallet address via a qr code and as a copy friendly input inside the application. The same address is in the main_base.addr file inside the main_user folder.

> Each message costs the fee for the transaction, ~0.17 ADA, plus the amount for the data. The current estimate for a single character is about ~50 lovelaces.



## Running dChat
> Assuming a fully synced passive relay node

sudo systemctl stop cnode

sudo systemctl start cnode

> Allow node to establish connections

source ${CNODE_HOME}/scripts/env

python ${CNODE_HOME}/dChat/gui.py