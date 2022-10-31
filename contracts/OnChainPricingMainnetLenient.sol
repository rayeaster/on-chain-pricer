// SPDX-License-Identifier: GPL-2.0
pragma solidity 0.8.10;

import {OnChainPricingMainnet} from "./OnChainPricingMainnet.sol";

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

    /// @dev WP-L2 from watchpug for V4, setting allowed slippage from oracle feed
    function setFeedSlippage(uint256 newSlippage) external {
        require(msg.sender == TECH_OPS, "Only TechOps");
        require(newSlippage < MAX_BPS);
        feed_tolerance = newSlippage;
    }

    // === PRICING === //

    /// @dev apply lenient slippage on top of parent query 
    function findOptimalSwap(address tokenIn, address tokenOut, uint256 amountIn) public view override returns (Quote memory q) {
        q = super.findOptimalSwap(tokenIn, tokenOut, amountIn);		
        if (q.amountOut > 0) {		
            q.amountOut = q.amountOut * (MAX_BPS - slippage) / MAX_BPS;
        }
    }
	
    /// @dev apply lenient slippage on top of parent query 
    function findExecutableSwap(address tokenIn, address tokenOut, uint256 amountIn) public view override returns (Quote memory q) {
        q = super.findExecutableSwap(tokenIn, tokenOut, amountIn);		
        if (q.amountOut > 0) {
            q.amountOut = q.amountOut * (MAX_BPS - slippage) / MAX_BPS;		
        }
    }	


    /// @dev apply lenient slippage on top of parent query 
    function unsafeFindExecutableSwap(address tokenIn, address tokenOut, uint256 amountIn) public view override returns (Quote memory q) {
        q = super.unsafeFindExecutableSwap(tokenIn, tokenOut, amountIn);		
        if (q.amountOut > 0) {
            q.amountOut = q.amountOut * (MAX_BPS - slippage) / MAX_BPS;		
        }
    }
}