import brownie
from brownie import *
import pytest
import random

"""
    Benchmark test for feed gas profiling in tryQuoteWithFeed() with focus in badgerdao strategy ecosystem
    This file is ok to be exclcuded in test suite due to its underluying functionality should be covered by other tests
    Rename the file to test_benchmark_token_gas_feed.py to make this part of the testing suite if required and run with `--gas`
"""

TOP_DECIMAL18_TOKENS = [
  ("0x5a98fcbea516cf06857215779fd812ca3bef1b32", 10000),    # LDO
  ("0x4e3fbd56cd56c3e72c1403e103b45db9da5b9d2b", 10000),    # CVX
  ("0xd533a949740bb3306d119cc777fa900ba034cd52", 10000),    # CRV
  ("0xba100000625a3754423978a60c9317c58a424e3D", 10000),    # BAL
  ("0x3432b6a60d23ca0dfca7761b7ab56459d9c964d0", 10000),    # FXS
  ("0xd33526068d116ce69f19a9ee46f0bd304f21a51f", 1000),     # RPL
  ("0xc7283b66Eb1EB5FB86327f08e1B5816b0720212B", 10000),    # TRIBE
  ("0x090185f2135308bad17527004364ebcc2d37e5f6", 10000000), # SPELL
  ("0x31429d1856ad1377a8a0079410b297e1a9e214c2", 100000),  # ANGLE
  ("0x956F47F50A910163D8BF957Cf5846D573E7f87CA", 10000),    # FEI
  ("0x853d955acef822db058eb8505911ed77f175b99e", 10000),    # FRAX 
  ("0xC0c293ce456fF0ED870ADd98a0828Dd4d2903DBF", 10000),    # AURA  
  ("0x6810e776880C02933D47DB1b9fc05908e5386b96", 500),      # GNO 
  ("0x616e8BfA43F920657B3497DBf40D6b1A02D4608d", 4000),     # auraBAL
  ("0x62b9c7356a2dc64a1969e19c23e4f579f9810aa7", 10000),    # cvxCRV
  ("0x41d5d79431a913c4ae7d69a668ecdfe5ff9dfb68", 1000),     # INV
  ("0x6243d8cea23066d098a15582d81a598b4e8391f4", 1000),     # FLX
  ("0x01BA67AAC7f75f647D94220Cc98FB30FCc5105Bf", 100000),   # LYRA
  ("0xa3BeD4E1c75D00fa6f4E5E6922DB7261B5E9AcD2", 1000000),  # MTA
  ("0x8207c1FfC5B6804F6024322CcF34F29c3541Ae26", 1000000),  # OGN
  ("0x674C6Ad92Fd080e4004b2312b45f796a192D27a0", 10000),    # USDN
]

@pytest.mark.parametrize("token,count", TOP_DECIMAL18_TOKENS)
def test_oracle_feed_coverage(oneE18, weth, usdc, token, count, pricerwrapper):
  pricer = pricerwrapper
  sell_token = token
  buy_token = weth.address if random.random() > 0.5 else usdc.address
  ## 1e18
  sell_count = count
  sell_amount = sell_count * oneE18 ## 1e18
    
  ## if tryQuoteWithFeed() return non-zero, so does findOptimalSwap()
  quote = pricer.tryQuoteWithFeedNonView(sell_token, buy_token, sell_amount)
  print('SELLING ' + str(sell_amount) + ' ' + sell_token + ' FOR ' + buy_token)
  assert quote.return_value[0] < 160000 ## gas consumption for price feed with possible quote from on-chain dex sources  
  assert quote.return_value[1] > 0 ## finalQuote is non-zero
 