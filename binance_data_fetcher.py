#!/usr/bin/env python3
"""
币安实时数据获取模块
使用HMAC签名认证
"""

import hmac
import hashlib
import time
import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from urllib.parse import urlencode

from binance_config import BINANCE_CONFIG, SYMBOLS

class BinanceDataFetcher:
    """币安数据获取器"""
    
    def __init__(self, api_key: str = None, api_secret: str = None):
        self.api_key = api_key or BINANCE_CONFIG['api_key']
        self.api_secret = api_secret or BINANCE_CONFIG['api_secret']
        self.base_url = BINANCE_CONFIG['base_url']
        self.session = requests.Session()
        self.session.headers.update({
            'X-MBX-APIKEY': self.api_key,
            'Content-Type': 'application/json'
        })
        
        # 缓存
        self.cache = {}
        self.cache_time = {}
        self.cache_ttl = 30  # 30秒缓存
        
    def _generate_signature(self, params: Dict[str, Any]) -> str:
        """生成HMAC SHA256签名"""
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None, 
                     signed: bool = False, method: str = 'GET') -> Dict[str, Any]:
        """发送API请求"""
        url = f"{self.base_url}{endpoint}"
        
        if params is None:
            params = {}
        
        # 添加时间戳（如果是签名请求）
        if signed:
            params['timestamp'] = int(time.time() * 1000)
            params['signature'] = self._generate_signature(params)
        
        try:
            if method == 'GET':
                response = self.session.get(url, params=params, timeout=10)
            elif method == 'POST':
                response = self.session.post(url, params=params, timeout=10)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API请求失败: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"   状态码: {e.response.status_code}")
                print(f"   响应: {e.response.text[:200]}")
            return {'error': str(e)}
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            return {'error': 'JSON解析失败'}
    
    def get_ticker_price(self, symbol: str) -> Optional[float]:
        """获取单个币种价格"""
        cache_key = f"price_{symbol}"
        
        # 检查缓存
        if cache_key in self.cache:
            cache_time = self.cache_time.get(cache_key)
            if cache_time and (datetime.now() - cache_time).seconds < self.cache_ttl:
                return self.cache[cache_key]
        
        endpoint = '/api/v3/ticker/price'
        params = {'symbol': SYMBOLS.get(symbol, f"{symbol}USDT")}
        
        result = self._make_request(endpoint, params)
        
        if 'price' in result:
            price = float(result['price'])
            self.cache[cache_key] = price
            self.cache_time[cache_key] = datetime.now()
            return price
        else:
            print(f"❌ 获取{symbol}价格失败: {result.get('msg', '未知错误')}")
            return None
    
    def get_ticker_24hr(self, symbol: str) -> Dict[str, Any]:
        """获取24小时行情数据"""
        cache_key = f"24hr_{symbol}"
        
        # 检查缓存
        if cache_key in self.cache:
            cache_time = self.cache_time.get(cache_key)
            if cache_time and (datetime.now() - cache_time).seconds < self.cache_ttl:
                return self.cache[cache_key]
        
        endpoint = '/api/v3/ticker/24hr'
        params = {'symbol': SYMBOLS.get(symbol, f"{symbol}USDT")}
        
        result = self._make_request(endpoint, params)
        
        if 'lastPrice' in result:
            data = {
                'price': float(result['lastPrice']),
                'price_change': float(result['priceChange']),
                'price_change_percent': float(result['priceChangePercent']),
                'high_price': float(result['highPrice']),
                'low_price': float(result['lowPrice']),
                'volume': float(result['volume']),
                'quote_volume': float(result['quoteVolume']),
                'open_time': datetime.fromtimestamp(result['openTime'] / 1000),
                'close_time': datetime.fromtimestamp(result['closeTime'] / 1000)
            }
            self.cache[cache_key] = data
            self.cache_time[cache_key] = datetime.now()
            return data
        else:
            print(f"❌ 获取{symbol}24小时数据失败: {result.get('msg', '未知错误')}")
            return {}
    
    def get_klines(self, symbol: str, interval: str = '1h', limit: int = 100) -> List[Dict[str, Any]]:
        """获取K线数据"""
        cache_key = f"klines_{symbol}_{interval}_{limit}"
        
        # 检查缓存
        if cache_key in self.cache:
            cache_time = self.cache_time.get(cache_key)
            if cache_time and (datetime.now() - cache_time).seconds < 300:  # 5分钟缓存
                return self.cache[cache_key]
        
        endpoint = '/api/v3/klines'
        params = {
            'symbol': SYMBOLS.get(symbol, f"{symbol}USDT"),
            'interval': interval,
            'limit': limit
        }
        
        result = self._make_request(endpoint, params)
        
        if isinstance(result, list):
            klines = []
            for kline in result:
                klines.append({
                    'open_time': datetime.fromtimestamp(kline[0] / 1000),
                    'open': float(kline[1]),
                    'high': float(kline[2]),
                    'low': float(kline[3]),
                    'close': float(kline[4]),
                    'volume': float(kline[5]),
                    'close_time': datetime.fromtimestamp(kline[6] / 1000),
                    'quote_volume': float(kline[7]),
                    'trades': int(kline[8]),
                    'taker_buy_base': float(kline[9]),
                    'taker_buy_quote': float(kline[10])
                })
            
            self.cache[cache_key] = klines
            self.cache_time[cache_key] = datetime.now()
            return klines
        else:
            print(f"❌ 获取{symbol}K线数据失败: {result.get('msg', '未知错误')}")
            return []
    
    def get_order_book(self, symbol: str, limit: int = 10) -> Dict[str, Any]:
        """获取订单簿数据"""
        endpoint = '/api/v3/depth'
        params = {
            'symbol': SYMBOLS.get(symbol, f"{symbol}USDT"),
            'limit': limit
        }
        
        result = self._make_request(endpoint, params)
        
        if 'bids' in result and 'asks' in result:
            return {
                'bids': [(float(price), float(quantity)) for price, quantity in result['bids'][:limit]],
                'asks': [(float(price), float(quantity)) for price, quantity in result['asks'][:limit]],
                'last_update_id': result['lastUpdateId']
            }
        else:
            print(f"❌ 获取{symbol}订单簿失败: {result.get('msg', '未知错误')}")
            return {'bids': [], 'asks': []}
    
    def get_account_info(self) -> Dict[str, Any]:
        """获取账户信息（需要签名）"""
        endpoint = '/api/v3/account'
        params = {}
        
        result = self._make_request(endpoint, params, signed=True)
        
        if 'balances' in result:
            return {
                'maker_commission': result['makerCommission'],
                'taker_commission': result['takerCommission'],
                'buyer_commission': result['buyerCommission'],
                'seller_commission': result['sellerCommission'],
                'can_trade': result['canTrade'],
                'can_withdraw': result['canWithdraw'],
                'can_deposit': result['canDeposit'],
                'update_time': datetime.fromtimestamp(result['updateTime'] / 1000),
                'balances': [
                    {
                        'asset': balance['asset'],
                        'free': float(balance['free']),
                        'locked': float(balance['locked'])
                    }
                    for balance in result['balances']
                    if float(balance['free']) > 0 or float(balance['locked']) > 0
                ]
            }
        else:
            print(f"❌ 获取账户信息失败: {result.get('msg', '未知错误')}")
            return {}
    
    def get_all_prices(self, symbols: List[str] = None) -> Dict[str, float]:
        """获取所有币种价格"""
        if symbols is None:
            symbols = list(SYMBOLS.keys())
        
        prices = {}
        for symbol in symbols:
            price = self.get_ticker_price(symbol)
            if price is not None:
                prices[symbol] = price
            else:
                prices[symbol] = 0.0
        
        return prices
    
    def get_all_24hr_data(self, symbols: List[str] = None) -> Dict[str, Dict[str, Any]]:
        """获取所有币种24小时数据"""
        if symbols is None:
            symbols = list(SYMBOLS.keys())
        
        data = {}
        for symbol in symbols:
            ticker_data = self.get_ticker_24hr(symbol)
            if ticker_data:
                data[symbol] = ticker_data
        
        return data
    
    def calculate_technical_indicators(self, symbol: str) -> Dict[str, Any]:
        """计算技术指标"""
        klines = self.get_klines(symbol, '1h', 100)
        
        if not klines:
            return {}
        
        closes = [kline['close'] for kline in klines]
        volumes = [kline['volume'] for kline in klines]
        
        # 计算简单移动平均
        def sma(data, period):
            if len(data) < period:
                return None
            return sum(data[-period:]) / period
        
        # 计算指数移动平均
        def ema(data, period):
            if len(data) < period:
                return None
            multiplier = 2 / (period + 1)
            ema_value = sma(data[:period], period)
            for price in data[period:]:
                ema_value = (price - ema_value) * multiplier + ema_value
            return ema_value
        
        # 计算MACD
        ema12 = ema(closes, 12)
        ema26 = ema(closes, 26)
        macd_line = ema12 - ema26 if ema12 and ema26 else None
        signal_line = ema([macd_line] if macd_line else closes, 9) if macd_line else None
        histogram = macd_line - signal_line if macd_line and signal_line else None
        
        # 计算RSI
        def rsi(data, period=14):
            if len(data) < period + 1:
                return None
            
            gains = []
            losses = []
            
            for i in range(1, len(data)):
                change = data[i] - data[i-1]
                if change > 0:
                    gains.append(change)
                    losses.append(0)
                else:
                    gains.append(0)
                    losses.append(abs(change))
            
            avg_gain = sum(gains[-period:]) / period
            avg_loss = sum(losses[-period:]) / period
            
            if avg_loss == 0:
                return 100
            
            rs = avg_gain / avg_loss
            return 100 - (100 / (1 + rs))
        
        # 计算布林带
        def bollinger_bands(data, period=20, std=2):
            if len(data) < period:
                return None, None, None
            
            middle = sma(data[-period:], period)
            std_dev = (sum((x - middle) ** 2 for x in data[-period:]) / period) ** 0.5
            upper = middle + (std_dev * std)
            lower = middle - (std_dev * std)
            
            return upper, middle, lower
        
        rsi_value = rsi(closes)
        upper_bb, middle_bb, lower_bb = bollinger_bands(closes)
        
        return {
            'macd': {
                'macd_line': macd_line,
                'signal_line': signal_line,
                'histogram': histogram,
                'signal': '金叉' if macd_line and signal_line and macd_line > signal_line else '死叉' if macd_line and signal_line else '盘整'
            },
            'rsi': rsi_value,
            'bollinger_bands': {
                'upper': upper_bb,
                'middle': middle_bb,
                'lower': lower_bb,
                'position': ((closes[-1] - lower_bb) / (upper_bb - lower_bb) * 100) if upper_bb and lower_bb and upper_bb != lower_bb else None
            },
            'sma_20': sma(closes, 20),
            'sma_50': sma(closes, 50),
            'sma_200': sma(closes, 200),
            'volume_sma': sma(volumes, 20) if len(volumes) >= 20 else None
        }
    
    def test_connection(self) -> bool:
        """测试API连接"""
        try:
            # 测试获取服务器时间
            endpoint = '/api/v3/time'
            result = self._make_request(endpoint)
            
            if 'serverTime' in result:
                print(f"✅ 币安API连接成功")
                print(f"   服务器时间: {datetime.fromtimestamp(result['serverTime'] / 1000)}")
                return True
            else:
                print(f"❌ API连接测试失败: {result}")
                return False
                
        except Exception as e:
            print(f"❌ API连接异常: {e}")
            return False
    
    def get_market_overview(self) -> Dict[str, Any]:
        """获取市场概况"""
        symbols = list(SYMBOLS.keys())
        
        prices = self.get_all_prices(symbols)
        ticker_data = self.get_all_24hr_data(symbols)
        
        total_volume = 0
        total_market_cap = 0
        
        for symbol, data in ticker_data.items():
            if data:
                total_volume += data.get('quote_volume', 0)
                # 简单估算市值（实际需要流通量数据）
                total_market_cap += data.get('price', 0) * 1000000  # 假设每个币种100万流通
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_symbols': len(symbols),
            'prices': prices,
            'total_volume_24h': total_volume,
            'estimated_market_cap': total_market_cap,
            'symbols_data': ticker_data
        }

