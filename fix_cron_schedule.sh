#!/bin/bash
# 定时任务修复脚本

echo "🔧 修复定时任务配置..."
echo "========================"

# 1. 检查当前cron配置
echo "1. 检查当前cron任务..."
crontab -l 2>/dev/null | grep -i "financial\|daily\|report" || echo "未找到相关定时任务"

# 2. 创建新的cron任务
echo ""
echo "2. 创建新的定时任务..."
CRON_JOB="0 0 * * * cd /Users/tik/Desktop/financial-reports-online && /usr/bin/python3 auto_daily_report.py"
echo "定时任务: $CRON_JOB"
echo "执行时间: 每日00:00 (UTC) = 08:00 (北京时间)"

# 3. 添加到crontab
echo ""
echo "3. 添加到crontab..."
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

# 4. 验证添加
echo ""
echo "4. 验证定时任务..."
crontab -l | grep -i "auto_daily_report"

echo ""
echo "✅ 定时任务修复完成！"
echo "   下次执行时间: 明日08:00 (北京时间)"
echo "   脚本路径: /Users/tik/Desktop/financial-reports-online/auto_daily_report.py"
