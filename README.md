# dChat
An unrestricted and decentralized communication platform.
### Requirements
> Fully synced cardano-node
> dChat
> Ubuntu 20

## Create a chat wallet
Inside the dChat directory is the new_addr.sh file. It will create a wallet with keys in the folder main_user. This wallet will allow the user to send messages on dChat.

dChat provides a qr code inside the application. The base address is also in the main_base.addr file inside the main_user folder.

> Each message costs the fee for the transaction, ~0.2 ADA
>
In the terminal run:

bash new_addr.sh

## Running dChat
sudo systemctl stop cnode
sudo systemctl start cnode

> Allow node to establish connections
>

source ./env
python gui.py