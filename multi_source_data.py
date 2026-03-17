#!/usr/bin/env python3
"""
多数据源加密货币数据获取系统
支持多个数据源，自动选择可用的源
"""

import requests
import json
import time
from datetime import datetime, timedelta
import logging
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CryptoDataFetcher:
    """加密货币数据获取器（多数据源）"""
    
    def __init__(self):
        self.data_sources = [
            {
                'name': 'CoinGecko',
                'function': self._fetch_coingecko,
                'priority': 1,
                'cache_ttl': 60  # 缓存60秒
            },
            {
                'name': 'Binance',
                'function': self._fetch_binance,
                'priority': 2,
                'cache_ttl': 30  # 缓存30秒
            },
            {
                'name': 'CryptoCompare',
                'function': self._fetch_cryptocompare,
                'priority': 3,
                'cache_ttl': 120  # 缓存120秒
            }
        ]
        
        self.cache = {}
        self.last_fetch_time = {}
    
    def _fetch_coingecko(self, symbols: list) -> Dict[str, Any]:
        """从CoinGecko获取数据"""
        try:
            # 映射币种名称
            symbol_map = {
                'BTC': 'bitcoin',
                'ETH': 'ethereum',
                'BNB': 'binancecoin',
                'XRP': 'ripple',
                'SOL': 'solana',
                'LINK': 'chainlink'
            }
            
            coin_ids = []
            for symbol in symbols:
                if symbol in symbol_map:
                    coin_ids.append(symbol_map[symbol])
            
            if not coin_ids:
                return {'status': 'error', 'error': '无支持的币种'}
            
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                'ids': ','.join(coin_ids),
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_market_cap': 'true',
                'include_24hr_vol': 'true'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # 转换格式
            result = {}
            for symbol, coin_id in symbol_map.items():
                if coin_id in data and symbol in symbols:
                    coin_data = data[coin_id]
                    result[symbol] = {
                        'price': coin_data.get('usd'),
                        'change_24h': coin_data.get('usd_24h_change'),
                        'market_cap': coin_data.get('usd_market_cap'),
                        'volume_24h': coin_data.get('usd_24h_vol'),
                        'source': 'CoinGecko',
                        'timestamp': datetime.now().isoformat()
                    }
            
            return {
                'status': 'success',
                'data': result,
                'source': 'CoinGecko'
            }
            
        except Exception as e:
            logger.error(f"CoinGecko获取失败: {str(e)}")
            return {'status': 'error', 'error': str(e), 'source': 'CoinGecko'}
    
    def _fetch_binance(self, symbols: list) -> Dict[str, Any]:
        """从币安获取数据（尝试）"""
        try:
            result = {}
            
            for symbol in symbols:
                try:
                    url = f"https://api.binance.com/api/v3/ticker/price"
                    params = {'symbol': f"{symbol}USDT"}
                    
                    response = requests.get(url, params=params, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        result[symbol] = {
                            'price': float(data['price']),
                            'source': 'Binance',
                            'timestamp': datetime.now().isoformat()
                        }
                    else:
                        logger.warning(f"币安{symbol}获取失败: {response.status_code}")
                        
                except Exception as e:
                    logger.warning(f"币安{symbol}异常: {str(e)}")
                    continue
            
            if result:
                return {
                    'status': 'success',
                    'data': result,
                    'source': 'Binance'
                }
            else:
                return {'status': 'error', 'error': '所有币种获取失败', 'source': 'Binance'}
                
        except Exception as e:
            logger.error(f"币安整体获取失败: {str(e)}")
            return {'status': 'error', 'error': str(e), 'source': 'Binance'}
    
    def _fetch_cryptocompare(self, symbols: list) -> Dict[str, Any]:
        """从CryptoCompare获取数据"""
        try:
            url = "https://min-api.cryptocompare.com/data/pricemulti"
            params = {
                'fsyms': ','.join(symbols),
                'tsyms': 'USD',
                'api_key': 'demo'  # 使用demo key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            result = {}
            for symbol in symbols:
                if symbol in data and 'USD' in data[symbol]:
                    result[symbol] = {
                        'price': data[symbol]['USD'],
                        'source': 'CryptoCompare',
                        'timestamp': datetime.now().isoformat()
                    }
            
            return {
                'status': 'success',
                'data': result,
                'source': 'CryptoCompare'
            }
            
        except Exception as e:
            logger.error(f"CryptoCompare获取失败: {str(e)}")
            return {'status': 'error', 'error': str(e), 'source': 'CryptoCompare'}
    
    def get_crypto_data(self, symbols: list) -> Dict[str, Any]:
        """获取加密货币数据（自动选择数据源）"""
        cache_key = ','.join(sorted(symbols))
        
        # 检查缓存
        if cache_key in self.cache:
            cache_data = self.cache[cache_key]
            cache_time = self.last_fetch_time.get(cache_key)
            
            if cache_time and (datetime.now() - cache_time).seconds < 60:  # 60秒缓存
                logger.info(f"使用缓存数据: {cache_key}")
                return cache_data
        
        # 按优先级尝试数据源
        for source in sorted(self.data_sources, key=lambda x: x['priority']):
            logger.info(f"尝试数据源: {source['name']}")
            
            result = source['function'](symbols)
            
            if result['status'] == 'success':
                logger.info(f"✅ 数据源 {source['name']} 成功")
                
                # 更新缓存
                self.cache[cache_key] = result
                self.last_fetch_time[cache_key] = datetime.now()
                
                return result
            
            logger.warning(f"❌ 数据源 {source['name']} 失败: {result.get('error', '未知错误')}")
        
        # 所有数据源都失败，返回错误
        return {
            'status': 'error',
            'error': '所有数据源都失败',
            'timestamp': datetime.now().isoformat()
        }
    
    def get_specific_crypto(self, symbol: str) -> Optional[Dict[str, Any]]:
        """获取特定币种数据"""
        result = self.get_crypto_data([symbol])
        
        if result['status'] == 'success' and symbol in result['data']:
            return result['data'][symbol]
        
        return None

# 测试函数
def test_multi_source():
    """测试多数据源系统"""
    print("🧪 测试多数据源加密货币数据系统")
    print("=" * 60)
    
    fetcher = CryptoDataFetcher()
    
    # 测试获取BTC和XRP
    print("1. 获取BTC和XRP实时数据...")
    result = fetcher.get_crypto_data(['BTC', 'XRP'])
    
    if result['status'] == 'success':
        print(f"✅ 数据获取成功，来源: {result['source']}")
        
        for symbol, data in result['data'].items():
            print(f"\n📊 {symbol}:")
            print(f"   价格: ${data.get('price', 'N/A'):,.2f}")
            print(f"   来源: {data.get('source', '未知')}")
            print(f"   时间: {data.get('timestamp', '未知')}")
            
            if 'change_24h' in data:
                change = data['change_24h']
                change_str = f"{change:+.2f}%" if change else "N/A"
                print(f"   24h变化: {change_str}")
    else:
        print(f"❌ 数据获取失败: {result.get('error', '未知错误')}")
    
    # 测试缓存
    print("\n2. 测试缓存功能...")
    result2 = fetcher.get_crypto_data(['BTC', 'XRP'])
    print(f"   第二次获取（应使用缓存）")
    
    print("\n3. 获取单个币种...")
    btc_data = fetcher.get_specific_crypto('BTC')
    if btc_data:
        print(f"   ✅ BTC: ${btc_data.get('price', 'N/A'):,.2f}")
    else:
        print("   ❌ BTC数据获取失败")
    
    print("\n" + "=" * 60)
    print("🎯 多数据源系统测试完成！")

if __name__ == "__main__":
    test_multi_source()
