#!/usr/bin/env python3
"""
更新自动化脚本使用实时数据
"""

import json
import sys
import os

# 读取当前的auto_daily_report.py
script_path = "auto_daily_report.py"
if not os.path.exists(script_path):
    print(f"❌ 找不到脚本: {script_path}")
    sys.exit(1)

with open(script_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 检查是否已包含实时数据
if "binance_realtime" in content or "api.binance.com" in content:
    print("✅ 脚本已包含实时数据功能")
else:
    print("⚠️ 脚本需要更新以包含实时数据")
    
    # 添加实时数据导入
    new_content = content.replace(
        "import yfinance as yf",
        """import yfinance as yf
import sys
import os

# 添加币安实时数据模块路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from binance_realtime import BinanceRealtimeData"""
    )
    
    # 添加获取实时数据的函数
    insert_point = "def get_crypto_data():"
    if insert_point in new_content:
        new_function = """
def get_crypto_data():
    \"\"\"获取加密货币实时数据（从币安）\"\"\"
    try:
        print("📊 从币安获取实时加密货币数据...")
        binance = BinanceRealtimeData()
        
        # 获取主要币种价格
        symbols = ['BTC', 'ETH', 'BNB', 'XRP', 'SOL', 'LINK']
        crypto_data = binance.get_multiple_prices(symbols)
        
        # 获取24小时数据
        crypto_24h = {}
        for symbol in ['BTC', 'XRP']:
            data_24h = binance.get_24h_ticker(symbol)
            if data_24h:
                crypto_24h[symbol] = data_24h
        
        print(f"✅ 获取到 {len(crypto_data)} 个币种实时数据")
        
        return {
            'prices': crypto_data,
            '24h_data': crypto_24h,
            'timestamp': datetime.now().isoformat(),
            'source': 'binance'
        }
        
    except Exception as e:
        print(f"❌ 获取加密货币数据失败: {e}")
        # 返回模拟数据作为后备
        return get_fallback_crypto_data()

def get_fallback_crypto_data():
    \"\"\"后备数据（当API失败时使用）\"\"\"
    print("⚠️ 使用后备数据（API可能暂时不可用）")
    
    # 这里应该从缓存或备用源获取数据
    # 暂时返回空数据
    return {
        'prices': {},
        '24h_data': {},
        'timestamp': datetime.now().isoformat(),
        'source': 'fallback',
        'warning': '使用后备数据，建议检查网络连接'
    }
"""
        
        # 替换原有的get_crypto_data函数
        lines = new_content.split('\n')
        new_lines = []
        in_function = False
        function_indent = 0
        
        for line in lines:
            if line.strip() == "def get_crypto_data():":
                in_function = True
                function_indent = len(line) - len(line.lstrip())
                new_lines.append(line)  # 保留函数定义
                # 添加新的函数体
                for func_line in new_function.split('\n'):
                    new_lines.append(" " * function_indent + func_line)
            elif in_function and line.startswith(" " * (function_indent + 4)):
                # 跳过旧的函数体
                continue
            elif in_function and not line.startswith(" " * function_indent):
                # 函数体结束
                in_function = False
                new_lines.append(line)
            elif not in_function:
                new_lines.append(line)
        
        new_content = '\n'.join(new_lines)
        
        # 保存更新后的脚本
        backup_path = f"{script_path}.backup"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ 脚本已更新，备份保存在: {backup_path}")
        print("   新增功能:")
        print("   • 从币安获取实时价格数据")
        print("   • 获取24小时行情数据")
        print("   • API失败时的后备机制")
    else:
        print("❌ 找不到get_crypto_data函数")

print("\n🎯 自动化脚本更新完成！")