def test_binance_integration():
    """测试币安集成"""
    print("🧪 测试币安API集成...")
    print("=" * 50)
    
    # 创建数据获取器
    fetcher = BinanceDataFetcher()
    
    # 测试连接
    if not fetcher.test_connection():
        print("❌ API连接失败，请检查配置")
        return False
    
    # 测试获取价格
    print("\n📊 测试获取实时价格...")
    symbols = ['BTC', 'ETH', 'BNB', 'XRP', 'SOL', 'LINK']
    
    for symbol in symbols:
        price = fetcher.get_ticker_price(symbol)
        if price:
            print(f"   {symbol}: ${price:,.2f}")
        else:
            print(f"   {symbol}: ❌ 获取失败")
    
    # 测试获取24小时数据
    print("\n📈 测试获取24小时数据...")
    btc_data = fetcher.get_ticker_24hr('BTC')
    if btc_data:
        print(f"   BTC 24h变化: {btc_data.get('price_change_percent', 0):+.2f}%")
        print(f"   最高价: ${btc_data.get('high_price', 0):,.2f}")
        print(f"   最低价: ${btc_data.get('low_price', 0):,.2f}")
        print(f"   成交量: ${btc_data.get('quote_volume', 0):,.0f}")
    
    # 测试技术指标计算
    print("\n📊 测试技术指标计算...")
    btc_indicators = fetcher.calculate_technical_indicators('BTC')
    if btc_indicators:
        print(f"   MACD信号: {btc_indicators['macd']['signal']}")
        print(f"   RSI: {btc_indicators.get('rsi', 'N/A'):.1f}")
        if btc_indicators['bollinger_bands']['position']:
            print(f"   布林带位置: {btc_indicators['bollinger_bands']['position']:.1f}%")
    
    # 测试市场概况
    print("\n🌐 测试市场概况...")
    overview = fetcher.get_market_overview()
    print(f"   分析币种: {overview['total_symbols']} 个")
    print(f"   总成交量(24h): ${overview['total_volume_24h']:,.0f}")
    
    print("\n" + "=" * 50)
    print("✅ 币安API集成测试完成！")
    return True

if __name__ == "__main__":
    test_binance_integration()
