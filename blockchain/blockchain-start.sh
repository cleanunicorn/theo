#!/bin/bash

geth --datadir=./ --rpc --rpcapi="eth,net,rpc,web3,txpool,personal,debug" --rpccorsdomain='*' --allow-insecure-unlock --unlock "0x90f8bf6a479f320ead074411a4b0e7944ea8c9c1,0xffcf8fdee72ac11b5c542428b35eef5769c409f0,0x1df62f291b2e969fb0849d99d9ce41e2f137006e,0x22d491bde2303f2f43325b2108d26f1eaba1e32b,0xe11ba2b4d45eaed5996cd0823791e0c93114882d" --password ./account-password.txt console