#!/usr/bin/env python3
"""
最终实时金融市场分析系统
使用多数据源获取准确数据
"""

import sys
import os
from datetime import datetime
import json
from typing import Dict, List, Any
import hashlib

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from multi_data_source import MultiDataSource
    print("✅ 多数据源模块导入成功")
except ImportError as e:
    print(f"❌ 多数据源模块导入失败: {e}")
    sys.exit(1)

class FinalRealtimeAnalyzer:
    """最终实时分析器"""
    
    def __init__(self):
        self.timestamp = datetime.now()
        self.beijing_time = self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        self.symbols = ['BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'LINK']
        
        # 创建数据源管理器
        self.data_source = MultiDataSource()
        
        # 测试数据源
        self.test_data_sources()
        
        # 加载历史分析记录
        self.history = self.load_analysis_history()
    
    def test_data_sources(self):
        """测试数据源"""
        print("🧪 测试数据源连接...")
        test_results = self.data_source.test_all_sources()
        
        if test_results['recommended_source'] == 'Simulated':
            print("⚠️ 警告: 所有数据源失败，将使用模拟数据")
            print("   建议: 检查网络连接或配置币安API密钥")
        else:
            print(f"✅ 数据源就绪: {test_results['recommended_source']}")
    
    def load_analysis_history(self) -> List[Dict[str, Any]]:
        """加载历史分析记录"""
        history_file = 'final_analysis_history.json'
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_analysis_history(self, analysis_data: Dict[str, Any]):
        """保存分析历史"""
        history_file = 'final_analysis_history.json'
        
        # 添加到历史
        self.history.append({
            'timestamp': self.timestamp.isoformat(),
            'beijing_time': self.beijing_time,
            'report_file': analysis_data.get('report_file', ''),
            'summary': analysis_data.get('summary', {}),
            'data_source': analysis_data.get('data_source', 'unknown'),
            'key_findings': analysis_data.get('key_findings', [])
        })
        
        # 只保留最近30天的记录
        if len(self.history) > 30:
            self.history = self.history[-30:]
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def get_real_time_data(self) -> Dict[str, Any]:
        """获取实时数据"""
        print("📊 获取实时加密货币数据...")
        result = self.data_source.get_crypto_data(self.symbols)
        
        return {
            'data': result.get('data', {}),
            'source': result.get('source', 'unknown'),
            'status': result.get('status', 'error'),
            'timestamp': self.beijing_time
        }
    
    def analyze_crypto_comprehensive(self, symbol: str, crypto_data: Dict[str, Any]) -> Dict[str, Any]:
        """综合分析加密货币"""
        data = crypto_data.get(symbol, {})
        price = data.get('price', 0)
        change = data.get('change_24h', 0)
        source = data.get('source', 'unknown')
        
        # 根据价格变化和技术指标生成分析
        if change > 5:
            sentiment = '极度乐观'
            action = '买入'
            confidence = 80
            reason = f'价格大幅上涨{change:.2f}%，市场情绪积极'
        elif change > 2:
            sentiment = '乐观'
            action = '持有'
            confidence = 70
            reason = f'温和上涨{change:.2f}%，趋势向好'
        elif change > -2:
            sentiment = '中性'
            action = '持有'
            confidence = 60
            reason = '价格震荡，等待方向选择'
        else:
            sentiment = '谨慎'
            action = '观望'
            confidence = 55
            reason = f'价格下跌{abs(change):.2f}%，需谨慎操作'
        
        # 技术指标分析（简化版）
        if price > 0:
            # 模拟技术指标计算
            if change > 3:
                macd_signal = '金叉'
                rsi = 65
                bb_position = 70
            elif change < -3:
                macd_signal = '死叉'
                rsi = 35
                bb_position = 30
            else:
                macd_signal = '盘整'
                rsi = 50
                bb_position = 50
        else:
            macd_signal = 'N/A'
            rsi = 50
            bb_position = 50
        
        return {
            'price': price,
            'change_24h': change,
            'volume_24h': data.get('volume_24h', 0),
            'high_price': data.get('high_price', 0),
            'low_price': data.get('low_price', 0),
            
            'technical_indicators': {
                'macd': {'signal': macd_signal},
                'rsi': rsi,
                'bollinger_bands': {'position': bb_position}
            },
            
            'market_sentiment': {
                'sentiment': sentiment,
                'analysis': self.get_sentiment_analysis(symbol, price, change)
            },
            
            'whale_activity': {
                'analysis': self.get_whale_analysis(symbol