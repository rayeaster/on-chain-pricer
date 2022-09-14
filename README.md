# Fair Selling

## WARNING

⚠️⚠️⚠️ V4 functions do not revert on error, they return 0 ⚠️⚠️⚠️

A 0 may mean the function call will revert or that there is no liquidity available

For all intents and purposes, check if a quote returns 0 and if it does, do not execute it or expect a revert


-----

A [BadgerDAO](https://app.badger.com/) sponsored repo of Open Source Contracts for:

- Calculating onChain Prices
- Executing the best onChain Swap

## Why bother

We understand that we cannot prove a optimal price because at any time a new source of liquidity may be available and the contract cannot adapt.

However we believe that given a set of constraints (available Dexes, handpicked), we can efficiently compute the best trade available to us

In exploring this issue we aim to:
- Find the most gas-efficient way to get the best executable price (currently 120 /150k per quote, from 1.6MLN)
- Finding the most reliable price we can, to determine if an offer is fair or unfair (Cowswap integration)
- Can we create a "trustless swap" that is provably not frontrun nor manipulated?
- How would such a "self-defending" contract act and how would it be able to defend itself, get the best quote, and be certain of it (with statistical certainty)

## Current Release V0.4 - Pricer

# Notable Contracts

## OnChainPricingMainnet

Given a tokenIn, tokenOut and AmountIn, returns a Quote from the most popular dexes

- `OnChainPricingMainnet` -> Fully onChain math to find best, single source swap (no fragmented swaps yet)
- `OnChainPricingMainnetLenient` -> Slippage tollerant version of the Pricer

### Dexes Support
- Curve
- UniV2
- UniV3
- Balancer
- Sushi

Covering >80% TVL on Mainnet. (Prob even more)

### New with V4

V4 adds support for Chainlink Price Feeds, all feeds are supported via the Feeds Registry

Because V4 marks the separation between "executable prices" and "ideal prices" we added new functions.

Read below for full details

## Example Usage

V4 functions are `view`

!!! V4 functions do not revert on error, they return 0 !!!
### isPairSupported

Returns true if the pricer will return a non-zero quote
NOTE: This is not proof of optimality

```solidity
    /// @dev Given tokenIn, out and amountIn, returns true if a quote will be non-zero
    /// @notice Doesn't guarantee optimality, just non-zero
    function isPairSupported(address tokenIn, address tokenOut, uint256 amountIn) external returns (bool)
```

In Brownie
```python
quote = pricer.isPairSupported(t_in, t_out, amt_in)
```

### findOptimalSwap

Finds the best quote available between the sources
Prioritizes price feeds


```solidity
    function findOptimalSwap(address tokenIn, address tokenOut, uint256 amountIn) external virtual returns (Quote memory)
```

In Brownie
```python
quote = pricer.findOptimalSwap(t_in, t_out, amt_in)
```

### findExecutableSwap

Finds the best executable quote
Uses PriceFeeds (if available) to verify the quote is better than the feed

```solidity
    function findExecutableSwap(address tokenIn, address tokenOut, uint256 amountIn) external virtual returns (Quote memory)
```

In Brownie
```python
quote = pricer.findExecutableSwap(t_in, t_out, amt_in)
```


### unsafeFindExecutableSwap

Finds the best executable quote
Doesn't check price feeds, use at your own risk

```solidity
    function unsafeFindExecutableSwap(address tokenIn, address tokenOut, uint256 amountIn) external virtual returns (Quote memory)
```

In Brownie
```python
quote = pricer.unsafeFindExecutableSwap(t_in, t_out, amt_in)
```

# Mainnet Pricing Lenient

Variation of Pricer with a slippage tollerance, mostly used to allow a multisig enough wiggle room for operation



# Notable Tests

## Proof that the math is accurate with gas savings

These tests compare the PricerV3 (150k per quote) against V2 (1.6MLN per quote)

```
brownie test tests/heuristic_equivalency/test_heuristic_equivalency.py

```

## Benchmark specific AMM quotes
TODO: Improve to just use the specific quote

```
brownie test tests/gas_benchmark/benchmark_pricer_gas.py --gas
```

## Benchmark coverage of top DeFi Tokens

TODO: Add like 200 tokens
TODO: Compare against Coingecko API or smth

```
brownie test tests/gas_benchmark/benchmark_token_coverage.py --gas
```

## Notable Test from V2

Run V3 Pricer against V2, to confirm results are correct, but with gas savings

```
brownie test  tests/heuristic_equivalency/test_heuristic_equivalency.py
