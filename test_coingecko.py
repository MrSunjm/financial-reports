#!/usr/bin/env python3
"""
测试CoinGecko API作为备用数据源
"""

import requests
import json
from datetime import datetime

def test_coingecko():
    """测试CoinGecko API"""
    print("🧪 测试CoinGecko API")
    print("=" * 50)
    
    try:
        # 获取BTC和XRP价格
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'bitcoin,ripple',
            'vs_currencies': 'usd',
            'include_24hr_change': 'true',
            'include_market_cap': 'true'
        }
        
        print("发送请求到CoinGecko API...")
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ CoinGecko API连接成功！")
            print(f"响应时间: {response.elapsed.total_seconds():.2f}秒")
            
            # 解析数据
            btc_data = data.get('bitcoin', {})
            xrp_data = data.get('ripple', {})
            
            print(f"\n📊 BTC数据:")
            print(f"   价格: ${btc_data.get('usd', 'N/A'):,.2f}")
            print(f"   24h变化: {btc_data.get('usd_24h_change', 'N/A'):.2f}%")
            
            print(f"\n📊 XRP数据:")
            print(f"   价格: ${xrp_data.get('usd', 'N/A'):,.2f}")
            print(f"   24h变化: {xrp_data.get('usd_24h_change', 'N/A'):.2f}%")
            
            return {
                'status': 'success',
                'data': data,
                'timestamp': datetime.now().isoformat()
            }
        else:
            print(f"❌ CoinGecko API错误: {response.status_code}")
            print(f"响应内容: {response.text[:200]}")
            return {
                'status': 'error',
                'error': f"HTTP {response.status_code}",
                'timestamp': datetime.now().isoformat()
            }
            
    except Exception as e:
        print(f"❌ CoinGecko API异常: {str(e)}")
        return {
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def test_alternative_sources():
    """测试备用数据源"""
    print("\n🔍 测试其他备用数据源...")
    
    sources = [
        {
            'name': 'CoinMarketCap模拟',
            'url': 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest',
            'params': {'symbol': 'BTC,XRP', 'convert': 'USD'}
        },
        {
            'name': 'CryptoCompare',
            'url': 'https://min-api.cryptocompare.com/data/pricemulti',
            'params': {'fsyms': 'BTC,XRP', 'tsyms': 'USD'}
        }
    ]
    
    for source in sources:
        print(f"\n测试 {source['name']}...")
        try:
            response = requests.get(source['url'], params=source['params'], timeout=5)
            print(f"  状态码: {response.status_code}")
            if response.status_code == 200:
                print(f"  ✅ 可用")
            else:
                print(f"  ❌ 不可用")
        except Exception as e:
            print(f"  ❌ 错误: {str(e)}")

if __name__ == "__main__":
    result = test_coingecko()
    
    print("\n" + "=" * 50)
    if result['status'] == 'success':
        print("🎯 CoinGecko API测试成功！")
        print("   可以使用CoinGecko作为主要数据源")
    else:
        print("⚠️ CoinGecko API测试失败")
        print("   需要寻找其他数据源或使用缓存数据")
    
    # 测试其他备用源
    test_alternative_sources()
