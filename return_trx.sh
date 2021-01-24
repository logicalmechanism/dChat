#!/bin/bash
set -e

# args
SENDER="main"
AMOUNT=1
RECEIVER="return"
# Convert ada into lovelaces
num=1000000
AMOUNT=$(echo "${num}*${AMOUNT}" | bc)
AMOUNT=${AMOUNT%.*}
#
BASE="${CNODE_HOME}/dchat/"
SENDER_FOLDER="${BASE}${SENDER}_user/"
RECEIVER_FOLDER="${BASE}${RECEIVER}_user/"
SENDER_ADDR="${SENDER_FOLDER}${SENDER}_base.addr"
RECEIVER_ADDR="${RECEIVER_FOLDER}${RECEIVER}_base.addr"
TMP_FOLDER="${SENDER_FOLDER}/TMP/"

# create temporary directory if missing
mkdir -p "${TMP_FOLDER}" # Create if missing
# start with a clean slate
rm -f "${TMP_FOLDER}"/*
# move to tmp folder
cd ${TMP_FOLDER}

# protocol
cardano-cli query protocol-parameters \
--allegra-era \
--mainnet \
--out-file protocol.json

# get utxo
cardano-cli query utxo \
--allegra-era \
--cardano-mode \
--mainnet \
--address $(cat ${SENDER_ADDR}) \
--out-file utxo.json

# # transaction variables
TXNS=$(jq length utxo.json)
alltxin=""
TXIN=$(jq -r --arg alltxin "" 'keys[] | . + $alltxin + " --tx-in"' utxo.json)
HEXTXIN=${TXIN::-8}
BALANCE=$(jq .[].amount utxo.json | awk '{sum=sum+$0} END{print sum}' )

# Next tip before no transaction
cardano-cli query tip --mainnet --out-file tip.json
TIP=$(jq .slotNo tip.json)
DELTA=200000
FINALTIP=$(( $DELTA + $TIP ))

# echo "Building Draft Transaction"
cardano-cli transaction build-raw \
--tx-in $HEXTXIN \
--tx-out $(cat ${RECEIVER_ADDR})+0 \
--tx-out $(cat ${SENDER_ADDR})+0 \
--invalid-hereafter $FINALTIP \
--fee 0 \
--allegra-era \
--out-file tx.draft \

# echo "Calculating Transaction Fee"
FEE=$(cardano-cli transaction calculate-min-fee \
--tx-body-file tx.draft \
--tx-in-count ${TXNS} \
--tx-out-count 2 \
--witness-count 3 \
--mainnet \
--protocol-params-file protocol.json \
| tr -dc '0-9')

CHANGE=$(( ${BALANCE} - ${FEE} ))

# echo "Building Raw Transaction"
cardano-cli transaction build-raw \
--tx-in $HEXTXIN \
--tx-out $(cat ${RECEIVER_ADDR})+${CHANGE} \
--invalid-hereafter $FINALTIP \
--fee $FEE \
--allegra-era \
--out-file tx.raw \

# echo "Signing Transaction"
cardano-cli transaction sign \
--tx-body-file tx.raw \
--signing-key-file ${BASE}${SENDER}"_user/"${SENDER}"_payment.skey" \
--mainnet \
--out-file tx.signed


###### THIS MAKES IT LIVE #####################################################
cardano-cli transaction submit \
--tx-file tx.signed \
--mainnet
###############################################################################