#!/usr/bin/env python3
"""
生成最终技术分析报告
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
    print("📊 最终技术分析报告生成")
    print("=" * 80)
    
    # 创建分析器
    analyzer = CompleteTechnicalAnalyzer()
    
    # 生成报告
    print(f"\n🎯 开始生成分析报告...")
    print(f"📅 分析时间: {analyzer.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    
    report = analyzer.generate_complete_report()
    
    if report['status'] == 'success':
        print(f"\n✅ 分析完成！")
        
        # 显示总结
        summary = report['summary']
        print(f"\n📋 分析总结:")
        print(f"   市场情绪: {summary['market_sentiment']}")
        print(f"   平均信心度: {summary['average_confidence']}%")
        print(f"   买入信号: {summary['buy_signals']} 个")
        print(f"   持有信号: {summary['hold_signals']} 个")
        
        # 显示实时数据
        print(f"\n📈 实时数据:")
        for symbol in ['BTC', 'XRP', 'ETH']:
            if symbol in report['crypto_analysis']:
                data = report['crypto_analysis'][symbol]
                basic = data['basic_info']
                print(f"   {symbol}: ${basic['price']:,.2f} ({basic['change_24h']:+.2f}%)")
        
        # 生成HTML报告
        generate_html_report(report)
        
    else:
        print(f"\n❌ 分析失败: {report.get('error', '未知错误')}")

def generate_html_report(report_data):
    """生成HTML报告"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"reports/final_technical_analysis_{timestamp}.html"
    
    crypto_analysis = report_data['crypto_analysis']
    news = report_data['international_news']
    trends = report_data['financial_trends']
    summary = report_data['summary']
    
    # 生成HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 最终技术分析报告</title>
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
        .crypto-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            padding: 30px;
        }}
        .crypto-card {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
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
        .footer {{
            text-align: center;
            padding: 30px;
            background: #2c3e50;
            color: white;
        }}
        @media (max-width: 768px) {{
            body {{ font-size: 17px; }}
            .crypto-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 最终技术分析报告</h1>
            <p>生成时间: {report_data['timestamp']}</p>
            <p>分析币种: BTC, ETH, BNB, XRP, SOL, LINK</p>
        </div>
        
        <div style="padding: 30px; text-align: center;">
            <h2>🎯 市场情绪: {summary['market_sentiment']}</h2>
            <p style="font-size: 20px; font-weight: bold;">平均信心度: {summary['average_confidence']}%</p>
        </div>
        
        <div class="crypto-grid">
'''
    
    # 添加加密货币卡片
    for symbol, analysis in crypto_analysis.items():
        basic = analysis['basic_info']
        indicators = analysis['technical_indicators']
        signal = indicators['trading_signal']
        
        signal_class = 'signal-buy' if signal['action'] == '买入' else 'signal-hold'
        
        html += f'''
            <div class="crypto-card">
                <div style="font-size: 24px; font-weight: bold;">{symbol}</div>
                <div style="font-size: 28px; font-weight: bold; margin: 10px 0;">${basic['price']:,.2f}</div>
                <div style="color: {'#27ae60' if basic['change_24h'] > 0 else '#e74c3c'}; font-size: 20px;">
                    {basic['change_24h']:+.2f}%
                </div>
                
                <div style="margin: 20px 0;">
                    <div>布林带: {indicators['bollinger_bands']['position']}%</div>
                    <div>MACD: {indicators['macd']['signal']}</div>
                    <div>ABC浪: {indicators['abc_wave']['current_wave']}</div>
                    <div>趋势: {indicators['trend']['long_term']['analysis']}</div>
                </div>
                
                <div class="{signal_class} signal-box">
                    <div>{signal['action']}</div>
                    <div>信心度: {signal['confidence']}%</div>
                </div>
            </div>
'''
    
    html += '''        </div>
        
        <div style="padding: 30px;">
            <h2>🌍 国际新闻影响</h2>
            <div style="background: #f8f9fa; padding: 25px; border-radius: 10px;">
'''
    
    # 添加新闻
    for item in news[:3]:  # 只显示前3条
        html += f'''
                <div style="margin-bottom: 20px;">
                    <div style="font-weight: bold;">{item['news']}</div>
                    <div style="color: #555;">{item['analysis']}</div>
                </div>
'''
    
    html += f'''            </div>
        </div>
        
        <div class="footer">
            <p>📊 金融市场分析系统 V2.0</p>
            <p>基于CoinGecko实时数据</p>
            <p>访问URL: https://MrSunjm.github.io/financial-reports/reports/</p>
        </div>
    </div>
</body>
</html>'''
    
    # 保存文件
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ HTML报告已生成: {report_file}")
    
    # 推送到GitHub
    os.system(f"git add {report_file}")
    os.system('git commit -m "添加最终技术分析报告" 2>/dev/null || echo "提交信息已存在"')
    os.system('git push origin main')
    
    print(f"\n🎉 最终报告URL:")
    print(f"   https://MrSunjm.github.io/financial-reports/{report_file}")
    
    return report_file

if __name__ == "__main__":
    main()
