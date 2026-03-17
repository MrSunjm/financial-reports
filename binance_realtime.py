#!/usr/bin/env python3
"""
币安实时数据获取模块
直接从币安API获取实时市场价格数据
"""

import requests
import json
import time
from datetime import datetime
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BinanceRealtimeData:
    """币安实时数据获取类"""
    
    def __init__(self):
        self.base_url = "https://api.binance.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        })
        
    def get_ticker_price(self, symbol):
        """获取单个币种价格"""
        try:
            url = f"{self.base_url}/api/v3/ticker/price"
            params = {'symbol': f"{symbol.upper()}USDT"}
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            price = float(data['price'])
            
            logger.info(f"获取 {symbol} 价格成功: ${price:,.2f}")
            return {
                'symbol': symbol.upper(),
                'price': price,
                'timestamp': datetime.now().isoformat(),
                'source': 'binance',
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"获取 {symbol} 价格失败: {str(e)}")
            return {
                'symbol': symbol.upper(),
                'price': None,
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'source': 'binance',
                'status': 'error'
            }
    
    def get_multiple_prices(self, symbols):
        """获取多个币种价格"""
        results = {}
        for symbol in symbols:
            result = self.get_ticker_price(symbol)
            results[symbol.upper()] = result
            
            # 避免请求过快
            time.sleep(0.1)
        
        return results
    
    def get_24h_ticker(self, symbol):
        """获取24小时行情数据"""
        try:
            url = f"{self.base_url}/api/v3/ticker/24hr"
            params = {'symbol': f"{symbol.upper()}USDT"}
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'symbol': symbol.upper(),
                'price': float(data['lastPrice']),
                'price_change': float(data['priceChange']),
                'price_change_percent': float(data['priceChangePercent']),
                'high_price': float(data['highPrice']),
                'low_price': float(data['lowPrice']),
                'volume': float(data['volume']),
                'quote_volume': float(data['quoteVolume']),
                'timestamp': datetime.now().isoformat(),
                'source': 'binance'
            }
            
        except Exception as e:
            logger.error(f"获取 {symbol} 24h数据失败: {str(e)}")
            return None
    
    def get_klines(self, symbol, interval='1h', limit=24):
        """获取K线数据"""
        try:
            url = f"{self.base_url}/api/v3/klines"
            params = {
                'symbol': f"{symbol.upper()}USDT",
                'interval': interval,
                'limit': limit
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            klines = response.json()
            
            # 解析K线数据
            parsed_klines = []
            for kline in klines:
                parsed_klines.append({
                    'timestamp': kline[0],
                    'open': float(kline[1]),
                    'high': float(kline[2]),
                    'low': float(kline[3]),
                    'close': float(kline[4]),
                    'volume': float(kline[5])
                })
            
            return parsed_klines
            
        except Exception as e:
            logger.error(f"获取 {symbol} K线数据失败: {str(e)}")
            return None
    
    def get_order_book(self, symbol, limit=10):
        """获取订单簿数据"""
        try:
            url = f"{self.base_url}/api/v3/depth"
            params = {
                'symbol': f"{symbol.upper()}USDT",
                'limit': limit
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            order_book = response.json()
            
            return {
                'symbol': symbol.upper(),
                'bids': order_book['bids'][:limit],  # 买盘
                'asks': order_book['asks'][:limit],  # 卖盘
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"获取 {symbol} 订单簿失败: {str(e)}")
            return None

# 测试函数
def test_binance_api():
    """测试币安API"""
    print("🧪 测试币安实时数据API")
    print("=" * 50)
    
    binance = BinanceRealtimeData()
    
    # 测试获取BTC价格
    print("1. 测试获取BTC实时价格...")
    btc_data = binance.get_ticker_price('BTC')
    if btc_data['status'] == 'success':
        print(f"   ✅ BTC价格: ${btc_data['price']:,.2f}")
        print(f"   时间: {btc_data['timestamp']}")
    else:
        print(f"   ❌ 失败: {btc_data.get('error', '未知错误')}")
    
    # 测试获取XRP价格
    print("\n2. 测试获取XRP实时价格...")
    xrp_data = binance.get_ticker_price('XRP')
    if xrp_data['status'] == 'success':
        print(f"   ✅ XRP价格: ${xrp_data['price']:,.2f}")
        print(f"   时间: {xrp_data['timestamp']}")
    else:
        print(f"   ❌ 失败: {xrp_data.get('error', '未知错误')}")
    
    # 测试获取多个币种
    print("\n3. 测试获取多个币种价格...")
    symbols = ['BTC', 'ETH', 'BNB', 'XRP', 'SOL', 'LINK']
    multi_data = binance.get_multiple_prices(symbols)
    
    for symbol, data in multi_data.items():
        if data['status'] == 'success':
            print(f"   ✅ {symbol}: ${data['price']:,.2f}")
        else:
            print(f"   ❌ {symbol}: 获取失败")
    
    # 测试24小时数据
    print("\n4. 测试获取BTC 24小时数据...")
    btc_24h = binance.get_24h_ticker('BTC')
    if btc_24h:
        print(f"   ✅ 当前价格: ${btc_24h['price']:,.2f}")
        print(f"   24h变化: {btc_24h['price_change_percent']:.2f}%")
        print(f"   最高价: ${btc_24h['high_price']:,.2f}")
        print(f"   最低价: ${btc_24h['low_price']:,.2f}")
        print(f"   成交量: {btc_24h['volume']:,.0f} BTC")
    
    print("\n" + "=" * 50)
    print("🎯 测试完成！")
    
    # 返回测试结果
    return {
        'btc': btc_data,
        'xrp': xrp_data,
        'multi': multi_data,
        'btc_24h': btc_24h
    }

if __name__ == "__main__":
    test_binance_api()
