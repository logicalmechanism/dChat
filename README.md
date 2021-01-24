# dChat
An unrestricted and decentralized communication platform.
### Requirements
> Fully synced cardano-node and Ubuntu 20
> Use this guide

## Create a chat wallet
Inside the dChat directory is the new_addr.sh file. It will create a wallet with keys in the folder main_user. This wallet will allow the user to send messages on dChat. It will prompt the user to input the return address as well. This will allow the user to extract funds back to any wallet.

dChat provides a the wallet address via a qr code inside the application. The base address is also in the main_base.addr file inside the main_user folder.

> Each message costs the fee for the transaction, ~0.17 ADA, plus the amount for the data. The current estimate for a single character is about ~50 lovelaces.

In the terminal run:

bash new_addr.sh

> new_addr.sh will only create a single address so it will not overwrite hot keys for a wallet.

## Running dChat
sudo systemctl stop cnode
sudo systemctl start cnode

> Allow node to establish connections
>

source ./env

python gui.py