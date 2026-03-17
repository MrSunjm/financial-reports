#!/usr/bin/env python3
"""
自动化完整分析脚本
每日08:00自动执行
"""

import sys
import os
from datetime import datetime

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """主函数"""
    print("=" * 80)
    print("🕗 自动化金融市场分析系统")
    print("=" * 80)
    
    # 检查时间
    now = datetime.now()
    beijing_time = now.strftime('%Y-%m-%d %H:%M:%S')
    print(f"执行时间: {beijing_time} (北京时间)")
    
    try:
        # 导入分析器
        from complete_analysis_framework import CompleteFinancialAnalyzer
        
        # 创建分析器并生成报告
        analyzer = CompleteFinancialAnalyzer()
        analysis_data = analyzer.generate_complete_analysis()
        
        # 推送到GitHub
        print("\n🚀 推送到GitHub...")
        report_file = analysis_data['report_file']
        
        import subprocess
        subprocess.run(['git', 'add', report_file], capture_output=True)
        subprocess.run(['git', 'add', 'reports/NAVIGATION_INDEX.html'], capture_output=True)
        subprocess.run(['git', 'add', 'analysis_history.json'], capture_output=True)
        
        commit_message = f"添加每日金融市场分析报告 {datetime.now().strftime('%Y%m%d')}"
        subprocess.run(['git', 'commit', '-m', commit_message], capture_output=True)
        subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True)
        
        print(f"\n✅ 自动化分析完成！")
        print(f"   报告文件: {report_file}")
        print(f"   导航页面: reports/NAVIGATION_INDEX.html")
        print(f"   访问URL: https://MrSunjm.github.io/financial-reports/{report_file}")
        
        # 发送Telegram通知（如果需要）
        # 这里可以添加Telegram通知代码
        
    except Exception as e:
        print(f"\n❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
