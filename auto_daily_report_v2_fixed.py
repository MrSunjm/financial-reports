#!/usr/bin/env python3
"""
增强版自动化每日报告脚本 V2.0
使用多数据源实时数据
"""

import sys
import os
import json
import time
from datetime import datetime, timedelta
import logging
from typing import Dict, Any, List

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入多数据源模块
try:
    from multi_source_data import CryptoDataFetcher
    HAS_REAL_DATA = True
except ImportError:
    HAS_REAL_DATA = False
    print("⚠️ 多数据源模块导入失败，将使用模拟数据")

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EnhancedDailyReporter:
    """增强版每日报告生成器"""
    
    def __init__(self):
        self.timestamp = datetime.now()
        self.report_date = self.timestamp.strftime("%Y%m%d")
        
        if HAS_REAL_DATA:
            self.data_fetcher = CryptoDataFetcher()
            logger.info("✅ 多数据源系统已初始化")
        else:
            logger.warning("⚠️ 使用模拟数据模式")
    
    def get_real_time_crypto_data(self) -> Dict[str, Any]:
        """获取实时加密货币数据"""
        if not HAS_REAL_DATA:
            return self._get_fallback_crypto_data()
        
        try:
            logger.info("📊 从多数据源获取实时加密货币数据...")
            
            # 获取主要币种
            symbols = ['BTC', 'ETH', 'BNB', 'XRP', 'SOL', 'LINK']
            result = self.data_fetcher.get_crypto_data(symbols)
            
            if result['status'] == 'success':
                logger.info(f"✅ 成功获取 {len(result['data'])} 个币种数据，来源: {result['source']}")
                return {
                    'status': 'success',
                    'data': result['data'],
                    'source': result['source'],
                    'timestamp': self.timestamp.isoformat()
                }
            else:
                logger.error(f"❌ 数据获取失败: {result.get('error', '未知错误')}")
                return self._get_fallback_crypto_data()
                
        except Exception as e:
            logger.error(f"❌ 数据获取异常: {str(e)}")
            return self._get_fallback_crypto_data()
    
    def _get_fallback_crypto_data(self) -> Dict[str, Any]:
        """获取后备数据（当实时数据不可用时）"""
        logger.warning("⚠️ 使用后备数据")
        
        # 这里应该从缓存或本地存储获取数据
        # 暂时返回模拟数据
        return {
            'status': 'fallback',
            'data': {
                'BTC': {
                    'price': 73500.0,
                    'change_24h': 2.5,
                    'source': 'fallback',
                    'timestamp': self.timestamp.isoformat(),
                    'warning': '使用后备数据，建议检查网络连接'
                },
                'XRP': {
                    'price': 1.50,
                    'change_24h': 8.2,
                    'source': 'fallback',
                    'timestamp': self.timestamp.isoformat(),
                    'warning': '使用后备数据，建议检查网络连接'
                }
            },
            'source': 'fallback',
            'timestamp': self.timestamp.isoformat(),
            'warning': '实时数据不可用，使用后备数据'
        }
    
    def get_stock_data(self) -> Dict[str, Any]:
        """获取股票数据（使用yfinance）"""
        try:
            import yfinance as yf
            
            logger.info("📈 获取股票市场数据...")
            
            # 定义关注的股票
            stocks = {
                'AAPL': '苹果',
                'MSFT': '微软',
                'GOOGL': '谷歌',
                'TSLA': '特斯拉',
                'NVDA': '英伟达'
            }
            
            stock_data = {}
            for symbol, name in stocks.items():
                try:
                    ticker = yf.Ticker(symbol)
                    info = ticker.info
                    
                    stock_data[symbol] = {
                        'name': name,
                        'price': info.get('regularMarketPrice', info.get('currentPrice')),
                        'change': info.get('regularMarketChangePercent'),
                        'market_cap': info.get('marketCap'),
                        'timestamp': self.timestamp.isoformat()
                    }
                    
                    logger.info(f"   ✅ {symbol}: ${stock_data[symbol]['price']:,.2f}")
                    
                except Exception as e:
                    logger.warning(f"   ⚠️ {symbol}获取失败: {str(e)}")
                    stock_data[symbol] = {
                        'name': name,
                        'error': str(e),
                        'timestamp': self.timestamp.isoformat()
                    }
            
            return {
                'status': 'success',
                'data': stock_data,
                'timestamp': self.timestamp.isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ 股票数据获取失败: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': self.timestamp.isoformat()
            }
    
    def generate_html_report(self, crypto_data: Dict[str, Any], stock_data: Dict[str, Any]) -> str:
        """生成HTML报告"""
        logger.info("📄 生成HTML报告...")
        
        # 提取数据
        btc_info = crypto_data['data'].get('BTC', {})
        xrp_info = crypto_data['data'].get('XRP', {})
        
        btc_price = btc_info.get('price', 'N/A')
        xrp_price = xrp_info.get('price', 'N/A')
        btc_change = btc_info.get('change_24h', 'N/A')
        xrp_change = xrp_info.get('change_24h', 'N/A')
        
        # 生成报告文件名
        timestamp_str = self.timestamp.strftime("%Y%m%d_%H%M%S")
        report_file = f"reports/daily_realtime_{timestamp_str}.html"
        
        # HTML模板
        html_content = f'''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 实时金融市场分析报告</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.8; font-size: 18px; }}
        .header {{ background: linear-gradient(135deg, #1a2980 0%, #26d0ce 100%); color: white; padding: 40px; text-align: center; border-radius: 15px; }}
        .price-card {{ background: #f8f9fa; padding: 25px; margin: 25px 0; border-radius: 12px; border-left: 5px solid #3498db; }}
        .data-source {{ background: #e8f4fd; padding: 15px; border-radius: 8px; margin: 20px 0; font-size: 16px; }}
        .positive {{ color: #27ae60; font-weight: bold; }}
        .negative {{ color: #e74c3c; font-weight: bold; }}
        .data-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        .data-table th, .data-table td {{ padding: 15px; text-align: left; border-bottom: 1px solid #ddd; }}
        .data-table th {{ background: #f8f9fa; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 实时金融市场分析报告</h1>
        <p>基于实时数据 | {self.timestamp.strftime('%Y年%m月%d日 %H:%M:%S')}</p>
        <p style="opacity: 0.9;">数据源: {crypto_data.get('source', '多数据源')}</p>
    </div>
    
    <div class="data-source">
        <strong>📡 数据源信息:</strong>
        <p>加密货币数据: {crypto_data.get('source', '未知')} | 更新时间: {crypto_data.get('timestamp', '未知')}</p>
        <p>股票数据: {stock_data.get('status', '未知')} | 数据状态: {'✅ 实时数据' if crypto_data['status'] == 'success' else '⚠️ 后备数据'}</p>
    </div>
    
    <h2>₿ 加密货币实时数据</h2>
    
    <div class="price-card">
        <h3>比特币 (BTC)</h3>
        <table class="data-table">
            <tr>
                <td><strong>当前价格</strong></td>
                <td style="font-size: 28px; font-weight: bold;">${btc_price:,.2f if isinstance(btc_price, (int, float)) else btc_price}</td>
            </tr>
            <tr>
                <td><strong>24小时变化</strong></td>
                <td class="{ 'positive' if isinstance(btc_change, (int, float)) and btc_change > 0 else 'negative' if isinstance(btc_change, (int, float)) and btc_change < 0 else '' }">
                    {f"{btc_change:+.2f}%" if isinstance(btc_change, (int, float)) else btc_change}
                </td>
            </tr>
            <tr>
                <td><strong>数据源</strong></td>
                <td>{btc_info.get('source', '未知')}</td>
            </tr>
            <tr>
                <td><strong>更新时间</strong></td>
                <td>{btc_info.get('timestamp', '未知')}</td>
            </tr>
        </table>
    </div>
    
    <div class="price-card">
        <h3>瑞波币 (XRP)</h3>
        <table class="data-table">
            <tr>
                <td><strong>当前价格</strong></td>
                <td style="font-size: 28px; font-weight: bold;">${xrp_price:,.2f if isinstance(xrp_price, (int, float)) else xrp_price}</td>
            </tr>
            <tr>
                <td><strong>24小时变化</strong></td>
                <td class="{ 'positive' if isinstance(xrp_change, (int, float)) and xrp_change > 0 else 'negative' if isinstance(xrp_change, (int, float)) and xrp_change < 0 else '' }">
                    {f"{xrp_change:+.2f}%" if isinstance(xrp_change, (int, float)) else xrp_change}
                </td>
            </tr>
            <tr>
                <td><strong>数据源</strong></td>
                <td>{xrp_info.get('source', '未知')}</td>
            </tr>
            <tr>
                <td><strong>更新时间</strong></td>
                <td>{xrp_info.get('timestamp', '未知')}</td>
            </tr>
        </table>
    </div>
    
    <h2>📈 股票市场数据</h2>
    
    <table class="data-table">
        <thead>
            <tr>
                <th>股票代码</th>
                <th>公司名称</th>
                <th>价格</th>
                <th>涨跌幅</th>
            </tr>
        </thead>
        <tbody>
'''

        # 添加股票数据行
        if stock_data['status'] == 'success':
            for symbol, data in stock_data['data'].items():
                price = data.get('price')
                change = data.get('change')
                
                html_content += f'''
            <tr>
                <td><strong>{symbol}</strong></td>
                <td>{data.get('name', '')}</td>
                <td>${price:,.2f if isinstance(price, (int, float)) else price}</td>
                <td class="{ 'positive' if isinstance(change, (int, float)) and change > 0 else 'negative' if isinstance(change, (int, float)) and change < 0 else '' }">
                    {f"{change:+.2f}%" if isinstance(change, (int, float)) else change}
                </td>
            </tr>
'''
        else:
            html_content += '''
            <tr>
                <td colspan="4" style="text-align: center; color: #666;">
                    ⚠️ 股票数据暂时不可用
                </td>
            </tr>
'''
        
        html_content += f'''
        </tbody>
    </table>
    
    <div class="price-card">
        <h3>🎯 市场分析</h3>
        <p><strong>BTC分析:</strong> 当前价格${btc_price:,.2f if isinstance(btc_price, (int, float)) else btc_price}，24小时变化{btc_change:+.2f if isinstance(btc_change, (int, float)) else btc_change}%。</p>
        <p><strong>XRP分析:</strong> 当前价格${xrp_price:,.2f if isinstance(xrp_price, (int, float)) else xrp_price}，24小时变化{xrp_change:+.2f if isinstance(xrp_change, (int, float)) else xrp_change}%。</p>
        <p><strong>整体市场:</strong> 加密货币市场表现强劲，股票市场相对稳定。</p>
    </div>
    
    <div style="text-align: center; margin: 40px 0; padding: 20px; background: #f8f9fa; border-radius: 10px;">
        <p><strong>📱 报告信息</strong></p>
        <p>生成时间: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>数据状态: {'✅ 实时数据' if crypto_data['status'] == 'success' else '⚠️ 后备数据'}</p>
        <p>下次更新: 每日08:00 (北京时间)</p>
    </div>
    
    <script>
        // 简单的数据刷新提示
        console.log('实时数据报告已生成');
        console.log('数据源: {crypto_data.get("source", "未知")}');
        console.log('BTC价格: ${btc_price}');
        console.log('XRP价格: ${xrp_price}');
    </script>
</body>
</html>
'''
        
        # 保存报告
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"✅ HTML报告已生成: {report_file}")
        return report_file
    
    def run(self):
        """运行报告生成流程"""
        logger.info("🚀 开始生成每日报告...")
        
        # 获取数据
        crypto_data = self.get_real_time_crypto_data()
        stock_data = self.get_stock_data()
        
        # 生成报告
        report_file = self.generate_html_report(crypto_data, stock_data)
        
        logger.info("🎉 每日报告生成完成！")
        
        return {
            'status': 'success',
            'report_file': report_file,
            'crypto_data': crypto_data,
            'stock_data': stock_data,
            'timestamp': self.timestamp.isoformat()
        }

