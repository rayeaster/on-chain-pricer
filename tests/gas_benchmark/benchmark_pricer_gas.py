import brownie
from brownie import *
import pytest

"""
    Benchmark test for gas cost in findOptimalSwap on various conditions
    This file is ok to be exclcuded in test suite due to its underluying functionality should be covered by other tests
    Rename the file to test_benchmark_pricer_gas.py to make this part of the testing suite if required
"""

def test_gas_only_uniswap_v2(oneE18, weth, pricerwrapper):
  pricer = pricerwrapper   
  token = "0xf0f9d895aca5c8678f706fb8216fa22957685a13" # some swap (CULTDAO-WETH) only in Uniswap V2  
  ## 1e18
  sell_count = 100000000
  sell_amount = sell_count * oneE18 ## 1e9
    
  tx = pricer.unsafeFindExecutableSwap(token, weth.address, sell_amount)
  assert tx[1][0] == 1 ## UNIV2  
  assert tx[1][1] > 0  
  assert tx[0] <= 60000

def test_gas_uniswap_v2_sushi(oneE18, weth, pricerwrapper):
  pricer = pricerwrapper   
  token = "0x2e9d63788249371f1DFC918a52f8d799F4a38C94" # some swap (TOKE-WETH) only in Uniswap V2 & SushiSwap
  ## 1e18
  sell_count = 5000
  sell_amount = sell_count * oneE18 ## 1e18
    
  tx = pricer.unsafeFindExecutableSwap(token, weth.address, sell_amount)
  assert (tx[1][0] == 1 or tx[1][0] == 2) ## SUSHI or UNIV2
  assert tx[1][1] > 0  
  assert tx[0] <= 60000

def test_gas_only_balancer_v2(oneE18, weth, aura, pricerwrapper):
  pricer = pricerwrapper   
  token = aura # some swap (AURA-WETH) only in Balancer V2
  ## 1e18
  sell_count = 8000
  sell_amount = sell_count * oneE18 ## 1e18
    
  tx = pricer.unsafeFindExecutableSwap(token, weth.address, sell_amount)
  assert tx[1][0] == 5 ## BALANCER  
  assert tx[1][1] > 0  
  assert tx[0] <= 100000

def test_gas_only_balancer_v2_with_weth(oneE18, wbtc, aura, pricerwrapper):
  pricer = pricerwrapper   
  token = aura # some swap (AURA-WETH-WBTC) only in Balancer V2 via WETH in between as connector
  ## 1e18
  sell_count = 8000
  sell_amount = sell_count * oneE18 ## 1e18
    
  tx = pricer.unsafeFindExecutableSwap(token, wbtc.address, sell_amount)
  assert tx[1][0] == 6 ## BALANCERWITHWETH  
  assert tx[1][1] > 0  
  assert tx[0] <= 170000

def test_gas_only_uniswap_v3(oneE18, weth, pricerwrapper):
  pricer = pricerwrapper   
  token = "0xf4d2888d29D722226FafA5d9B24F9164c092421E" # some swap (LOOKS-WETH) only in Uniswap V3
  ## 1e18
  sell_count = 600000
  sell_amount = sell_count * oneE18 ## 1e18
    
  tx = pricer.unsafeFindExecutableSwap(token, weth.address, sell_amount)
  assert tx[1][0] == 3 ## UNIV3  
  assert tx[1][1] > 0  
  assert tx[0] <= 140000

def test_gas_only_uniswap_v3_with_weth(oneE18, wbtc, pricerwrapper):
  pricer = pricerwrapper   
  token = "0xf4d2888d29D722226FafA5d9B24F9164c092421E" # some swap (LOOKS-WETH-WBTC) only in Uniswap V3 via WETH in between as connector
  ## 1e18
  sell_count = 600000
  sell_amount = sell_count * oneE18 ## 1e18
    
  tx = pricer.unsafeFindExecutableSwap(token, wbtc.address, sell_amount)
  assert tx[1][0] == 4 ## UNIV3WITHWETH  
  assert tx[1][1] > 0  
  assert tx[0] <= 216000

def test_gas_almost_everything(oneE18, wbtc, weth, pricerwrapper):
  pricer = pricerwrapper   
  token = weth # some swap (WETH-WBTC) almost in every DEX, the most gas-consuming scenario
  ## 1e18
  sell_count = 10
  sell_amount = sell_count * oneE18 ## 1e18
    
  tx = pricer.unsafeFindExecutableSwap(token, wbtc.address, sell_amount)
  assert (tx[1][0] <= 5 or tx[1][0] == 5) ## 
  assert tx[1][1] > 0  
  assert tx[0] <= 210000
  