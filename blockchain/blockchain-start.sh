#!/bin/bash

./geth.bin --datadir=./ --syncmode=full --rpc --rpcapi="eth,net,rpc,web3,txpool,personal,debug,account" --miner.gasprice=100 --txpool.locals="0x1dF62f291b2E969fB0849d99D9Ce41e2F137006e" --rpccorsdomain='*' --allow-insecure-unlock --unlock "0x90f8bf6a479f320ead074411a4b0e7944ea8c9c1,0xffcf8fdee72ac11b5c542428b35eef5769c409f0" --password ./account-password.txt --port 4030 --port 40303 --rpcport=9545 console
