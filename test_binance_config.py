#!/usr/bin/env python3
"""
测试币安API连接
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from binance_data_fetcher import test_binance_integration
    print("🧪 测试币安API集成...")
    print("=" * 50)
    
    # 测试连接
    test_binance_integration()
    
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("请确保已正确配置 binance_config.py")
except Exception as e:
    print(f"❌ 测试失败: {e}")
