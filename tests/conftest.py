from time import time
from brownie import *
from brownie import (
  accounts,
  interface,
  UniV3SwapSimulator,
  BalancerSwapSimulator,
  OnChainPricingMainnet,
  OnChainPricingMainnetLenient,
  FullOnChainPricingMainnet,
  SwapExecutor
)
import eth_abi
from rich.console import Console
import pytest

console = Console()

MAX_INT = 2**256 - 1
DEV_MULTI = "0xB65cef03b9B89f99517643226d76e286ee999e77"
WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
BADGER = "0x3472A5A71965499acd81997a54BBA8D852C6E53d"
CVX = "0x4e3fbd56cd56c3e72c1403e103b45db9da5b9d2b"
DAI = "0x6b175474e89094c44da98b954eedeac495271d0f"
WBTC = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
OHM="0x64aa3364F17a4D01c6f1751Fd97C2BD3D7e7f1D5"
USDC_WHALE = "0x0a59649758aa4d66e25f08dd01271e891fe52199"
BADGER_WHALE = "0xd0a7a8b98957b9cd3cfb9c0425abe44551158e9e"
CVX_WHALE = "0xcf50b810e57ac33b91dcf525c6ddd9881b139332"
DAI_WHALE = "0x8EB8a3b98659Cce290402893d0123abb75E3ab28"
AURA = "0xC0c293ce456fF0ED870ADd98a0828Dd4d2903DBF"
AURABAL = "0x616e8BfA43F920657B3497DBf40D6b1A02D4608d"
BVE_CVX = "0xfd05D3C7fe2924020620A8bE4961bBaA747e6305"
BVE_AURA = "0xBA485b556399123261a5F9c95d413B4f93107407"
AURA_WHALE = "0x43B17088503F4CE1AED9fB302ED6BB51aD6694Fa"
BALANCER_VAULT = "0xBA12222222228d8Ba445958a75a0704d566BF2C8"
BVE_AURA_WETH_AURA_POOL_ID = "0xa3283e3470d3cd1f18c074e3f2d3965f6d62fff2000100000000000000000267"
CVX_BVECVX_POOL = "0x04c90C198b2eFF55716079bc06d7CCc4aa4d7512"
BALETH_BPT = "0x5c6Ee304399DBdB9C8Ef030aB642B10820DB8F56"
USDT = "0xdac17f958d2ee523a2206206994597c13d831ec7"
TUSD = "0x0000000000085d4780B73119b644AE5ecd22b376"
XSUSHI = "0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272"

WETH_WHALE = "0x8EB8a3b98659Cce290402893d0123abb75E3ab28"
CRV = "0xD533a949740bb3306d119CC777fa900bA034cd52"
WBTC_WHALE = "0xbf72da2bd84c5170618fbe5914b0eca9638d5eb5"

## Contracts ##
  
@pytest.fixture
def swapexecutor(pricer):
  return SwapExecutor.deploy(pricer.address, {"from": accounts[0]})
  
@pytest.fixture
def mainnetpricer():
  univ3simulator = UniV3SwapSimulator.deploy({"from": accounts[0]})
  balancerV2Simulator = BalancerSwapSimulator.deploy({"from": accounts[0]})
  c = OnChainPricingMainnet.deploy(univ3simulator.address, balancerV2Simulator.address, {"from": accounts[0]})  
  return c
  
@pytest.fixture
def pricerwrapper():
  univ3simulator = UniV3SwapSimulator.deploy({"from": accounts[0]})
  balancerV2Simulator = BalancerSwapSimulator.deploy({"from": accounts[0]})
  c = OnChainPricingMainnet.deploy(univ3simulator.address, balancerV2Simulator.address, {"from": accounts[0]})  
  return PricerWrapper.deploy(c.address, {"from": accounts[0]})

@pytest.fixture
def pricer():
  univ3simulator = UniV3SwapSimulator.deploy({"from": accounts[0]})
  balancerV2Simulator = BalancerSwapSimulator.deploy({"from": accounts[0]})
  c = OnChainPricingMainnetLenient.deploy(univ3simulator.address, balancerV2Simulator.address, {"from": accounts[0]})
  c.setSlippage(0, {"from": accounts.at(c.TECH_OPS(), force=True)})
  return c

@pytest.fixture
def pricer_legacy():
  return FullOnChainPricingMainnet.deploy({"from": accounts[0]})

@pytest.fixture
def lenient_contract():
  ## NOTE: We have 5% slippage on this one
  univ3simulator = UniV3SwapSimulator.deploy({"from": accounts[0]})
  balancerV2Simulator = BalancerSwapSimulator.deploy({"from": accounts[0]})
  c = OnChainPricingMainnetLenient.deploy(univ3simulator.address, balancerV2Simulator.address, {"from": accounts[0]})
  c.setSlippage(499, {"from": accounts.at(c.TECH_OPS(), force=True)})

  return c

@pytest.fixture
def oneE18():
  return 1000000000000000000

@pytest.fixture
def xsushi():
  return interface.ERC20(XSUSHI)

@pytest.fixture
def tusd():
  return interface.ERC20(TUSD)

@pytest.fixture
def usdt():
  return interface.ERC20(USDT)

@pytest.fixture
def balethbpt():
  return interface.ERC20(BALETH_BPT)

@pytest.fixture
def aurabal():
  return interface.ERC20(AURABAL)

@pytest.fixture
def ohm():
  return interface.ERC20(OHM)

@pytest.fixture
def wbtc():
  return interface.ERC20(WBTC)

@pytest.fixture
def balancer_vault():
  return interface.IBalancerVault(BALANCER_VAULT)

@pytest.fixture
def cvx_bvecvx_pool():
  return interface.ICurvePool(CVX_BVECVX_POOL)

@pytest.fixture
def crv():
  return interface.ERC20(CRV)

@pytest.fixture
def usdc():
  return interface.ERC20(USDC)

@pytest.fixture
def weth():
  return interface.ERC20(WETH)

@pytest.fixture
def badger():
  return interface.ERC20(BADGER)

@pytest.fixture
def cvx():
  return interface.ERC20(CVX)
  
@pytest.fixture
def dai():
  return interface.ERC20(DAI)

@pytest.fixture
def aura():
  return interface.ERC20(AURA)

@pytest.fixture
def usdc_whale():
  return accounts.at(USDC_WHALE, force=True)

@pytest.fixture
def badger_whale():
  return accounts.at(BADGER_WHALE, force=True)

@pytest.fixture
def cvx_whale():
  return accounts.at(CVX_WHALE, force=True)
  
@pytest.fixture
def weth_whale():
  return accounts.at(WETH_WHALE, force=True)

@pytest.fixture
def wbtc_whale():
  return accounts.at(WBTC_WHALE, force=True)

@pytest.fixture
def aura_whale():
  return accounts.at(AURA_WHALE, force=True)
  
@pytest.fixture
def pricer_V_0_3_deployed():
  return PricerWrapper.deploy("0x2DC7693444aCd1EcA1D6dE5B3d0d8584F3870c49", {"from": accounts[0]})

## Forces reset before each test
@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass