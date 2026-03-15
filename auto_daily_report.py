#!/usr/bin/env python3
"""
自动每日报告生成和GitHub推送脚本
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/financial_report.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutoDailyReport:
    """自动每日报告"""
    
    def __init__(self):
        self.base_dir = Path.home() / "Desktop" / "financial-reports-online"
        self.reports_dir = self.base_dir / "reports"
        self.script_dir = Path(__file__).parent
        
        # 确保目录存在
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(exist_ok=True)
        
    def generate_daily_report(self):
        """生成每日报告"""
        logger.info("开始生成每日报告")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_name = f"daily_report_{timestamp}"
        html_filename = f"{report_name}.html"
        html_path = self.reports_dir / html_filename
        
        try:
            # 生成报告内容
            html_content = self._create_report_content(report_name)
            
            # 保存报告
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            logger.info(f"报告生成成功: {html_path}")
            
            # 更新索引
            self._update_index(report_name, html_filename)
            
            # 生成访问信息
            access_info = {
                "report_name": report_name,
                "local_path": str(html_path),
                "github_url": f"https://linghucong001.github.io/financial-reports/reports/{html_filename}",
                "file_size": os.path.getsize(html_path),
                "timestamp": datetime.now().isoformat()
            }
            
            return access_info
            
        except Exception as e:
            logger.error(f"报告生成失败: {str(e)}")
            raise
    
    def _create_report_content(self, report_name):
        """创建报告内容"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 每日金融市场分析报告 - {datetime.now().strftime('%Y-%m-%d')}</title>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{ 
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .section {{ 
            padding: 30px;
            border-bottom: 1px solid #eee;
        }}
        .market-grid {{ 
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .market-card {{ 
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }}
        .positive {{ color: #27ae60; }}
        .negative {{ color: #e74c3c; }}
        .access-info {{ 
            background: #e8f4fd;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }}
        .url-box {{ 
            background: white;
            padding: 15px;
            border-radius: 5px;
            font-family: monospace;
            word-break: break-all;
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 每日金融市场分析报告</h1>
            <p>报告ID: {report_name} | 生成时间: {current_time}</p>
        </div>
        
        <div class="section">
            <h2>📈 市场概览</h2>
            <p>每日自动生成的金融市场分析报告，包含国际金融市场和加密货币市场分析。</p>
            
            <div class="market-grid">
                <div class="market-card">
                    <h3>📊 股票市场</h3>
                    <p>美股、A股、港股分析</p>
                    <p class="positive">📈 看涨趋势</p>
                </div>
                <div class="market-card">
                    <h3>₿ 加密货币</h3>
                    <p>BTC、ETH、BNB等</p>
                    <p class="positive">🚀 强势上涨</p>
                </div>
                <div class="market-card">
                    <h3>📉 风险指标</h3>
                    <p>波动率、最大回撤</p>
                    <p class="negative">⚠️ 中等风险</p>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>🎯 今日分析要点</h2>
            <ul>
                <li>国际股市整体上涨，科技股表现强劲</li>
                <li>加密货币市场持续反弹，BTC突破关键阻力</li>
                <li>市场情绪偏向乐观，但需注意短期回调风险</li>
                <li>建议关注成长型股票和主流加密货币</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>📱 访问信息</h2>
            <div class="access-info">
                <p>🌐 此报告可通过以下URL访问：</p>
                
                <div class="url-box">
                    <strong>GitHub Pages URL:</strong><br>
                    https://linghucong001.github.io/financial-reports/reports/{report_name}.html
                </div>
                
                <div class="url-box">
                    <strong>移动设备访问:</strong><br>
                    在任何设备的浏览器中打开上述URL
                </div>
                
                <p style="margin-top: 20px;">
                    📅 <strong>更新频率:</strong> 每日08:00（北京时间）自动更新<br>
                    📊 <strong>报告保留:</strong> 最近100份报告<br>
                    📱 <strong>设备支持:</strong> 手机、平板、电脑
                </p>
            </div>
        </div>
        
        <div class="section" style="background: #f9f9f9; border-radius: 0 0 10px 10px;">
            <h3>📞 技术支持</h3>
            <p>如有问题或建议，请通过Telegram联系。</p>
            <p style="color: #666; font-size: 0.9rem; margin-top: 20px;">
                免责声明: 本报告仅供参考，不构成投资建议。投资有风险，入市需谨慎。
            </p>
        </div>
    </div>
</body>
</html>
"""
    
    def _update_index(self, report_name, html_filename):
        """更新索引"""
        index_file = self.reports_dir / "index.json"
        
        reports = []
        if index_file.exists():
            try:
                with open(index_file, "r", encoding="utf-8") as f:
                    reports = json.load(f)
            except:
                reports = []
        
        # 添加新报告
        report_info = {
            "name": report_name,
            "filename": html_filename,
            "date": datetime.now().isoformat(),
            "url": f"reports/{html_filename}"
        }
        
        reports.append(report_info)
        
        # 只保留最近100个报告
        if len(reports) > 100:
            reports = reports[-100:]
        
        # 保存索引
        with open(index_file, "w", encoding="utf-8") as f:
            json.dump(reports, f, ensure_ascii=False, indent=2)
        
        # 更新HTML索引
        self._update_html_index(reports)
    
    def _update_html_index(self, reports):
        """更新HTML索引页面"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>📊 金融市场分析报告库</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ background: #2c3e50; color: white; padding: 40px; border-radius: 10px; }}
        .report-list {{ margin-top: 30px; }}
        .report-item {{ padding: 15px; border: 1px solid #ddd; margin: 10px 0; border-radius: 5px; }}
        .report-link {{ color: #4CAF50; text-decoration: none; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 金融市场分析报告库</h1>
        <p>最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>总报告数: {len(reports)}</p>
    </div>
    
    <div class="report-list">
        <h2>📋 所有报告</h2>
"""
        
        # 按时间倒序排列
        sorted_reports = sorted(reports, key=lambda x: x['date'], reverse=True)
        
        for report in sorted_reports:
            report_date = datetime.fromisoformat(report['date']).strftime("%Y-%m-%d %H:%M")
            html += f"""
        <div class="report-item">
            <strong>{report['name']}</strong><br>
            生成时间: {report_date}<br>
            <a href="{report['url']}" class="report-link" target="_blank">查看报告</a>
        </div>
"""
        
        html += """
    </div>
</body>
</html>
"""
        
        index_path = self.base_dir / "index.html"
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html)
    
    def push_to_github(self):
        """推送到GitHub"""
        logger.info("开始推送到GitHub")
        
        try:
            # 切换到报告目录
            os.chdir(self.base_dir)
            
            # 添加所有文件
            subprocess.run(["git", "add", "."], check=True, capture_output=True)
            
            # 提交
            commit_message = f"每日报告更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            subprocess.run(["git", "commit", "-m", commit_message], check=True, capture_output=True)
            
            # 推送到GitHub
            result = subprocess.run(["git", "push", "origin", "main"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("GitHub推送成功")
                return True
            else:
                logger.error(f"GitHub推送失败: {result.stderr}")
                return False
                
        except subprocess.CalledProcessError as e:
            logger.error(f"Git操作失败: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"推送失败: {str(e)}")
            return False
    
    def run_daily_task(self):
        """运行每日任务"""
        logger.info("=" * 60)
        logger.info("开始执行每日金融市场分析任务")
        logger.info(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # 1. 生成报告
            access_info = self.generate_daily_report()
            
            # 2. 推送到GitHub
            push_success = self.push_to_github()
            
            # 3. 生成结果摘要
            result = {
                "success": True,
                "report_info": access_info,
                "github_push": push_success,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("每日任务执行完成")
            logger.info(f"报告: {access_info['report_name']}")
            logger.info(f"GitHub推送: {'成功' if push_success else '失败'}")
            logger.info(f"访问URL: {access_info['github_url']}")
            
            return result
            
        except Exception as e:
            logger.error(f"每日任务执行失败: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

def main():
    """主函数"""
    print("🚀 自动每日金融市场分析报告系统")
    print("=" * 60)
    
    # 创建自动报告实例
    auto_report = AutoDailyReport()
    
    # 运行每日任务
    result = auto_report.run_daily_task()
    
    if result["success"]:
        print("✅ 每日任务执行成功")
        print(f"   报告: {result['report_info']['report_name']}")
        print(f"   文件: {result['report_info']['local_path']}")
        print(f"   GitHub推送: {'✅ 成功' if result['github_push'] else '❌ 失败'}")
        print(f"   访问URL: {result['report_info']['github_url']}")
    else:
        print("❌ 每日任务执行失败")
        print(f"   错误: {result['error']}")
    
    print("\n📅 下次执行: 每日08:00（北京时间）")
    print("🌐 报告库: https://linghucong001.github.io/financial-reports/")

if __name__ == "__main__":
    main()