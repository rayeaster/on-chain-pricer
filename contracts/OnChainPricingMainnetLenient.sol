// SPDX-License-Identifier: GPL-2.0
pragma solidity 0.8.10;


import {IERC20} from "@oz/token/ERC20/IERC20.sol";
import {ERC20} from "@oz/token/ERC20/ERC20.sol";
import {SafeERC20} from "@oz/token/ERC20/utils/SafeERC20.sol";

import "@chainlink/src/v0.8/interfaces/FeedRegistryInterface.sol";
import "@chainlink/src/v0.8/Denominations.sol";


import "../interfaces/uniswap/IUniswapRouterV2.sol";
import "../interfaces/curve/ICurveRouter.sol";

import {OnChainPricingMainnet, SwapType} from "./OnChainPricingMainnet.sol";



/// @title OnChainPricing
/// @author Alex the Entreprenerd @ BadgerDAO
/// @dev Mainnet Version of Price Quoter, hardcoded for more efficiency
/// @notice To spin a variant, just change the constants and use the Component Functions at the end of the file
/// @notice Instead of upgrading in the future, just point to a new implementation
/// @notice This version has 5% extra slippage to allow further flexibility
///     if the manager abuses the check you should consider reverting back to a more rigorous pricer
contract OnChainPricingMainnetLenient is OnChainPricingMainnet {

    // === SLIPPAGE === //
    // Can change slippage within rational limits
    address public constant TECH_OPS = 0x86cbD0ce0c087b482782c181dA8d191De18C8275;
	
    /// @dev https://docs.chain.link/docs/feed-registry/
    address public constant FEED_REGISTRY = 0x47Fb2585D2C56Fe188D0E6ec628a38b74fCeeeDf;
    
    uint256 private constant MAX_BPS = 10_000;

    uint256 private constant MAX_SLIPPAGE = 500; // 5%

    uint256 public slippage = 200; // 2% Initially
    uint256 private constant SECONDS_PER_HOUR = 3600;
    uint256 private constant SECONDS_PER_DAY = 86400;

    constructor(
        address _uniV3Simulator, 
        address _balancerV2Simulator
    ) OnChainPricingMainnet(_uniV3Simulator, _balancerV2Simulator){
        // Silence is golden
    }

    function setSlippage(uint256 newSlippage) external {
        require(msg.sender == TECH_OPS, "Only TechOps");
        require(newSlippage < MAX_SLIPPAGE);
        slippage = newSlippage;
    }

    // === PRICING === //

    /// @dev View function to provide quote (maybe not EXECUTABLE) from tokenIn to tokenOut with given amountIn
    /// @dev Priority to use Price Feeds directly, skip query to various on-chain dex sources if price feed is available
    function findOptimalSwap(address tokenIn, address tokenOut, uint256 amountIn) external view override returns (Quote memory q) {
        uint256 _qFeed = tryQuoteWithFeed(tokenIn, tokenOut, amountIn);
		
        if (_qFeed == 0) {		
            q = _findOptimalSwap(tokenIn, tokenOut, amountIn);
        } else { 
            bytes32[] memory dummyPools;
            uint256[] memory dummyPoolFees;
            q = Quote(SwapType.PRICEFEED, _qFeed, dummyPools, dummyPoolFees);
        }
		
        q.amountOut = q.amountOut * (MAX_BPS - slippage) / MAX_BPS;
    }	

    /// @dev View function to provide EXECUTABLE quote from tokenIn to tokenOut with given amountIn
    /// @dev This function will use Price Feeds to confirm the quote from on-chain dex source is within acceptable slippage-range
    /// @dev a valid quote from on-chain dex source will return or 0 if it is just not "good enough" compared to oracle feed
    function findExecutableSwap(address tokenIn, address tokenOut, uint256 amountIn) external view returns (Quote memory q) {
        uint256 _qFeed = tryQuoteWithFeed(tokenIn, tokenOut, amountIn);
        q = _findOptimalSwap(tokenIn, tokenOut, amountIn);
		
        if (q.amountOut < (_qFeed * (MAX_BPS - slippage) / MAX_BPS)) {
            q.amountOut = 0;
        } else {
            q.amountOut = q.amountOut * (MAX_BPS - slippage) / MAX_BPS;		
        }
    }	

    /// @dev View function to provide EXECUTABLE quote from tokenIn to tokenOut with given amountIn
    /// @dev This function will use directly the quote from on-chain dex source no matter how poorly bad (e.g., illiquid pair) it might be
    function unsafeFindExecutableSwap(address tokenIn, address tokenOut, uint256 amountIn) external view returns (Quote memory q) {
        q = _findOptimalSwap(tokenIn, tokenOut, amountIn);		
        if (q.amountOut > 0) {
            q.amountOut = q.amountOut * (MAX_BPS - slippage) / MAX_BPS;		
        }
    }

    // === ORACLE VIEW FUNCTIONS === //
	
    /// @dev try to convert from tokenIn to tokenOut using price feeds directly: (quote = amountIn * feedPricing)
    function tryQuoteWithFeed(address tokenIn, address tokenOut, uint256 amountIn) public view returns (uint256){		
        uint256 _inDecimals = 10 ** ERC20(tokenIn).decimals();
        uint256 _outDecimals = 10 ** ERC20(tokenOut).decimals();		
				
        // try short-circuit to ETH feeds if possible
        if (tokenIn == WETH){
            uint256 pOutETH = getPriceInETH(tokenOut);
            if (pOutETH > 0){
                return (amountIn * 1e18 / pOutETH) * _outDecimals / _inDecimals;			
            }
        } else if (tokenOut == WETH) {
            uint256 pInETH = getPriceInETH(tokenIn);
            if (pInETH > 0){
                return (amountIn * pInETH / 1e18) * _outDecimals / _inDecimals;			
            }	
        }
        
        // fall-back to USD feeds as last resort
        uint256 pInUSD = fetchUSDFeed(tokenIn);
        if (pInUSD == 0) {
            return 0;		
        }
        uint256 pOutUSD = fetchUSDFeed(tokenOut);
        if (pOutUSD == 0) {
            return 0;		
        }
		
        return (amountIn * pInUSD / pOutUSD) * _outDecimals / _inDecimals;		
    }
	
    /// @dev try to find USD price for given token from feed
    /// @return USD feed value scaled by 10^8 or 0 if no valid USD/ETH/BTC feed exist 
    function fetchUSDFeed(address base) public view returns (uint256) {
        uint256 pUSD = base == WETH? getEthUsdPrice() : getPriceInUSD(base);
        if (pUSD == 0) {
            uint256 pETH = getPriceInETH(base);
            if (pETH > 0) {
                pUSD = pETH * getEthUsdPrice() / 1e18;
            } else {			    
                uint256 pBTC = getPriceInBTC(base);
                if (pBTC > 0){
                    pUSD = pBTC * getBtcUsdPrice() / 1e8;				
                }
            }
        }
        return pUSD;
    }
	
    /// @dev Returns the price of ETH in USD from feed registry
    /// @return price value scaled by 10^8
    function getEthUsdPrice() public view returns (uint256) {
        (uint80 roundID, int price, uint startedAt, uint timeStamp, uint80 answeredInRound) = FeedRegistryInterface(FEED_REGISTRY).latestRoundData(Denominations.ETH, Denominations.USD);
        require(block.timestamp - timeStamp <= SECONDS_PER_HOUR, '!stale'); // Check for freshness of feed
        return uint256(price);
    }
	
    /// @dev Returns the price of BTC in USD from feed registry
    /// @return price value scaled by 10^8
    function getBtcUsdPrice() public view returns (uint256) {
        (uint80 roundID, int price, uint startedAt, uint timeStamp, uint80 answeredInRound) = FeedRegistryInterface(FEED_REGISTRY).latestRoundData(Denominations.BTC, Denominations.USD);
        require(block.timestamp - timeStamp <= SECONDS_PER_HOUR, '!stale'); // Check for freshness of feed
        return uint256(price);
    }

    /// @dev Returns the latest price of given base token in USD
    /// @return price value scaled by 10^8 or 0 if no valid price feed is found
    function getPriceInUSD(address base) public view returns (uint256) {
        try FeedRegistryInterface(FEED_REGISTRY).latestRoundData(base, Denominations.USD) returns (uint80 roundID, int price, uint startedAt, uint timeStamp, uint80 answeredInRound) {	
            require(block.timestamp - timeStamp <= SECONDS_PER_DAY, '!stale'); // Check for freshness of feed	
            return uint256(price);
        } catch {		
            return 0;
        }
    }

    /// @dev Returns the latest price of given base token in ETH
    /// @return price value scaled by 10^18 or 0 if no valid price feed is found
    function getPriceInETH(address base) public view returns (uint256) {
        try FeedRegistryInterface(FEED_REGISTRY).latestRoundData(base, Denominations.ETH) returns (uint80 roundID, int price, uint startedAt, uint timeStamp, uint80 answeredInRound) {
            require(block.timestamp - timeStamp <= SECONDS_PER_DAY, '!stale'); // Check for freshness of feed		
            return uint256(price);
        } catch {		
            return 0;
        }
    }

    /// @dev Returns the latest price of given base token in BTC (typically for WBTC)
    /// @return price value scaled by 10^8 or 0 if no valid price feed is found
    function getPriceInBTC(address base) public view returns (uint256) {
        try FeedRegistryInterface(FEED_REGISTRY).latestRoundData(base, Denominations.BTC) returns (uint80 roundID, int price, uint startedAt, uint timeStamp, uint80 answeredInRound) {	
            require(block.timestamp - timeStamp <= SECONDS_PER_DAY, '!stale'); // Check for freshness of feed
            return uint256(price);
        } catch {		
            return 0;
        }
    }
}