#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 13:37:02 2022

@author: juan
"""

import numpy as np
import pandas as pd
from web3 import Web3
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()
import json





class DEXGen:
    def __init__(self,factoryAddress:str,
                     Infura_HTTP:str,
                     factory_abi:str,
                     pair_abi:str,
                     erc20_abi:str):
                     
                             
        with open(factory_abi) as f:
            info_json = json.load(f)
        self.abi = info_json["abi"]
        with open(pair_abi) as f:
            info_json = json.load(f)
        self.abiPair = info_json["abi"]
        with open(erc20_abi) as f:
            self.erc20 = json.load(f)
    
        self.factoryAddress=factoryAddress
        self.Infura_HTTP=Infura_HTTP
        self.w3 = Web3(Web3.HTTPProvider(Infura_HTTP))
        self.factory = self.w3.eth.contract(factoryAddress,abi=self.abi)
                     

    def getPairData(self,tokenA,tokenB,dexName='uniswapV2',chainId=1):
        w3=self.w3
        factory=self.factory
        try:
            pair_address=factory.functions.getPair(tokenA,tokenB).call()
        except:
            return 
        
        pool=self.w3.eth.contract(pair_address,abi=self.abiPair)
        res=pool.functions.getReserves().call()
        token0Address=pool.functions.token0().call()
        token1Address=pool.functions.token1().call()
        token0Info=self.w3.eth.contract(token0Address,abi=self.erc20)
        token1Info=self.w3.eth.contract(token1Address,abi=self.erc20)
            
        def getTokenData(tokenI,indx):
            decimals=tokenI.functions.decimals().call()
            token={
                    "name":tokenI.functions.name().call(),
                    "symbol":tokenI.functions.symbol().call(),
                    "address":tokenI.address,
                    "decimals":decimals,
                    "liquidity":res[indx]/10**decimals,
                    }
            return token
        
        
        
        
        token0=getTokenData(token0Info,indx=0)
        token1=getTokenData(token1Info,indx=1)
        
        dexInfo={
            'type':'dex',
            'gasUnits':103000, # to find
            'name': dexName,
            'Address':pair_address,
            'chainId':chainId,
            'PairName':dexName+'_'+token0['symbol']+'_'+token1['symbol'],
            "token0":token0,
            "token1":token1
            }
        return dexInfo

if __name__=='__main__':
    FACT_ADDRESS='0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
    Infura_HTTP = 'https://mainnet.infura.io/v3/0616444dc78c4f9889ae8685a6156da6'
    ERC20_ABI='erc20.json'
    UNI_V2_PAIR='univ2Pair.json'
    UNI_V2_FACTORY='univ2_abi.json'
    

    
    
    
    
    tokenA='0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
    tokenB='0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984'
    dexs=DEXGen(factoryAddress=FACT_ADDRESS,
                Infura_HTTP=Infura_HTTP,
                factory_abi=UNI_V2_FACTORY,
                pair_abi=UNI_V2_PAIR,
                erc20_abi=ERC20_ABI)
                
    
                
                
    dexEntry=dexs.getPairData(tokenA,tokenB, dexName='univ2',chainId='1')
    
    
    #ok now does the whole thing:
    ListOfEntries=[]
    tokens=[
    {'name':'usdc',
     'address':'0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'},
    {'name':'busd',
     'address':'0x4Fabb145d64652a948d72533023f6E7A623C7C53'},
    {'name':'dai',
     'address':'0x6B175474E89094C44Da98b954EedeAC495271d0F'},
    {'name':'hex',
     'address':'0x2b591e99afE9f32eAA6214f7B7629768c40Eeb39'},
    {'name':'wbtc',
     'address':'0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599'},
    {'name':'theta',
     'address':'0x3883f5e181fccaF8410FA61e12b59BAd963fb645'},
    {'name':'leo',
     'address':'0x2AF5D2aD76741191D15Dfe7bF6aC92d4Bd912Ca3'},
    {'name':'shib',
     'address':'0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE'},
    {'name':'matic',
     'address':'0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0'},
    {'name':'uni',
     'address':'0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984'},
    {'name':'wfil',
     'address':'0x6e1A19F235bE7ED8E3369eF73b196C07257494DE'},
    {'name':'bat',
     'address':'0x0d8775f648430679a709e98d2b0cb6250d2887ef'},
    {'name':'weth',
     'address':'0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'},
    ]
    
    ii=0
        
    for tokenA in tokens:
        for tokenB in tokens:
            if tokenA !=tokenB:
                print('iteration '+str(ii))
                
                
                try: # so that it can fail silently, lol 
                    ListOfEntries.append(dexs.getPairData(tokenA['address'],
                                            tokenB['address'],dexName='univ2',chainId='1'))
                except:
                    pass
                
                ii+=1



    
    

        