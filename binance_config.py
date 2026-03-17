#!/usr/bin/env python3
"""
币安API配置
使用用户提供的真实API密钥
"""

# 币安API配置 - 使用用户提供的真实密钥
BINANCE_CONFIG = {
    'api_key': 'CYGiPb9SyNM3SAaPP3av8yyGZgEGJeUTsCN8N4a6AUiAKlLAogvZjDBNoRKHmjBn',
    'api_secret': 'FQe5gjbTV9y1WtH6mDyY3EqqjG0IpRKQKWFe6D7bGPLp4AIEE05CLCHhYUiUthcz',
    'testnet': False,               # 使用主网
    'base_url': 'https://api.binance.com'
}

# 支持的交易对
SUPPORTED_SYMBOLS = ['BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'LINK']

# 技术指标参数
TECHNICAL_INDICATORS = {
    'rsi_period': 14,
    'macd_fast': 12,
    'macd_slow': 26,
    'macd_signal': 9,
    'bollinger_period': 20,
    'bollinger_std': 2
}

# 缓存配置
CACHE_CONFIG = {
    'price_cache_ttl': 30,      # 价格缓存30秒
    'ticker_cache_ttl': 60,     # 24小时数据缓存60秒
    'max_cache_size': 100       # 最大缓存条目数
}

print("✅ 币安API配置已更新")
print(f"   API密钥: {BINANCE_CONFIG['api_key'][:10]}...")
print(f"   Secret密钥: {BINANCE_CONFIG['api_secret'][:10]}...")
print(f"   支持币种: {', '.join(SUPPORTED_SYMBOLS)}")
