import pytest
from brownie import *

import brownie
import pytest

## This test require the connected chain is snapshot at block#13537932
## You could add a local fork and use it in test by configuring brownie-config.yml: 
## brownie networks add development hardhat-local-fork cmd=ganache-cli host=http://127.0.0.1 fork=RPC_URL@13537932 accounts=10 mnemonic=brownie port=8545
@pytest.mark.require_network("hardhat-local-fork")
def test_rari_fuse_pool23_deny(pricer, oneE18): 
  vusd_usdc_pool = "0x8dDE0A1481b4A14bC1015A5a8b260ef059E9FD89"
  
  ## some configuration deployment in conftest
  if chain.height >= 13537932 and chain.height <= 13537942:
  
     liq = interface.IUniswapV3Pool(vusd_usdc_pool).liquidity()
     checkTwap = pricer.checkUniV3PoolOracle(vusd_usdc_pool, liq)
  
     ## TWAP check will tell us sth is off
     assert checkTwap == False
 
## This test require snapshot on another block heigh#13537921
## brownie networks add development hardhat-local-fork cmd=ganache-cli host=http://127.0.0.1 fork=RPC_URL@13537921 accounts=10 mnemonic=brownie port=8545
@pytest.mark.require_network("hardhat-local-fork")
def test_rari_fuse_pool23_ok(pricer, oneE18): 
  vusd_usdc_pool = "0x8dDE0A1481b4A14bC1015A5a8b260ef059E9FD89"
  
  ## some configuration deployment in conftest
  if chain.height >= 13537921 and chain.height <= 13537931:
  
     liq = interface.IUniswapV3Pool(vusd_usdc_pool).liquidity()
     checkTwap = pricer.checkUniV3PoolOracle(vusd_usdc_pool, liq)
  
     ## TWAP check will tell us everything is fine
     assert checkTwap == True

@pytest.mark.require_network("mainnet-fork")
def test_price_manipulate(pricer, pricer_V_0_3_deployed, weth_whale, weth, oneE18): 
  looks = "0xf4d2888d29D722226FafA5d9B24F9164c092421E"
  weth_looks_pool = "0x4b5ab61593a2401b1075b90c04cbcdd3f87ce011"
  
  liqBefore = interface.IUniswapV3Pool(weth_looks_pool).liquidity()
  checkTwapBefore = pricer.checkUniV3PoolOracle(weth_looks_pool, liqBefore)
  
  ## TWAP check will tell us everything is fine
  assert checkTwapBefore == True
  
  ## do a big pump trade: swap 100K weth to looks
  uniswap_v3_router = "0xE592427A0AEce92De3Edee1F18E0157C05861564"
  oneM = 1000000
  weth.approve(uniswap_v3_router, oneM * oneE18, {'from': weth_whale})
  interface.IUniswapRouterV3(uniswap_v3_router).exactInputSingle([weth.address, looks, 3000, weth_whale.address, 1695456431, 100000 * oneE18, 0, 0], {'from': weth_whale})
  
  ## TWAP check will tell us sth is off
  liq = interface.IUniswapV3Pool(weth_looks_pool).liquidity()
  checkTwap = pricer.checkUniV3PoolOracle(weth_looks_pool, liq)
  assert checkTwap == False
  quote = pricer.unsafeFindExecutableSwap(looks, weth.address, oneM * oneE18)  
  assert quote[1] == 0 ## no valid quote due to manipulation
  
  ## While V3 pricer might still try to return best quote though manipulated
  quoteV3 = pricer_V_0_3_deployed.findOptimalSwap(looks, weth.address, oneM * oneE18)  
  assert quoteV3[1][0] == 3 ## univ3
  assert quoteV3[1][1] > oneM * 0.09 * oneE18 ## badger usually should be around below 0.001 ETH
  