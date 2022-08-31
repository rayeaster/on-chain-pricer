import pytest
from brownie import *

def test_eth_btc_usd(pricer, oneE18):  
  pETH = pricer.getEthUsdPrice()
  assert pETH > 800 * 100000000 
  
  pBTC = pricer.getBtcUsdPrice()
  assert pBTC > 10000 * 100000000  
  
  pBTCETH = interface.FeedRegistryInterface(pricer.FEED_REGISTRY()).latestRoundData("0xbBbBBBBbbBBBbbbBbbBbbbbBBbBbbbbBbBbbBBbB", "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE")
  assert pBTCETH[1] > 5 * oneE18

  assert abs((pBTC / pETH) - (pBTCETH[1] / oneE18)) / (pBTC / pETH) < 0.015

def test_eth_feed(pricer, badger, balethbpt, oneE18): 
  pBadgerETH = pricer.getPriceInETH(badger.address)
  assert pBadgerETH > 0.0005 * oneE18
   
  pBalBptETH = pricer.getPriceInETH(balethbpt.address)
  assert pBalBptETH == 0  

def test_usd_feed(pricer, badger, balethbpt, oneE18): 
  pBadgerUSD = pricer.getPriceInUSD(badger.address)
  assert pBadgerUSD > 1 * 100000000
   
  pBalBptUSD = pricer.getPriceInUSD(balethbpt.address)
  assert pBalBptUSD == 0  

def test_btc_feed(pricer, wbtc, balethbpt, oneE18): 
  pWBTC = pricer.getPriceInBTC(wbtc.address)
  assert pWBTC > 0.995 * 100000000
   
  pBalBptBTC = pricer.getPriceInBTC(balethbpt.address)
  assert pBalBptBTC == 0  

def test_fetch_usd(pricer, weth, wbtc, badger, ohm): 
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

  

