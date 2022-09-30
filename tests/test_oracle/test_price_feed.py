import pytest
from brownie import *

import brownie

def test_eth_btc_usd(mainnetpricer, oneE18): 
  pricer = mainnetpricer 
  pETH = pricer.getEthUsdPrice()
  assert pETH > 800 * 100000000 
  
  pBTC = pricer.getBtcUsdPrice()
  assert pBTC > 10000 * 100000000  
  
  pBTCETH = interface.FeedRegistryInterface(pricer.FEED_REGISTRY()).latestRoundData("0xbBbBBBBbbBBBbbbBbbBbbbbBBbBbbbbBbBbbBBbB", "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE")
  assert pBTCETH[1] > 5 * oneE18

  assert abs((pBTC / pETH) - (pBTCETH[1] / oneE18)) / (pBTC / pETH) < 0.02

def test_eth_feed(mainnetpricer, badger, wbtc, balethbpt, oneE18):  
  pricer = mainnetpricer 
  pWBTCETH = pricer.getPriceInETH(wbtc.address)
  assert pWBTCETH > 6 * oneE18
  
  pBadgerETH = pricer.getPriceInETH(badger.address)
  assert pBadgerETH > 0.0005 * oneE18
   
  pBalBptETH = pricer.getPriceInETH(balethbpt.address)
  assert pBalBptETH == 0  

def test_usd_feed(mainnetpricer, badger, balethbpt, usdc, usdt, dai, weth, oneE18):
  pricer = mainnetpricer   
  pUSDCUSD = pricer.getPriceInUSD(usdc.address)
  assert pUSDCUSD > 0.97 * 100000000 
  
  pUSDTUSD = pricer.getPriceInUSD(usdt.address)
  assert pUSDTUSD > 0.97 * 100000000 
  
  pDAIUSD = pricer.getPriceInUSD(dai.address)
  assert pDAIUSD > 0.9 * 100000000
  
  pBadgerUSD = pricer.getPriceInUSD(badger.address)
  assert pBadgerUSD > 1 * 100000000
   
  pBalBptUSD = pricer.getPriceInUSD(balethbpt.address)
  assert pBalBptUSD == 0  

def test_btc_feed(mainnetpricer, wbtc, balethbpt, oneE18): 
  pricer = mainnetpricer   
  pWBTC = pricer.getPriceInBTC(wbtc.address)
  assert pWBTC > 0.995 * 100000000
   
  pBalBptBTC = pricer.getPriceInBTC(balethbpt.address)
  assert pBalBptBTC == 0  

def test_fetch_usd(mainnetpricer, weth, wbtc, badger, ohm, aura, usdc, usdt): 
  pricer = mainnetpricer   
  pWETH = pricer.fetchUSDFeed(weth.address)  
  pETH = pricer.getEthUsdPrice()
  assert pWETH == pETH 
  
  pBadger = pricer.fetchUSDFeed(badger.address)  
  pBadgerUSD = pricer.getPriceInUSD(badger.address)
  assert pBadgerUSD == pBadger
  
  pWBTC = pricer.fetchUSDFeed(wbtc.address)  
  pBTC = pricer.getBtcUsdPrice()
  assert abs(pWBTC - pBTC) / pWBTC < 0.015
  
  pOHMv2 = pricer.fetchUSDFeed(ohm.address) 
  assert pOHMv2 > 5 * 100000000  
  
  pAura = pricer.fetchUSDFeed(aura.address) 
  assert pAura == 0
  
  pUSDC = pricer.fetchUSDFeed(usdc.address) 
  assert pUSDC == 1 * 100000000  
  
  pUSDT = pricer.fetchUSDFeed(usdt.address) 
  assert pUSDT == 1 * 100000000  

def test_staleness(mainnetpricer, wbtc, badger, oneE18):   
  pricer = mainnetpricer   
  pETH = pricer.getEthUsdPrice()
  assert pETH > 800 * 100000000 
  
  pBTC = pricer.getBtcUsdPrice()
  assert pBTC > 10000 * 100000000  
  
  pBadgerETH = pricer.getPriceInETH(badger.address)
  assert pBadgerETH > 0.0005 * oneE18
   
  pBadgerUSD = pricer.getPriceInUSD(badger.address)
  assert pBadgerUSD > 1 * 100000000
  
  pWBTC = pricer.getPriceInBTC(wbtc.address)
  assert pWBTC > 0.995 * 100000000
  
  ## one hour heartbeat
  chain.sleep(3600 + 1)
  chain.mine(1)
  with brownie.reverts("!stale"):
       pricer.getEthUsdPrice()
  with brownie.reverts("!stale"):
       pricer.getBtcUsdPrice()
       
  ## 24 hours heartbeat
  chain.sleep(86400 + 1)
  chain.mine(1)  
  with brownie.reverts("!stale"):
       pricer.getPriceInETH(badger.address)
  with brownie.reverts("!stale"):
       pricer.getPriceInUSD(badger.address)
  with brownie.reverts("!stale"):
       pricer.getPriceInBTC(wbtc.address)
       
