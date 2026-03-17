#!/usr/bin/env python3
"""
真实数据版本金融市场分析系统
使用币安API获取实时数据
"""

import sys
import os
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any
import hashlib

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from binance_data_fetcher import BinanceDataFetcher
    print("✅ 币安数据模块导入成功")
except ImportError as e:
    print(f"❌ 币安数据模块导入失败: {e}")
    sys.exit(1)

class RealtimeFinancialAnalyzer:
    """实时金融分析器"""
    
    def __init__(self):
        self.timestamp = datetime.now()
        self.beijing_time = self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        self.symbols = ['BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'LINK']
        
        # 创建数据获取器
        self.fetcher = BinanceDataFetcher()
        
        # 加载历史分析记录
        self.history = self.load_analysis_history()
        
        # 测试连接
        if not self.fetcher.test_connection():
            print("⚠️ 币安API连接测试失败，将使用模拟数据")
            self.use_real_data = False
        else:
            self.use_real_data = True
            print("✅ 币安API连接成功，使用真实数据")
    
    def load_analysis_history(self) -> List[Dict[str, Any]]:
        """加载历史分析记录"""
        history_file = 'realtime_analysis_history.json'
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_analysis_history(self, analysis_data: Dict[str, Any]):
        """保存分析历史"""
        history_file = 'realtime_analysis_history.json'
        
        # 添加到历史
        self.history.append({
            'timestamp': self.timestamp.isoformat(),
            'beijing_time': self.beijing_time,
            'report_file': analysis_data.get('report_file', ''),
            'summary': analysis_data.get('summary', {}),
            'key_findings': analysis_data.get('key_findings', []),
            'data_source': 'binance' if self.use_real_data else 'simulated'
        })
        
        # 只保留最近30天的记录
        if len(self.history) > 30:
            self.history = self.history[-30:]
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def get_real_time_prices(self) -> Dict[str, float]:
        """获取实时价格"""
        if self.use_real_data:
            return self.fetcher.get_all_prices(self.symbols)
        else:
            # 模拟数据
            return {
                'BTC': 73860.0, 'ETH': 2100.0, 'BNB': 600.0,
                'SOL': 180.0, 'XRP': 1.51, 'LINK': 20.0
            }
    
    def get_24hr_data(self) -> Dict[str, Dict[str, Any]]:
        """获取24小时数据"""
        if self.use_real_data:
            return self.fetcher.get_all_24hr_data(self.symbols)
        else:
            # 模拟数据
            data = {}
            for symbol in self.symbols:
                data[symbol] = {
                    'price': 0,
                    'price_change_percent': 0,
                    'volume': 0,
                    'high_price': 0,
                    'low_price': 0
                }
            return data
    
    def get_technical_indicators(self, symbol: str) -> Dict[str, Any]:
        """获取技术指标"""
        if self.use_real_data:
            indicators = self.fetcher.calculate_technical_indicators(symbol)
            
            # 确保所有字段都有值
            if not indicators:
                indicators = {}
            
            # 添加默认值
            indicators.setdefault('macd', {'signal': '盘整', 'macd_line': 0, 'signal_line': 0, 'histogram': 0})
            indicators.setdefault('rsi', 50)
            indicators.setdefault('bollinger_bands', {'position': 50, 'upper': 0, 'middle': 0, 'lower': 0})
            
            return indicators
        else:
            # 模拟数据
            return {
                'macd': {'signal': '金叉', 'macd_line': 10.5, 'signal_line': 8.2, 'histogram': 2.3},
                'rsi': 65.5,
                'bollinger_bands': {'position': 65.2, 'upper': 0, 'middle': 0, 'lower': 0},
                'sma_20': 0,
                'sma_50': 0,
                'sma_200': 0
            }
    
    def get_international_news(self) -> List[Dict[str, Any]]:
        """获取国际新闻（真实数据需要新闻API）"""
        # 这里使用静态数据，实际应该集成新闻API
        return [
            {
                'title': '美联储维持利率不变，暗示年内可能降息',
                'category': '宏观经济',
                'impact': 'positive',
                'link': 'https://www.federalreserve.gov/',
                'analysis': '流动性预期改善，利好风险资产'
            },
            {
                'title': '比特币现货ETF持续净流入',
                'category': '机构资金',
                'impact': 'strong_positive',
                'link': 'https://www.coindesk.com/',
                'analysis': '机构资金大规模入场，提供买盘支撑'
            }
        ]
    
    def analyze_crypto_comprehensive(self, symbol: str) -> Dict[str, Any]:
        """综合分析加密货币"""
        # 获取实时数据
        prices = self.get_real_time_prices()
        ticker_data = self.get_24hr_data()
        indicators = self.get_technical_indicators(symbol)
        
        price = prices.get(symbol, 0)
        ticker = ticker_data.get(symbol, {})
        
        # 根据技术指标生成分析
        macd_signal = indicators.get('macd', {}).get('signal', '盘整')
        rsi_value = indicators.get('rsi', 50)
        bb_position = indicators.get('bollinger_bands', {}).get('position', 50)
        
        # 生成交易建议
        if macd_signal == '金叉' and rsi_value < 70 and bb_position < 80:
            action = '买入'
            confidence = 75
            reason = '技术指标显示上涨信号，风险可控'
        elif macd_signal == '死叉' or rsi_value > 80 or bb_position > 90:
            action = '观望'
            confidence = 60
            reason = '技术指标显示超买或下跌风险'
        else:
            action = '持有'
            confidence = 65
            reason = '技术指标中性，趋势延续'
        
        return {
            'price': price,
            'change_24h': ticker.get('price_change_percent', 0),
            'volume_24h': ticker.get('volume', 0),
            
            'macd': indicators.get('macd', {}),
            'rsi': rsi_value,
            'bollinger_bands': indicators.get('bollinger_bands', {}),
            
            'market_sentiment': {
                'analysis': self.get_sentiment_analysis(symbol, price, ticker)
            },
            
            'whale_activity': {
                'analysis': self.get_whale_analysis(symbol)
            },
            
            'project_development': {
                'analysis': self.get_project_analysis(symbol)
            },
            
            'trading_recommendation': {
                'action': action,
                'confidence': confidence,
                'reason': reason,
                'target_price': price * 1.1 if action == '买入' else price,
                'stop_loss': price * 0.95
            },
            
            'data_source': 'binance' if self.use_real_data else 'simulated',
            'data_timestamp': self.beijing_time
        }
    
    def get_sentiment_analysis(self, symbol: str, price: float, ticker: Dict[str, Any]) -> str:
        """获取市场情绪分析"""
        change = ticker.get('price_change_percent', 0)
        volume = ticker.get('volume', 0)
        
        if change > 5:
            return f"{symbol}价格大幅上涨{change:.2f}%，市场情绪极度乐观，成交量${volume:,.0f}"
        elif change > 2:
            return f"{symbol}温和上涨{change:.2f}%，市场情绪积极"
        elif change > -2:
            return f"{symbol}价格震荡，市场情绪中性"
        else:
            return f"{symbol}价格下跌{abs(change):.2f}%，市场情绪谨慎"
    
    def get_whale_analysis(self, symbol: str) -> str:
        """获取鲸鱼动态分析（需要链上数据API）"""
        # 这里使用静态分析，实际应该集成链上数据API
        analyses = {
            'BTC': '鲸鱼地址持续增持，交易所净流出明显',
            'ETH': '鲸鱼活动温和，长期持有者稳定',
            'BNB': '币安生态内资金流动增加',
            'XRP': '法律利好吸引机构资金入场',
            'SOL': '鲸鱼增持明显，生态发展活跃',
            'LINK': '鲸鱼活动稳定，项目持续建设'
        }
        return analyses.get(symbol, '鲸鱼动态数据更新中')
    
    def get_project_analysis(self, symbol: str) -> str:
        """获取项目方动向分析"""
        analyses = {
            'BTC': '比特币核心开发活跃，Layer2解决方案进展',
            'ETH': '以太坊基金会推动升级，Layer2生态发展',
            'BNB': '币安链生态扩展，DeFi和GameFi项目增加',
            'XRP': 'Ripple拓展支付网络，金融机构合作',
            'SOL': 'Solana基金会优化网络，生态项目融资',
            'LINK': 'Chainlink扩展预言机网络，跨链功能'
        }
        return analyses.get(symbol, '项目方动向更新中')
    
    def generate_complete_analysis(self) -> Dict[str, Any]:
        """生成完整分析报告"""
        print(f"🎯 开始生成实时分析报告...")
        print(f"📅 分析时间: {self.beijing_time} (北京时间)")
        print(f"📊 数据源: {'币安实时API' if self.use_real_data else '模拟数据'}")
        
        # 收集所有数据
        analysis_data = {
            'timestamp': self.timestamp.isoformat(),
            'beijing_time': self.beijing_time,
            'report_id': hashlib.md5(self.beijing_time.encode()).hexdigest()[:8],
            'data_source': 'binance' if self.use_real_data else 'simulated',
            
            # 实时价格数据
            'real_time_prices': self.get_real_time_prices(),
            '24hr_data': self.get_24hr_data(),
            
            # 国际新闻
            'international_news': self.get_international_news(),
            
            # 加密货币深度分析
            'crypto_analysis': {},
            
            # 总结
            'summary': {},
            'key_findings': []
        }
        
        # 分析每个加密货币
        print(f"📊 分析 {len(self.symbols)} 个加密货币...")
        for symbol in self.symbols:
            print(f"  分析 {symbol}...")
            analysis_data['crypto_analysis'][symbol] = self.analyze_crypto_comprehensive(symbol)
        
        # 生成总结
        analysis_data['summary'] = self.generate_summary(analysis_data)
        analysis_data['key_findings'] = analysis_data['summary'].get('key_findings', [])
        
        # 生成报告文件
        report_file = self.generate_html_report(analysis_data)
        analysis_data['report_file'] = report_file
        
        # 保存到历史
        self.save_analysis_history(analysis_data)
        
        print(f"✅ 实时分析报告生成完成！")
        print(f"   报告文件: {report_file}")
        
        return analysis_data
    
    def generate_summary(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """生成分析总结"""
        crypto_data = analysis_data['crypto_analysis']
        prices = analysis_data['real_time_prices']
        
        # 统计信号
        buy_signals = 0
        hold_signals = 0
        total_confidence = 0
        
        for symbol, data in crypto_data.items():
            recommendation = data.get('trading_recommendation', {})
            action = recommendation.get('action', '')
            if action == '买入':
                buy_signals += 1
            elif action == '持有':
                hold_signals += 1
            total_confidence += recommendation.get('confidence', 50)
        
        avg_confidence = total_confidence / len(crypto_data) if crypto_data else 0
        
        # 判断市场情绪
        if avg_confidence > 75:
            market_sentiment = '乐观'
            sentiment_color = '#27ae60'
        elif avg_confidence > 65:
            market_sentiment = '中性偏多'
            sentiment_color = '#f39c12'
        else:
            market_sentiment = '谨慎'
            sentiment_color = '#e74c3c'
        
        # 关键发现
        key_findings = [
            f"数据源: {'币安实时API' if self.use_real_data else '模拟数据'}",
            f"分析时间: {self.beijing_time}",
            f"市场情绪: {market_sentiment}"
        ]
        
        # 添加价格信息
        for symbol in ['BTC', 'ETH', 'XRP']:
            if symbol in prices and prices[symbol] > 0:
                key_findings.append(f"{symbol}: ${prices[symbol]:,.2f}")
        
        return {
            'total_coins_analyzed': len(crypto_data),
            'buy_signals': buy_signals,
            'hold_signals': hold_signals,
            'watch_signals': len(crypto_data) - buy_signals - hold_signals,
            'average_confidence': round(avg_confidence, 1),
            'market_sentiment': market_sentiment,
            'sentiment_color': sentiment_color,
            'key_findings': key_findings,
            'recommendation': '基于技术指标分析，控制风险，分批建仓'
        }
    
    def generate_html_report(self, analysis_data: Dict[str, Any]) -> str:
        """生成HTML报告"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"reports/realtime_analysis_{timestamp}.html"
        
        print(f"📄 生成HTML报告: {report_file}")
        
        # 生成HTML内容
        html_content = self.generate_report_html(analysis_data)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return report_file
    
    def generate_report_html(self, analysis_data: Dict[str, Any]) -> str:
        """生成报告HTML"""
        prices = analysis_data['real_time_prices']
        crypto_analysis = analysis_data['crypto_analysis']
        summary = analysis_data['summary']
        
        # 开始生成HTML
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 实时金融市场分析报告</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            line-height: 1.8;
            font-size: 18px;
            background: #f5f7fa;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #1a2980 0%, #26d0ce 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .data-source {{
            background: #e8f4fd;
            padding: 20px;
            margin: 20px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
        }}
        .crypto-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
            padding: 30px;
        }}
        .crypto-card {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
            border-left: 5px solid #3498db;
        }}
        .price-display {{
            font-size: 32px;
            font-weight: bold;
            margin: 10px 0;
        }}
        .signal-box {{
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin-top: 20px;
            font-weight: bold;
        }}
        .signal-buy {{ background: #d4edda; color: #155724; }}
        .signal-hold {{ background: #fff3cd; color: #856404; }}
        .signal-watch {{ background: #f8d7da; color: #721c24; }}
        .footer {{
            text-align: center;
            padding: 30px;
            background: #2c3e50;
            color: white;
        }}
        @media (max-width: 768px) {{
            body {{ font-size: 17px; }}
            .header {{ padding: 30px 20px; }}
            .crypto-grid {{ grid-template-columns: 1fr; }}
            .price-display {{ font-size: 28px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 实时金融市场分析报告</h1>
            <p>生成时间: {analysis_data['beijing_time']} (北京时间)</p>
            <p>报告ID: {analysis_data['report_id']}</p>
        </div>
        
        <div class="data-source">
            📡 数据源: {analysis_data['data_source'].upper()} | 数据时间: {analysis_data['beijing_time']}
        </div>
        
        <div style="padding: 30px;">
            <h2>🎯 市场总结</h2>
            <div style="background: {summary['sentiment_color']}20; padding: 25px; border-radius: 10px;">
                <div style="font-size: 24px; font-weight: bold;">市场情绪: {summary['market_sentiment']}</div>
                <div>平均信心度: {summary['average_confidence']}%</div>
                <div>买入信号: {summary['buy_signals']} 个 | 持有信号: {summary['hold_signals']} 个</div>
                <div style="margin-top: 15px; font-weight: bold;">投资建议: {summary['recommendation']}</div>
            </div>
        </div>
        
        <div style="padding: 30px;">
            <h2>₿ 加密货币实时分析</h2>
            <div class="crypto-grid">
'''
        
        # 添加加密货币卡片
        for symbol, data in crypto_analysis.items():
            price = data['price']
            change = data['change_24h']
            recommendation = data['trading_recommendation']
            
            signal_class = f"signal-{recommendation['action'].lower()}"
            change_color = '#27ae60' if change > 0 else '#e74c3c'
            
            html += f'''
                <div class="crypto-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="font-size: 28px; font-weight: bold;">{symbol}</div>
                        <div class="price-display">${price:,.2f}</div>
                    </div>
                    
                    <div style="color: {change_color}; font-size: 22px; margin: 15px 0;">
                        {change:+.2f}%
                    </div>
                    
                    <div style="margin: 20px 0;">
                        <div><strong>MACD信号:</strong> {data['macd'].get('signal', 'N/A')}</div>
                        <div><strong>RSI指标:</strong> {data.get('rsi', 'N/A')}</div>
                        <div><strong>布林带位置:</strong> {data['bollinger_bands'].get('position', 'N/A')}%</div>
                        <div><strong>市场情绪:</strong> {data['market_sentiment']['analysis']}</div>
                        <div><strong>鲸鱼动态:</strong> {data['whale_activity']['analysis']}</div>
                    </div>
                    
                    <div class="{signal_class} signal-box">
                        <div style="font-size: 24px;">{recommendation['action']}</div>
                        <div style="font-size: 18px;">信心度: {recommendation['confidence']}%</div>
                        <div style="font-size: 16px; margin-top: 10px;">{recommendation['reason']}</div>
                    </div>
                    
                    <div style="font-size: 14px; color: #666; margin-top: 15px;">
                        数据时间: {data.get('data_timestamp', 'N/A')}
                    </div>
                </div>
'''
        
        html += '''            </div>
        </div>
        
        <div class="footer">
            <p style="font-size: 24px; font-weight: bold; margin-bottom: 20px;">📊 实时金融市场分析系统</p>
            <p>数据源: ''' + ('币安实时API' if analysis_data['data_source'] == 'binance' else '模拟数据') + '''</p>
            <p>生成时间: ''' + analysis_data['beijing_time'] + '''</p>
            <p>投资有风险，分析仅供参考</p>
        </div>
    </div>
    
    <script>
        console.log('实时分析报告加载完成');
        console.log('数据源:', '''' + analysis_data['data_source'] + '''');
        console.log('分析时间:', '''' + analysis_data['beijing_time'] + '''');
    </script>
</body>
</html>'''
        
        return html

def main():
    """主函数"""
    print("=" * 80)
    print("🚀 实时金融市场分析系统")
    print("=" * 80)
    
    # 创建分析器
    analyzer = RealtimeFinancialAnalyzer()
    
    # 生成完整分析
    analysis_data = analyzer.generate_complete_analysis()
    
    print(f"\n✅ 分析完成！")
    print(f"   报告文件: {analysis_data['report_file']}")
    print(f"   数据源: {analysis_data['data_source']}")
    print(f"   分析时间: {analysis_data['beijing_time']}")
    
    # 显示实时价格
    prices = analysis_data['real_time_prices']
    print(f"\n📊 实时价格:")
    for symbol in ['BTC', 'ETH', 'XRP']:
        if symbol in prices:
            print(f"   {symbol}: ${prices[symbol]:,.2f}")
    
    print(f"\n🌐 访问URL:")
    print(f"   最新报告: https://MrSunjm.github.io/financial-reports/{analysis_data['report_file']}")

if __name__ == "__main__":
    main()
