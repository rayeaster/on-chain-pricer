```python
contract: BalancerSwapSimulator - 59.4%
    BalancerFixedPoint.powUp - 100.0%
    BalancerMath.div - 100.0%
    BalancerFixedPoint.add - 75.0%
    BalancerFixedPoint.mulDown - 75.0%
    BalancerFixedPoint.sub - 75.0%
    BalancerMath.divDown - 75.0%
    BalancerMath.mul - 75.0%
    BalancerSwapSimulator.calcOutGivenIn - 75.0%
    BalancerStableMath._getTokenBalanceGivenInvariantAndAllOtherBalances - 65.0%
    BalancerFixedPoint.divDown - 62.5%
    BalancerFixedPoint.divUp - 62.5%
    BalancerStableMath._calculateInvariant - 61.4%
    BalancerFixedPoint.mulUp - 58.3%
    BalancerMath.divUp - 58.3%
    BalancerLogExpMath.exp - 57.4%
    BalancerLogExpMath.pow - 55.2%
    BalancerLogExpMath._ln - 48.7%

  contract: FullOnChainPricingMainnet - 58.2%
    FullOnChainPricingMainnet._findOptimalSwap - 100.0%
    FullOnChainPricingMainnet._ifUniV3Token0Price - 100.0%
    FullOnChainPricingMainnet.getUniV3Price - 100.0%
    FullOnChainPricingMainnet.getBalancerPrice - 87.5%
    FullOnChainPricingMainnet.getBalancerPriceWithConnector - 77.1%
    FullOnChainPricingMainnet._compareUniV3Tokens - 75.0%
    FullOnChainPricingMainnet._getUniV3Rate - 64.4%
    FullOnChainPricingMainnet._queryUniV3PriceWithSlot - 50.0%
    FullOnChainPricingMainnet.getUniV3PriceWithConnector - 50.0%
    FullOnChainPricingMainnet.getBalancerV2Pool - 36.3%
    FullOnChainPricingMainnet.isPairSupported - 0.0%

  contract: OnChainPricingMainnet - 62.9%
    OnChainPricingMainnet._checkPoolLiquidityAndBalances - 100.0%
    OnChainPricingMainnet._fetchUSDPriceViaBTCFeed - 100.0%
    OnChainPricingMainnet._ifStablecoinForFeed - 100.0%
    OnChainPricingMainnet._ifUniV3Token0Price - 100.0%
    OnChainPricingMainnet._simLoopAllUniV3Pools - 100.0%
    OnChainPricingMainnet.findOptimalSwap - 100.0%
    OnChainPricingMainnet.getBalancerPriceAnalytically - 100.0%
    OnChainPricingMainnet.getPriceInBTC - 100.0%
    OnChainPricingMainnet.getPriceInETH - 100.0%
    OnChainPricingMainnet.getPriceInUSD - 100.0%
    OnChainPricingMainnet.getUniPrice - 100.0%
    OnChainPricingMainnet.pairForUniV2 - 100.0%
    OnChainPricingMainnet.sortUniV3Pools - 100.0%
    OnChainPricingMainnet.univ3_fees - 100.0%
    OnChainPricingMainnet._findOptimalSwap - 95.0%
    OnChainPricingMainnet._fetchUSDAndPiggybackETH - 92.9%
    OnChainPricingMainnet.checkUniV3InRangeLiquidity - 87.5%
    OnChainPricingMainnet._findTokenInBalancePool - 83.3%
    OnChainPricingMainnet._getPriceFromFeedAggregator - 75.0%
    OnChainPricingMainnet._getPriceInDenomination - 75.0%
    OnChainPricingMainnet._feedWithPossibleETHConnector - 64.6%
    OnChainPricingMainnet.getBalancerPriceWithConnectorAnalytically - 58.3%
    OnChainPricingMainnet.getBalancerQuoteWithinPoolAnalytcially - 58.3%
    OnChainPricingMainnet.getUniV3PriceWithConnector - 58.3%
    OnChainPricingMainnet._getDecimalsMultiplier - 56.2%
    OnChainPricingMainnet._useSinglePoolInUniV3 - 43.6%
    OnChainPricingMainnet.getBalancerV2Pool - 30.8%
    OnChainPricingMainnet.isPairSupported - 11.3%
    OnChainPricingMainnet.findExecutableSwap - 0.0%

  contract: OnChainPricingMainnetLenient - 64.3%
    OnChainPricingMainnet._checkPoolLiquidityAndBalances - 100.0%
    OnChainPricingMainnet._findTokenInBalancePool - 100.0%
    OnChainPricingMainnet._ifUniV3Token0Price - 100.0%
    OnChainPricingMainnet._simLoopAllUniV3Pools - 100.0%
    OnChainPricingMainnet._useSinglePoolInUniV3 - 100.0%
    OnChainPricingMainnet.getBalancerPriceAnalytically - 100.0%
    OnChainPricingMainnet.pairForUniV2 - 100.0%
    OnChainPricingMainnet.sortUniV3Pools - 100.0%
    OnChainPricingMainnet.univ3_fees - 100.0%
    OnChainPricingMainnet.getBalancerV2Pool - 90.4%
    OnChainPricingMainnet._ifStablecoinForFeed - 87.5%
    OnChainPricingMainnet.checkUniV3InRangeLiquidity - 87.5%
    OnChainPricingMainnet.getBalancerPriceWithConnectorAnalytically - 83.3%
    OnChainPricingMainnet.getBalancerQuoteWithinPoolAnalytcially - 82.6%
    OnChainPricingMainnet.getUniV3PriceWithConnector - 79.2%
    OnChainPricingMainnet._getPriceFromFeedAggregator - 75.0%
    OnChainPricingMainnet._getPriceInDenomination - 75.0%
    OnChainPricingMainnetLenient.setSlippage - 75.0%
    OnChainPricingMainnet.getUniPrice - 60.0%
    OnChainPricingMainnet._getDecimalsMultiplier - 56.2%
    OnChainPricingMainnet._fetchUSDAndPiggybackETH - 50.0%
    OnChainPricingMainnet.getPriceInETH - 50.0%
    OnChainPricingMainnet.getPriceInUSD - 37.5%
    OnChainPricingMainnet._feedWithPossibleETHConnector - 16.7%
    OnChainPricingMainnet.isPairSupported - 11.3%
    OnChainPricingMainnet._fetchUSDPriceViaBTCFeed - 0.0%
    OnChainPricingMainnet._findOptimalSwap - 0.0%
    OnChainPricingMainnet.findExecutableSwap - 0.0%
    OnChainPricingMainnet.findOptimalSwap - 0.0%
    OnChainPricingMainnet.getPriceInBTC - 0.0%
    OnChainPricingMainnetLenient.unsafeFindExecutableSwap - 0.0%

  contract: PricerWrapper - 0.0%

  contract: UniV3SwapSimulator - 79.5%
    SwapMath._getExactInNextPrice - 100.0%
    TickBitmap.nextInitializedTickWithinOneWord - 100.0%
    UniV3SwapSimulator._getAmountOutputDelta - 100.0%
    UniV3SwapSimulator._getLimitPrice - 100.0%
    UniV3SwapSimulator._getTargetPriceForSwapStep - 100.0%
    BitMath.leastSignificantBit - 97.2%
    BitMath.mostSignificantBit - 97.2%
    TickMath.getSqrtRatioAtTick - 95.6%
    UniV3SwapSimulator._stepInTick - 90.0%
    FullMath.mulDiv - 83.3%
    LiquidityMath.addDelta - 83.3%
    SqrtPriceMath.getNextSqrtPriceFromInput - 83.3%
    FullMath.mulDivRoundingUp - 75.0%
    LowGasSafeMath.add - 75.0%
    SafeCast.toInt256 - 75.0%
    SafeCast.toUint160 - 75.0%
    UniV3SwapSimulator.checkInRangeLiquidity - 75.0%
    TickMath.getTickAtSqrtRatio - 72.5%
    SqrtPriceMath.getAmount0Delta - 66.7%
    SqrtPriceMath.getAmount1Delta - 62.5%
    SwapMath.computeSwapStep - 58.6%
    UniV3SwapSimulator._getNextInitializedTick - 50.0%
    SqrtPriceMath.getNextSqrtPriceFromAmount1RoundingDown - 29.2%
    SqrtPriceMath.getNextSqrtPriceFromAmount0RoundingUp - 25.0%
    SqrtPriceMath.getNextSqrtPriceFromOutput - 0.0%
```