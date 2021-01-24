#!/bin/bash
NAME="main"
### Check if a directory does not exist ###
cd $CNODE_HOME'/dchat'
if [ -d "/${NAME}_user" ] 
then
  mkdir -p $NAME"_user"
  mkdir -p "return_user"
  read -p "Enter Return Wallet Address" RETURN_WALLET
  echo $RETURN_WALLET >> "return_user/return_base.addr"
  echo "Return wallet address saved to return_base.addr"
else
  exit 1
fi
cd "${NAME}_user"
# echo "Generating Payment/Enterprise address"
cardano-cli address key-gen --verification-key-file ${NAME}_payment.vkey --signing-key-file ${NAME}_payment.skey
cardano-cli stake-address key-gen --verification-key-file ${NAME}_stake.vkey --signing-key-file ${NAME}_stake.skey
# echo "Payment/Enterprise address:"
cardano-cli address build --payment-verification-key-file ${NAME}_payment.vkey --mainnet | tee ${NAME}_payment.addr
# echo "Base address:"
cardano-cli address build --payment-verification-key-file ${NAME}_payment.vkey --stake-verification-key-file ${NAME}_stake.vkey --mainnet | tee ${NAME}_base.addr
# echo "$Reward address:"
cardano-cli stake-address build --stake-verification-key-file ${NAME}_stake.vkey --mainnet | tee ${NAME}_reward.addr
qr $(cat ${CNODE_HOME}"/addr/"${NAME}"_user/"${NAME}_base.addr) > ${NAME}"_qrcode.png"
