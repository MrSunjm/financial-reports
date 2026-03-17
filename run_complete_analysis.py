#!/usr/bin/env python3
"""
运行完整技术分析并生成报告
"""

import sys
import os
from datetime import datetime
import json

# 导入分析器
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from complete_technical_analysis import CompleteTechnicalAnalyzer
    print("✅ 分析器导入成功")
except ImportError as e:
    print(f"❌ 分析器导入失败: {e}")
    sys.exit(1)

def main():
    """主函数"""
    print("=" * 80)
    print("📊 完整多币种技术分析报告生成系统")
    print("=" * 80)
    
    # 创建分析器
    analyzer = CompleteTechnicalAnalyzer()
    
    # 生成完整报告
    print(f"\n🎯 开始生成完整分析报告...")
    print(f"📅 分析时间: {analyzer.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"💰 分析币种: {', '.join(analyzer.symbols)}")
    
    report = analyzer.generate_complete_report()
    
    if report['status'] == 'success':
        print(f"\n✅ 分析完成！")
        
        # 显示总结信息
        summary = report['summary']
        print(f"\n📋 分析总结:")
        print(f"   分析币种: {summary['total_coins_analyzed']} 个")
        print(f"   买入信号: {summary['buy_signals']} 个")
        print(f"   持有信号: {summary['hold_signals']} 个")
        print(f"   观望信号: {summary['watch_signals']} 个")
        print(f"   平均信心度: {summary['average_confidence']}%")
        print(f"   市场情绪: {summary['market_sentiment']}")
        print(f"   投资建议: {summary['recommendation']}")
        
        # 显示关键币种数据
        print(f"\n📈 关键币种实时数据:")
        for symbol in ['BTC', 'XRP']:
            if symbol in report['crypto_analysis']:
                data = report['crypto_analysis'][symbol]
                basic = data['basic_info']
                signal = data['technical_indicators']['trading_signal']
                
                print(f"\n   {symbol}:")
                print(f"     价格: ${basic['price']:,.2f}")
                print(f"     24h变化: {basic['change_24h']:+.2f}%")
                print(f"     交易信号: {signal['action']}")
                print(f"     信心度: {signal['confidence']}%")
                print(f"     原因: {signal['reason']}")
        
        # 生成HTML报告
        print(f"\n📄 生成HTML报告...")
        generate_html_report(report)
        
        # 保存JSON数据
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_file = f"reports/analysis_data_{timestamp}.json"
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ JSON数据已保存: {json_file}")
        
        # 推送到GitHub
        print(f"\n🚀 推送到GitHub...")
        os.system(f"git add reports/complete_analysis_*.html 2>/dev/null || echo '无新HTML报告'")
        os.system(f"git add {json_file}")
        os.system('git commit -m "添加完整技术分析报告" 2>/dev/null || echo "提交信息已存在"')
        os.system('git push origin main')
        
        print(f"\n🎉 完整分析报告生成完成！")
        print(f"   报告已推送到GitHub")
        print(f"   访问URL: https://MrSunjm.github.io/financial-reports/reports/")
        
    else:
        print(f"\n❌ 分析失败: {report.get('error', '未知错误')}")

def generate_html_report(report_data: Dict[str, Any]):
    """生成HTML报告（简化版）"""
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"reports/complete_analysis_{timestamp}.html"
    
    # 提取数据
    crypto_analysis = report_data['crypto_analysis']
    news = report_data['international_news']
    trends = report_data['financial_trends']
    summary = report_data['summary']
    
    # 生成HTML内容
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 完整多币种技术分析报告</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            line-height: 1.8;
            font-size: 18px;
            background: #f5f7fa;
        }}
        
        .container {{
            max-width: 100%;
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
        
        .header h1 {{
            font-size: 36px;
            margin: 0 0 15px 0;
        }}
        
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        
        .summary-card {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }}
        
        .crypto-section {{
            padding: 30px;
        }}
        
        .crypto-tabs {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 30px;
        }}
        
        .crypto-tab {{
            padding: 12px 24px;
            background: #f8f9fa;
            border: none;
            border-radius: 25px;
            font-size: 18px;
            cursor: pointer;
        }}
        
        .crypto-tab.active {{
            background: #3498db;
            color: white;
        }}
        
        .crypto-content {{
            display: none;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        
        .crypto-content.active {{
            display: block;
        }}
        
        .price-display {{
            font-size: 32px;
            font-weight: bold;
            margin: 0 0 20px 0;
        }}
        
        .indicators-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        
        .indicator-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #3498db;
        }}
        
        .signal-box {{
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            margin: 30px 0;
            font-size: 20px;
            font-weight: bold;
        }}
        
        .signal-buy {{
            background: #d4edda;
            color: #155724;
        }}
        
        .signal-hold {{
            background: #fff3cd;
            color: #856404;
        }}
        
        .macro-section {{
            padding: 30px;
            background: #f8f9fa;
        }}
        
        .news-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        
        .news-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #3498db;
        }}
        
        .footer {{
            text-align: center;
            padding: 30px;
            background: #2c3e50;
            color: white;
        }}
        
        @media (max-width: 768px) {{
            body {{ font-size: 17px; }}
            .header h1 {{ font-size: 28px; }}
            .price-display {{ font-size: 28px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 头部 -->
        <div class="header">
            <h1>📊 完整多币种技术分析报告</h1>
            <p>基于实时数据 + 技术指标 + 国际新闻 + 金融趋势</p>
            <p>生成时间: {report_data['timestamp']}</p>
            <p>分析币种: BTC, ETH, BNB, XRP, SOL, LINK</p>
        </div>
        
        <!-- 总结 -->
        <div class="summary-grid">
            <div class="summary-card">
                <div style="font-size: 32px; font-weight: bold;">{summary['total_coins_analyzed']}</div>
                <div>分析币种</div>
            </div>
            <div class="summary-card">
                <div style="font-size: 32px; font-weight: bold; color: #27ae60;">{summary['buy_signals']}</div>
                <div>买入信号</div>
            </div>
            <div class="summary-card">
                <div style="font-size: 32px; font-weight: bold; color: #f39c12;">{summary['hold_signals']}</div>
                <div>持有信号</div>
            </div>
            <div class="summary-card">
                <div style="font-size: 32px; font-weight: bold;">{summary['average_confidence']}%</div>
                <div>平均信心度</div>
            </div>
        </div>
        
        <!-- 市场情绪 -->
        <div style="padding: 30px; text-align: center; background: {summary['sentiment_color']}20; margin: 20px; border-radius: 10px;">
            <h2 style="margin: 0 0 15px 0;">🎯 市场情绪: {summary['market_sentiment']}</h2>
            <p style="font-size: 20px; font-weight: bold;">{summary['recommendation']}</p>
        </div>
        
        <!-- 加密货币分析 -->
        <div class="crypto-section">
            <h2 style="font-size: 28px; margin: 0 0 30px 0; color: #2c3e50;">₿ 加密货币技术分析</h2>
            
            <!-- 标签 -->
            <div class="crypto-tabs" id="cryptoTabs">
'''

    # 添加标签
    for symbol in crypto_analysis.keys():
        html_content += f'                <button class="crypto-tab" onclick="showCrypto(\'{symbol.lower()}\')">{symbol}</button>\n'
    
    html_content += '''            </div>
'''
    
    # 添加每个币种内容
    for symbol, analysis in crypto_analysis.items():
        basic = analysis['basic_info']
        indicators = analysis['technical_indicators']
        signal = indicators['trading_signal']
        
        # 确定信号样式
        signal_class = 'signal-buy' if signal['action'] == '买入' else 'signal-hold' if signal['action'] == '持有' else 'signal-watch'
        
        html_content += f'''
            <!-- {symbol}分析 -->
            <div class="crypto-content" id="{symbol.lower()}-content">
                <div class="price-display">
                    {symbol}: ${basic['price']:,.2f}
                    <span style="font-size: 24px; color: {'#27ae60' if basic['change_24h'] > 0 else '#e74c3c'}">
                        ({basic['change_24h']:+.2f}%)
                    </span>
                </div>
                
                <div class="indicators-grid">
                    <div class="indicator-card">
                        <h3>📊 布林带</h3>
                        <p>上轨: ${indicators['bollinger_bands']['upper']:,.2f}</p>
                        <p>中轨: ${indicators['bollinger_bands']['middle']:,.2f}</p>
                        <p>下轨: ${indicators['bollinger_bands']['lower']:,.2f}</p>
                        <p>位置: {indicators['bollinger_bands']['position']}%</p>
                    </div>
                    
                    <div class="indicator-card">
                        <h3>📈 MACD</h3>
                        <p>信号: {indicators['macd']['signal']}</p>
                        <p>强度: {indicators['macd']['strength']}</p>
                        <p>MACD值: {indicators['macd']['value']}</p>
                    </div>
                    
                    <div class="indicator-card">
                        <h3>🌊 ABC浪</h3>
                        <p>当前浪: {indicators['abc_wave']['current_wave']}</p>
                        <p>完成度: {indicators['abc_wave']['completion']}%</p>
                        <p>目标价: ${indicators['abc_wave']['target_price']:,.2f}</p>
                    </div>
                </div>
                
                <div class="{signal_class} signal-box">
                    <div style="font-size: 28px;">{signal['action']}</div>
                    <div style="font-size: 20px;">信心度: {signal['confidence']}%</div>
                    <div style="font-size: 18px; margin-top: 10px;">{signal['reason']}</div>
                </div>
                
                <div style="font-size: 16px; color: #666; text-align: center;">
                    数据源: {basic.get('source', 'CoinGecko')} | 更新时间: {basic.get('timestamp', '')}
                </div>
            </div>
'''
    
    html_content += '''        </div>
        
        <!-- 国际新闻 -->
        <div class="macro-section">
            <h2 style="font-size: 28px; margin: 0 0 30px 0; color: #2c3e50;">🌍 国际新闻影响分析</h2>
            <div class="news-grid">
'''
    
    # 添加新闻
    for item in news:
        impact_class = 'positive' if 'positive' in item['impact'] else 'negative' if 'negative' in item['impact'] else 'caution'
        html_content += f'''
                <div class="news-card {impact_class}">
                    <div class="news-category">{item['category']}</div>
                    <div class="news-title">{item['news']}</div>
                    <div class="news-analysis">{item['analysis']}</div>
                    <div style="margin-top: 15px; font-weight: bold;">影响: {item['effect_on_crypto']}</div>
                </div>
'''
    
    html_content += '''            </div>
        </div>
        
        <!-- 金融趋势 -->
        <div style="padding: 30px;">
            <h2 style="font-size: 28px; margin: 0 0 30px 0; color: #2c3e50;">📈 金融趋势背景</h2>
            <div style="background: #f8f9fa; padding: 25px; border-radius: 10px;">
                <h3 style="margin: 0 0 20px 0;">全球市场趋势</h3>
'''

    # 添加趋势
    for market, data in trends['global_markets'].items():
        html_content += f'                <p><strong>{market.replace("_", " ").title()}:</strong> {data["trend"]} - {data["driver"]}</p>\n'
    
    html_content += f'''
                <h3 style="margin: 20px 0;">整体评估</h3>
                <p>{trends["overall_assessment"]}</p>
            </div>
        </div>
        
        <!-- 脚部 -->
        <div class="footer">
            <p>📊 金融市场分析系统 V2.0</p>
            <p>基于实时数据，技术分析仅供参考</p>
            <p>投资有风险，入市需谨慎</p>
            <p style="margin-top: 20px; font-size: 16px;">
                访问更多报告: https://MrSunjm.github.io/financial-reports/reports/
            </p>
        </div>
    </div>
    
    <script>
        // 默认显示BTC
        document.addEventListener('DOMContentLoaded', function() {{
            showCrypto('btc');
            document.querySelector('.crypto-tab').classList.add('active');
        }});
        
        function showCrypto(symbol) {{
            // 隐藏所有内容
            document.querySelectorAll('.crypto-content').forEach(el => {{
                el.classList.remove('active');
            }});
            
            // 移除所有标签的active类
            document.querySelectorAll('.crypto-tab').forEach(el => {
                el.classList.remove('active');
            });
            
            // 显示选中的内容
            document.getElementById(symbol + '-content').classList.add('active');
            
            // 激活对应的标签
            document.querySelectorAll('.crypto-tab').forEach(el => {
                if (el.textContent.toLowerCase() === symbol.toUpperCase()) {
                    el.classList.add('active');
                }
            });
        }
    </script>
</body>
</html>'''
    
    # 保存HTML文件
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ HTML报告已生成: {report_file}")
    return report_file

if __name__ == "__main__":
    main()
