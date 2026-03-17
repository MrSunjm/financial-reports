#!/usr/bin/env python3
"""
直接测试币安API
"""

import requests
from datetime import datetime

print("🔍 直接测试币安API连接...")
print("=" * 60)

# 测试1: 服务器时间
print("1. 测试服务器时间...")
try:
    response = requests.get("https://api.binance.com/api/v3/time", timeout=5)
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        server_time = data.get('serverTime', 0)
        if server_time:
            dt = datetime.fromtimestamp(server_time/1000)
            print(f"   服务器时间: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
            print("   ✅ 服务器时间获取成功")
        else:
            print("   ❌ 服务器时间数据异常")
    else:
        print(f"   ❌ 请求失败: {response.text[:100]}")
except Exception as e:
    print(f"   ❌ 异常: {e}")

print("\n2. 测试价格获取...")
try:
    response = requests.get("https://api.binance.com/api/v3/ticker/price", params={'symbol': 'BTCUSDT'}, timeout=5)
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   BTC价格: ${float(data.get('price', 0)):,.2f}")
        print("   ✅ 价格获取成功")
    else:
        print(f"   ❌ 请求失败: {response.text[:100]}")
except Exception as e:
    print(f"   ❌ 异常: {e}")

print("\n3. 测试24小时数据...")
try:
    response = requests.get("https://api.binance.com/api/v3/ticker/24hr", params={'symbol': 'BTCUSDT'}, timeout=5)
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        price = float(data.get('lastPrice', 0))
        change = float(data.get('priceChangePercent', 0))
        print(f"   BTC价格: ${price:,.2f}")
        print(f"   24h变化: {change:+.2f}%")
        print("   ✅ 24小时数据获取成功")
    else:
        print(f"   ❌ 请求失败: {response.text[:100]}")
except Exception as e:
    print(f"   ❌ 异常: {e}")

print("\n" + "=" * 60)
print("📋 测试总结:")
print("如果服务器时间测试失败，可能是网络问题或地域限制")
print("如果价格获取成功但API密钥失败，可能是密钥权限问题")