def main():
    """主函数"""
    print("=" * 60)
    print("📊 增强版金融市场分析系统 V2.0")
    print("=" * 60)
    
    reporter = EnhancedDailyReporter()
    result = reporter.run()
    
    if result['status'] == 'success':
        print(f"\n✅ 报告生成成功！")
        print(f"   报告文件: {result['report_file']}")
        print(f"   加密货币数据源: {result['crypto_data'].get('source', '未知')}")
        print(f"   股票数据状态: {result['stock_data'].get('status', '未知')}")
        
        # 显示关键数据
        crypto_data = result['crypto_data']['data']
        if 'BTC' in crypto_data:
            btc_price = crypto_data['BTC'].get('price', 'N/A')
            print(f"\n📊 关键数据:")
            print(f"   BTC: ${btc_price:,.2f if isinstance(btc_price, (int, float)) else btc_price}")
        
        if 'XRP' in crypto_data:
            xrp_price = crypto_data['XRP'].get('price', 'N/A')
            print(f"   XRP: ${xrp_price:,.2f if isinstance(xrp_price, (int, float)) else xrp_price}")
    else:
        print(f"\n❌ 报告生成失败")
    
    print("\n" + "=" * 60)
    print("🎯 系统运行完成")

if __name__ == "__main__":
    main()
