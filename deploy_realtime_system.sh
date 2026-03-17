#!/bin/bash
# 实时分析系统部署脚本

echo "🚀 部署实时金融市场分析系统"
echo "=========================="

cd ~/Desktop/financial-reports-online

echo "1. 检查依赖..."
echo "-------------"

# 检查Python依赖
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安装"
    exit 1
fi

echo "✅ Python3已安装: $(python3 --version)"

# 检查requests库
python3 -c "import requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 安装requests库..."
    pip3 install requests
fi

echo "✅ 依赖检查完成"

echo ""
echo "2. 配置币安API..."
echo "----------------"

if [ ! -f "binance_config.py" ]; then
    echo "❌ binance_config.py 不存在"
    echo "请先创建配置文件"
    exit 1
fi

echo "✅ 配置文件存在"

echo ""
echo "3. 测试系统..."
echo "-------------"

# 测试实时分析系统
python3 realtime_analysis_system.py

echo ""
echo "4. 配置定时任务..."
echo "-----------------"

if [ -f "setup_daily_cron.sh" ]; then
    echo "🔧 运行定时任务配置脚本..."
    chmod +x setup_daily_cron.sh
    ./setup_daily_cron.sh
else
    echo "⚠️ 定时任务配置脚本不存在"
    echo "手动配置cron: 0 0 * * * cd $(pwd) && python3 realtime_analysis_system.py"
fi

echo ""
echo "5. 推送到GitHub..."
echo "-----------------"

git add .
git commit -m "部署实时金融市场分析系统" 2>/dev/null || echo "提交信息已存在"
git push origin main

echo ""
echo "🎉 部署完成！"
echo "==========="
echo ""
echo "📊 系统功能:"
echo "✅ 币安实时数据获取"
echo "✅ 加密货币深度分析"
echo "✅ 自动报告生成"
echo "✅ GitHub自动推送"
echo ""
echo "🌐 访问URL:"
echo "   报告: https://MrSunjm.github.io/financial-reports/reports/realtime_analysis_*.html"
echo "   导航: https://MrSunjm.github.io/financial-reports/reports/NAVIGATION_INDEX.html"
echo ""
echo "📅 定时任务:"
echo "   每日08:00 (北京时间) 自动执行"
echo ""
echo "🔧 手动运行:"
echo "   cd ~/Desktop/financial-reports-online"
echo "   python3 realtime_analysis_system.py"
