import brownie
from brownie import *
import pytest
import random

"""
    Benchmark test for feed gas profiling in tryQuoteWithFeed with focus in DeFi category
    Selected tokens from https://defillama.com/chain/Ethereum
    This file is ok to be exclcuded in test suite due to its underluying functionality should be covered by other tests
    Rename the file to test_benchmark_token_gas_feed.py to make this part of the testing suite if required and run with `--gas`
"""

TOP_DECIMAL18_TOKENS = [
  ("0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2", 100),      # MKR
  ("0x5a98fcbea516cf06857215779fd812ca3bef1b32", 10000),    # LDO
  ("0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", 10000),    # UNI
  ("0xd533a949740bb3306d119cc777fa900ba034cd52", 10000),    # CRV
  ("0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9", 1000),     # AAVE
  ("0x4e3fbd56cd56c3e72c1403e103b45db9da5b9d2b", 10000),    # CVX
  ("0xc00e94cb662c3520282e6f5717214004a7f26888", 1000),     # COMP
  ("0x6f40d4A6237C257fff2dB00FA0510DeEECd303eb", 10000),    # INST
  ("0xba100000625a3754423978a60c9317c58a424e3D", 10000),    # BAL
  ("0x3432b6a60d23ca0dfca7761b7ab56459d9c964d0", 10000),    # FXS
  ("0x6b3595068778dd592e39a122f4f5a5cf09c90fe2", 10000),    # SUSHI
  ("0x92D6C1e31e14520e676a687F0a93788B716BEff5", 10000),    # DYDX
  ("0x0bc529c00c6401aef6d220be8c6ea1667f6ad93e", 10),       # YFI
  ("0x6DEA81C8171D0bA574754EF6F8b412F2Ed88c54D", 50000),    # LQTY
  ("0xd33526068d116ce69f19a9ee46f0bd304f21a51f", 1000),     # RPL
  ("0x090185f2135308bad17527004364ebcc2d37e5f6", 10000000), # SPELL
  ("0x77777feddddffc19ff86db637967013e6c6a116c", 1000),     # TORN
  ("0xc011a73ee8576fb46f5e1c5751ca3b9fe0af2a6f", 10000),    # SNX
  ("0x0d438f3b5175bebc262bf23753c1e53d03432bde", 1000),     # WNXM
  ("0xff20817765cb7f73d4bde2e66e067e58d11095c2", 10000000), # AMP
  ("0xd9Fcd98c322942075A5C3860693e9f4f03AAE07b", 1000),     # EUL
  ("0x1f573d6fb3f13d689ff844b4ce37794d79a7ff1c", 50000),    # BNT
  ("0xdbdb4d16eda451d0503b854cf79d55697f90c8df", 1000),     # ALCX
  ("0x73968b9a57c6e53d41345fd57a6e6ae27d6cdb2f", 50000),    # SDT
  ("0x31429d1856ad1377a8a0079410b297e1a9e214c2", 1000000),  # ANGLE
  ("0x04Fa0d235C4abf4BcF4787aF4CF447DE572eF828", 10000),    # UMA
  ("0x6123B0049F904d730dB3C36a31167D9d4121fA6B", 50000),    # RBN
  ("0x956F47F50A910163D8BF957Cf5846D573E7f87CA", 10000),    # FEI
  ("0x853d955acef822db058eb8505911ed77f175b99e", 10000),    # FRAX
  ("0xD291E7a03283640FDc51b121aC401383A46cC623", 10000),    # RGT
  ("0x1b40183efb4dd766f11bda7a7c3ad8982e998421", 50000),    # VSP  
  ("0x0cec1a9154ff802e7934fc916ed7ca50bde6844e", 50000),    # POOL  
  ("0x43dfc4159d86f3a37a5a4b3d4580b888ad7d4ddd", 50000),    # DODO  
  ("0xe28b3b32b6c345a34ff64674606124dd5aceca30", 10000),    # INJ
  ("0x0f2d719407fdbeff09d87557abb7232601fd9f29", 10000),    # SYN  
  ("0xC0c293ce456fF0ED870ADd98a0828Dd4d2903DBF", 10000),    # AURA   
  ("0x3472A5A71965499acd81997a54BBA8D852C6E53d", 10000),    # BADGER  
  ("0x6810e776880C02933D47DB1b9fc05908e5386b96", 500),      # GNO  
  ("0xDEf1CA1fb7FBcDC777520aa7f396b4E015F497aB", 100000),   # COW  
  ("0xE80C0cd204D654CEbe8dd64A4857cAb6Be8345a3", 10000000), # JPEG 
  ("0xAf5191B0De278C7286d6C7CC6ab6BB8A73bA2Cd6", 10000),    # STG
  ("0x616e8BfA43F920657B3497DBf40D6b1A02D4608d", 10000),    # auraBAL
  ("0x62b9c7356a2dc64a1969e19c23e4f579f9810aa7", 10000),    # cvxCRV
  ("0x41d5d79431a913c4ae7d69a668ecdfe5ff9dfb68", 1000),     # INV
  ("0x6243d8cea23066d098a15582d81a598b4e8391f4", 1000),     # FLX
  ("0x01BA67AAC7f75f647D94220Cc98FB30FCc5105Bf", 100000),   # LYRA
  ("0xFEEf77d3f69374f66429C91d732A244f074bdf74", 10000),    # cvxFXS
  ("0xa3BeD4E1c75D00fa6f4E5E6922DB7261B5E9AcD2", 1000000),  # MTA
  ("0x8207c1FfC5B6804F6024322CcF34F29c3541Ae26", 1000000),  # OGN
  ("0x674C6Ad92Fd080e4004b2312b45f796a192D27a0", 10000),    # USDN
  ("0x408e41876cccdc0f92210600ef50372656052a38", 100000),   # REN
]

@pytest.mark.parametrize("token,count", TOP_DECIMAL18_TOKENS)
def test_feed_gas(oneE18, weth, usdc, token, count, pricerwrapper):
  pricer = pricerwrapper
  sell_token = token
  buy_token = weth.address if random.random() > 0.5 else usdc.address
  ## 1e18
  sell_count = count
  sell_amount = sell_count * oneE18 ## 1e18
    
  quote = pricer.tryQuoteWithFeedNonView(sell_token, buy_token, sell_amount)
  quote.call_trace()
  assert quote.return_value[0] < 38000 ## gas consumption  
 