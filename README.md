# dChat
An unrestricted and decentralized communication platform.

### Requirements
> Fully synced cardano-node, python, and Ubuntu 20.

## Create a chat wallet
Pull the dchat git into the $CNODE_HOME folder.

>git clone https://github.com/logicalmechanism/dChat

Inside the dChat directory is the new_addr.sh file. Run this file with this command:

>bash ${CNODE_HOME}/dChat/new_addr.sh

This will create a wallet with payment/stake keys in the folder called main_user. This wallet will allow the user to send messages on dChat. 

It will also prompt the user to input the return wallet address as well. This will allow the user to extract funds. The wallet address is stored in the return_user folder inside the return_base.addr file.

> new_addr.sh will only create a single address so it will not overwrite hot keys for a wallet.

dChat provides a the wallet address via a qr code inside the application. The base address is also in the main_base.addr file inside the main_user folder.

> Each message costs the fee for the transaction, ~0.17 ADA, plus the amount for the data. The current estimate for a single character is about ~50 lovelaces.



## Running dChat
> Assuming a fully synced passive relay node

sudo systemctl stop cnode

sudo systemctl start cnode

> Allow node to establish connections

source ${CNODE_HOME}/scripts/env

python ${CNODE_HOME}/dChat/gui.py