#!/usr/bin/env python3
"""
增强版币安数据获取器
使用真实API密钥获取准确数据
"""

import hmac
import hashlib
import time
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
import json

# 导入配置
from binance_config import BINANCE_CONFIG, SUPPORTED_SYMBOLS

class EnhancedBinanceFetcher:
    """增强版币安数据获取器"""
    
    def __init__(self):
        self.api_key = BINANCE_CONFIG['api_key']
        self.api_secret = BINANCE_CONFIG['api_secret']
        self.base_url = BINANCE_CONFIG['base_url']
        
        # 测试连接
        self.connection_status = self.test_connection()
        
        if self.connection_status:
            print(f"✅ 币安API连接成功")
            print(f"   服务器时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"❌ 币安API连接失败")
    
    def _generate_signature(self, params: Dict[str, Any]) -> str:
        """生成HMAC SHA256签名"""
        query_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None, signed: bool = False) -> Optional[Dict[str, Any]]:
        """发送API请求"""
        try:
            url = f"{self.base_url}{endpoint}"
            headers = {}
            
            if signed:
                if params is None:
                    params = {}
                params['timestamp'] = int(time.time() * 1000)
                params['signature'] = self._generate_signature(params)
                headers['X-MBX-APIKEY'] = self.api_key
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ API请求失败: {response.status_code} - {response.text[:100]}")
                return None
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return None
    
    def test_connection(self) -> bool:
        """测试API连接"""
        try:
            # 测试服务器时间
            response = requests.get(f"{self.base_url}/api/v3/time", timeout=5)
            if response.status_code == 200:
                server_time = response.json().get('serverTime', 0)
                if server_time > 0:
                    print(f"✅ 币安服务器时间: {datetime.fromtimestamp(server_time/1000).strftime('%Y-%m-%d %H:%M:%S')}")
                    return True
            return False
        except Exception as e:
            print(f"❌ 连接测试失败: {e}")
            return False
    
    def get_ticker_price(self, symbol: str) -> Optional[float]:
        """获取单个币种价格"""
        trading_pair = f"{symbol}USDT"
        endpoint = "/api/v3/ticker/price"
        params = {'symbol': trading_pair}
        
        data = self._make_request(endpoint, params)
        if data and 'price' in data:
            return float(data['price'])
        return None
    
    def get_all_prices(self, symbols: List[str]) -> Dict[str, float]:
        """获取所有币种价格"""
        prices = {}
        
        for symbol in symbols:
            price = self.get_ticker_price(symbol)
            if price:
                prices[symbol] = price
            else:
                print(f"⚠️ {symbol}价格获取失败")
        
        return prices
    
    def get_ticker_24hr(self, symbol: str) -> Optional[Dict[str, Any]]:
        """获取24小时数据"""
        trading_pair = f"{symbol}USDT"
        endpoint = "/api/v3/ticker/24hr"
        params = {'symbol': trading_pair}
        
        data = self._make_request(endpoint, params)
        if data:
            return {
                'symbol': data.get('symbol'),
                'price': float(data.get('lastPrice', 0)),
                'price_change': float(data.get('priceChange', 0)),
                'price_change_percent': float(data.get('priceChangePercent', 0)),
                'high_price': float(data.get('highPrice', 0)),
                'low_price': float(data.get('lowPrice', 0)),
                'volume': float(data.get('volume', 0)),
                'quote_volume': float(data.get('quoteVolume', 0)),
                'open_time': data.get('openTime'),
                'close_time': data.get('closeTime')
            }
        return None
    
    def get_all_24hr_data(self, symbols: List[str]) -> Dict[str, Dict[str, Any]]:
        """获取所有币种24小时数据"""
        all_data = {}
        
        for symbol in symbols:
            data = self.get_ticker_24hr(symbol)
            if data:
                all_data[symbol] = data
        
        return all_data
    
    def get_account_info(self) -> Optional[Dict[str, Any]]:
        """获取账户信息（需要签名）"""
        if not self.connection_status:
            return None
        
        endpoint = "/api/v3/account"
        data = self._make_request(endpoint, signed=True)
        return data
    
    def get_market_overview(self) -> Dict[str, Any]:
        """获取市场概况"""
        prices = self.get_all_prices(SUPPORTED_SYMBOLS)
        total_volume = 0
        
        for symbol in SUPPORTED_SYMBOLS:
            data = self.get_ticker_24hr(symbol)
            if data:
                total_volume += data.get('quote_volume', 0)
        
        return {
            'total_symbols': len(prices),
            'total_volume_24h': total_volume,
            'prices': prices,
            'timestamp': datetime.now().isoformat()
        }

def test_enhanced_binance():
    """测试增强版币安数据获取器"""
    print("🧪 测试增强版币安数据获取器...")
    print("=" * 60)
    
    fetcher = EnhancedBinanceFetcher()
    
    if not fetcher.connection_status:
        print("❌ 无法连接币安API，请检查网络或API密钥")
        return False
    
    print("\n📊 获取实时价格...")
    symbols = ['BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'LINK']
    prices = fetcher.get_all_prices(symbols)
    
    for symbol, price in prices.items():
        print(f"   {symbol}: ${price:,.2f}")
    
    print("\n📈 获取24小时数据...")
    btc_data = fetcher.get_ticker_24hr('BTC')
    if btc_data:
        print(f"   BTC 24h变化: {btc_data.get('price_change_percent', 0):+.2f}%")
        print(f"   最高价: ${btc_data.get('high_price', 0):,.2f}")
        print(f"   最低价: ${btc_data.get('low_price', 0):,.2f}")
        print(f"   成交量: ${btc_data.get('quote_volume', 0):,.0f}")
    
    print("\n🌐 获取市场概况...")
    overview = fetcher.get_market_overview()
    print(f"   分析币种: {overview['total_symbols']} 个")
    print(f"   总成交量(24h): ${overview['total_volume_24h']:,.0f}")
    
    print("\n" + "=" * 60)
    print("✅ 增强版币安数据获取器测试完成！")
    return True

if __name__ == "__main__":
    test_enhanced_binance()
