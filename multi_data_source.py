#!/usr/bin/env python3
"""
多数据源管理器
支持币安API和CoinGecko API
自动选择可用数据源
"""

import requests
import time
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

class MultiDataSource:
    """多数据源管理器"""
    
    def __init__(self):
        self.data_sources = [
            {
                'name': 'CoinGecko',
                'priority': 1,
                'function': self._fetch_coingecko,
                'cache_ttl': 60
            },
            {
                'name': 'Binance',
                'priority': 2,
                'function': self._fetch_binance,
                'cache_ttl': 30
            }
        ]
        
        self.cache = {}
        self.cache_time = {}
        self.active_source = None
        
    def _fetch_coingecko(self, symbols: List[str]) -> Dict[str, Any]:
        """从CoinGecko获取数据"""
        try:
            # 映射币种名称
            symbol_map = {
                'BTC': 'bitcoin',
                'ETH': 'ethereum',
                'BNB': 'binancecoin',
                'SOL': 'solana',
                'XRP': 'ripple',
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
            return {'status': 'error', 'error': str(e), 'source': 'CoinGecko'}
    
    def _fetch_binance(self, symbols: List[str]) -> Dict[str, Any]:
        """从币安获取数据"""
        try:
            result = {}
            
            for symbol in symbols:
                try:
                    # 映射交易对
                    symbol_map = {
                        'BTC': 'BTCUSDT',
                        'ETH': 'ETHUSDT',
                        'BNB': 'BNBUSDT',
                        'SOL': 'SOLUSDT',
                        'XRP': 'XRPUSDT',
                        'LINK': 'LINKUSDT'
                    }
                    
                    trading_pair = symbol_map.get(symbol, f"{symbol}USDT")
                    
                    # 获取价格
                    price_url = "https://api.binance.com/api/v3/ticker/price"
                    price_params = {'symbol': trading_pair}
                    
                    price_response = requests.get(price_url, params=price_params, timeout=5)
                    
                    if price_response.status_code == 200:
                        price_data = price_response.json()
                        
                        # 获取24小时数据
                        ticker_url = "https://api.binance.com/api/v3/ticker/24hr"
                        ticker_params = {'symbol': trading_pair}
                        
                        ticker_response = requests.get(ticker_url, params=ticker_params, timeout=5)
                        
                        if ticker_response.status_code == 200:
                            ticker_data = ticker_response.json()
                            
                            result[symbol] = {
                                'price': float(price_data['price']),
                                'change_24h': float(ticker_data.get('priceChangePercent', 0)),
                                'high_price': float(ticker_data.get('highPrice', 0)),
                                'low_price': float(ticker_data.get('lowPrice', 0)),
                                'volume_24h': float(ticker_data.get('volume', 0)),
                                'quote_volume': float(ticker_data.get('quoteVolume', 0)),
                                'source': 'Binance',
                                'timestamp': datetime.now().isoformat()
                            }
                        else:
                            # 只有价格数据
                            result[symbol] = {
                                'price': float(price_data['price']),
                                'source': 'Binance',
                                'timestamp': datetime.now().isoformat()
                            }
                    
                except Exception as e:
                    print(f"币安{symbol}获取失败: {e}")
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
            return {'status': 'error', 'error': str(e), 'source': 'Binance'}
    
    def get_crypto_data(self, symbols: List[str]) -> Dict[str, Any]:
        """获取加密货币数据（自动选择数据源）"""
        cache_key = ','.join(sorted(symbols))
        
        # 检查缓存
        if cache_key in self.cache:
            cache_data = self.cache[cache_key]
            cache_time = self.cache_time.get(cache_key)
            
            if cache_time and (datetime.now() - cache_time).seconds < 30:  # 30秒缓存
                return cache_data
        
        # 按优先级尝试数据源
        for source in sorted(self.data_sources, key=lambda x: x['priority']):
            print(f"尝试数据源: {source['name']}")
            
            result = source['function'](symbols)
            
            if result['status'] == 'success':
                print(f"✅ 数据源 {source['name']} 成功")
                self.active_source = source['name']
                
                # 更新缓存
                self.cache[cache_key] = result
                self.cache_time[cache_key] = datetime.now()
                
                return result
            
            print(f"❌ 数据源 {source['name']} 失败: {result.get('error', '未知错误')}")
        
        # 所有数据源都失败，返回模拟数据
        print("⚠️ 所有数据源都失败，使用模拟数据")
        return self._get_simulated_data(symbols)
    
    def _get_simulated_data(self, symbols: List[str]) -> Dict[str, Any]:
        """获取模拟数据"""
        base_prices = {
            'BTC': 73860, 'ETH': 2100, 'BNB': 600,
            'SOL': 180, 'XRP': 1.51, 'LINK': 20
        }
        
        result = {}
        for symbol in symbols:
            price = base_prices.get(symbol, 1000)
            result[symbol] = {
                'price': price,
                'change_24h': 0,
                'source': 'Simulated',
                'timestamp': datetime.now().isoformat(),
                'warning': '使用模拟数据，请检查网络连接'
            }
        
        return {
            'status': 'simulated',
            'data': result,
            'source': 'Simulated',
            'warning': '所有数据源失败，使用模拟数据'
        }
    
    def get_specific_crypto(self, symbol: str) -> Optional[Dict[str, Any]]:
        """获取特定币种数据"""
        result = self.get_crypto_data([symbol])
        
        if result['status'] in ['success', 'simulated'] and symbol in result['data']:
            return result['data'][symbol]
        
        return None
    
    def test_all_sources(self) -> Dict[str, Any]:
        """测试所有数据源"""
        test_symbols = ['BTC', 'ETH']
        results = {}
        
        print("🧪 测试所有数据源...")
        print("=" * 50)
        
        for source in self.data_sources:
            print(f"\n测试 {source['name']}...")
            result = source['function'](test_symbols)
            
            results[source['name']] = {
                'status': result['status'],
                'error': result.get('error'),
                'data_count': len(result.get('data', {}))
            }
            
            if result['status'] == 'success':
                print(f"✅ {source['name']}: 成功获取 {len(result['data'])} 个币种")
                for symbol, data in result['data'].items():
                    print(f"   {symbol}: ${data.get('price', 'N/A'):,.2f}")
            else:
                print(f"❌ {source['name']}: 失败 - {result.get('error', '未知错误')}")
        
        # 确定推荐数据源
        available_sources = [name for name, data in results.items() if data['status'] == 'success']
        
        if available_sources:
            recommended = available_sources[0]
            print(f"\n🎯 推荐数据源: {recommended}")
        else:
            print(f"\n⚠️ 无可用数据源，将使用模拟数据")
        
        return {
            'results': results,
            'available_sources': available_sources,
            'recommended_source': available_sources[0] if available_sources else 'Simulated',
            'timestamp': datetime.now().isoformat()
        }

def main():
    """主函数"""
    print("=" * 60)
    print("🔧 多数据源管理器测试")
    print("=" * 60)
    
    # 创建数据源管理器
    data_source = MultiDataSource()
    
    # 测试所有数据源
    test_results = data_source.test_all_sources()
    
    # 获取实时数据
    print(f"\n📊 获取实时数据...")
    symbols = ['BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'LINK']
    result = data_source.get_crypto_data(symbols)
    
    print(f"\n✅ 数据获取完成")
    print(f"   数据源: {result['source']}")
    print(f"   状态: {result['status']}")
    
    if result['status'] in ['success', 'simulated']:
        print(f"\n📈 实时价格:")
        for symbol in ['BTC', 'ETH', 'XRP']:
            if symbol in result['data']:
                data = result['data'][symbol]
                price = data.get('price', 0)
                change = data.get('change_24h', 0)
                source = data.get('source', '未知')
                
                print(f"   {symbol}: ${price:,.2f} ({change:+.2f}%) - {source}")
    
    if 'warning' in result:
        print(f"\n⚠️ 警告: {result['warning']}")
    
    print(f"\n🌐 推荐配置:")
    print(f"   主数据源: CoinGecko (免费，无需API密钥)")
    print(f"   备用数据源: 币安API (需要配置，但可能受地域限制)")
    print(f"   自动故障转移: 已实现")

if __name__ == "__main__":
    main()
