pragma solidity 0.8.10;
pragma experimental ABIEncoderV2;

enum SwapType { 
   CURVE, //0
   UNIV2, //1
   SUSHI, //2
   UNIV3, //3
   UNIV3WITHWETH, //4 
   BALANCER, //5
   BALANCERWITHWETH, //6
   PRICEFEED  //7 	
}

// Onchain Pricing Interface
struct Quote {
   SwapType name;
   uint256 amountOut;
   bytes32[] pools; // specific pools involved in the optimal swap path
   uint256[] poolFees; // specific pool fees involved in the optimal swap path, typically in Uniswap V3
}
interface OnChainPricing {
   function isPairSupported(address tokenIn, address tokenOut, uint256 amountIn) external view returns (bool);
   function findOptimalSwap(address tokenIn, address tokenOut, uint256 amountIn) external view returns (Quote memory);
   function unsafeFindExecutableSwap(address tokenIn, address tokenOut, uint256 amountIn) external view virtual returns (Quote memory q);
   function checkUniV3InRangeLiquidity(address token0, address token1, uint256 amountIn, uint24 _fee, bool token0Price, address _pool) external view returns (bool, uint256);
   function simulateUniV3Swap(address token0, uint256 amountIn, address token1, uint24 _fee, bool token0Price, address _pool) external view returns (uint256);
   function tryQuoteWithFeed(address tokenIn, address tokenOut, uint256 amountIn) external view returns (uint256);
}
// END OnchainPricing

contract PricerWrapper {
   address public pricer;
   constructor(address _pricer) {
      pricer = _pricer;
   }
	
   function isPairSupported(address tokenIn, address tokenOut, uint256 amountIn) external view returns (bool) {
      return OnChainPricing(pricer).isPairSupported(tokenIn, tokenOut, amountIn);
   }
   
   /// @dev mainly for gas profiling test
   function findOptimalSwapNonView(address tokenIn, address tokenOut, uint256 amountIn) external returns (Quote memory) {
      return OnChainPricing(pricer).findOptimalSwap(tokenIn, tokenOut, amountIn);
   }

   function findOptimalSwap(address tokenIn, address tokenOut, uint256 amountIn) external view returns (uint256, Quote memory) {
      uint256 _gasBefore = gasleft();
      Quote memory q = OnChainPricing(pricer).findOptimalSwap(tokenIn, tokenOut, amountIn);
      return (_gasBefore - gasleft(), q);
   }

   function unsafeFindExecutableSwap(address tokenIn, address tokenOut, uint256 amountIn) external view returns (uint256, Quote memory) {
      uint256 _gasBefore = gasleft();
      Quote memory q = OnChainPricing(pricer).unsafeFindExecutableSwap(tokenIn, tokenOut, amountIn);
      return (_gasBefore - gasleft(), q);
   }
   
   function checkUniV3InRangeLiquidity(address token0, address token1, uint256 amountIn, uint24 _fee, bool token0Price, address _pool) public view returns (uint256, bool, uint256){
      uint256 _gasBefore = gasleft();
      (bool _crossTicks, uint256 _inRangeSimOut) = OnChainPricing(pricer).checkUniV3InRangeLiquidity(token0, token1, amountIn, _fee, token0Price, _pool);
      return (_gasBefore - gasleft(), _crossTicks, _inRangeSimOut);
   }
   
   function simulateUniV3Swap(address token0, uint256 amountIn, address token1, uint24 _fee, bool token0Price, address _pool) public view returns (uint256, uint256){
      uint256 _gasBefore = gasleft();
      uint256 _simOut = OnChainPricing(pricer).simulateUniV3Swap(token0, amountIn, token1, _fee, token0Price, _pool);
      return (_gasBefore - gasleft(), _simOut);
   }
   
   /// @dev mainly for gas profiling
   function tryQuoteWithFeedNonView(address tokenIn, address tokenOut, uint256 amountIn) public returns (uint256, uint256){
      uint256 _gasBefore = gasleft();
      uint256 _qFeed = OnChainPricing(pricer).tryQuoteWithFeed(tokenIn, tokenOut, amountIn);
      return (_gasBefore - gasleft(), _qFeed);
   }
}