def test_feed_quote(mainnetpricer, weth, badger, ohm, wbtc, usdc, aura, usdt, oneE18):    
  pricer = mainnetpricer   
  pBadgerETH = pricer.tryQuoteWithFeed(badger.address, weth.address, 100 * oneE18)  
  assert pBadgerETH >= 100 * 0.001 * oneE18
  
  pETHBadger = pricer.tryQuoteWithFeed(weth.address, badger.address, 1 * oneE18)  
  assert pETHBadger >= 1 * 300 * oneE18
  
  pWBTCUSDC = pricer.tryQuoteWithFeed(wbtc.address, usdc.address, 1 * 100000000)  
  assert pWBTCUSDC >= 1 * 10000 * 1000000 
  
  pOhmETH = pricer.tryQuoteWithFeed(ohm.address, weth.address, 100 * 1000000000)  
  assert pOhmETH >= 100 * 0.001 * oneE18
  
  pAuraETH = pricer.tryQuoteWithFeed(aura.address, weth.address, 1000 * oneE18)  
  assert pAuraETH > 1000 * 0.001 * oneE18 
  
  pETHAura = pricer.tryQuoteWithFeed(weth.address, aura.address, 1 * oneE18)  
  assert pETHAura > 1 * 300 * oneE18
  
  gno = "0x6810e776880c02933d47db1b9fc05908e5386b96"
  cow = "0xdef1ca1fb7fbcdc777520aa7f396b4e015f497ab"
  dummy = "0xc5023255Ad7E0E49D207FAD2bb628312ceA51153"
  pGNOCOW = pricer.tryQuoteWithFeed(gno, cow, 10 * oneE18)  
  assert pGNOCOW > 10 * 1000 * oneE18
  
  pUSDCCOW = pricer.tryQuoteWithFeed(usdc.address, cow, 1000 * 1000000)  
  assert pUSDCCOW > 1000 * 5 * oneE18
  
  pCOWUSDC = pricer.tryQuoteWithFeed(cow, usdc.address, 10000 * oneE18)  
  assert pCOWUSDC > 10000 * 0.05 * 1000000
  
  pWETHUSDT = pricer.tryQuoteWithFeed(weth.address, usdt.address, 1 * oneE18)
  assert pWETHUSDT > 1 * 800 * 1000000  
  
  pOHMGNO = pricer.tryQuoteWithFeed(ohm.address, gno, 1000 * oneE18)
  assert pOHMGNO > 1000 * 0.03 * oneE18  
  
  pAURACOW = pricer.tryQuoteWithFeed(aura.address, cow, 10000 * oneE18)
  assert pAURACOW == 0  
  
  pOHMDUMMY = pricer.tryQuoteWithFeed(ohm.address, dummy, 1 * oneE18)
  assert pOHMDUMMY == 0 
  
  pDUMMYOHM = pricer.tryQuoteWithFeed(dummy, ohm.address, 1 * oneE18)
  assert pDUMMYOHM == 0

def test_registry_gas_usge(pricerwrapper, weth, badger, usdc, oneE18):   
  pBadgerQuote = pricerwrapper.tryQuoteWithFeedNonView(badger.address, weth.address, 1000 * oneE18)
  assert pBadgerQuote.return_value[0] < 23000 # gas consumption
  
  pBadgerUSDQuote = pricerwrapper.tryQuoteWithFeedNonView(badger.address, usdc.address, 1000 * oneE18)
  assert pBadgerUSDQuote.return_value[0] < 23000 # gas consumption  
  
  rgt = "0xD291E7a03283640FDc51b121aC401383A46cC623"
  pRGTQuote = pricerwrapper.tryQuoteWithFeedNonView(rgt, weth.address, 10000 * oneE18)
  assert pRGTQuote.return_value[1] > 0
  assert pRGTQuote.return_value[0] < 25000 # gas consumption
  
  pRGTUSDQuote = pricerwrapper.tryQuoteWithFeedNonView(rgt, usdc.address, 10000 * oneE18)
  assert pRGTUSDQuote.return_value[1] > 0
  assert pRGTUSDQuote.return_value[0] < 39000 # gas consumption
  
def test_find_executable_swap(pricer, aura, oneE18): 
  pAURAGNO = pricer.findExecutableSwap(aura.address, "0x6810e776880c02933d47db1b9fc05908e5386b96", 100000 * oneE18)  
  assert pAURAGNO[1] >= 100000 * 0.008 * oneE18 
  assert pAURAGNO[0] == 6 ##BALANCERWITHWETH 

