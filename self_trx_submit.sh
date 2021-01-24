#!/bin/bash
set -e

# args
SENDER="main"
AMOUNT=1
RECEIVER=$SENDER
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
# move to tmp folder
cd ${TMP_FOLDER}


###### THIS MAKES IT LIVE #####################################################
cardano-cli transaction submit \
--tx-file tx.signed \
--mainnet
###############################################################################